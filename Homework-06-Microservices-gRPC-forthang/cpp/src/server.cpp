#include <userver/utest/using_namespace_userver.hpp>
#include <userver/ugrpc/server/service_component_base.hpp>
#include <unordered_map>
#include <vector>
#include <mutex>
#include <numeric>

// Подключаем сгенерированный заголовочный файл
#include <lifeos/metrics_service.usrv.pb.hpp>

namespace lifeos {

class VitalSignsServiceComponent final : public lifeos::VitalSignsServiceBase::Component {
public:
    // Стандартный конструктор компонента
    static constexpr std::string_view kName = "vital-signs-service";

    VitalSignsServiceComponent(const components::ComponentConfig& config,
                               const components::ComponentContext& context)
        : lifeos::VitalSignsServiceBase::Component(config, context) {}

    // Реализация метода RecordMetric
    void RecordMetric(
        lifeos::VitalSignsServiceBase::RecordMetricCall& call,
        lifeos::MetricRequest&& request) override
    {
        std::lock_guard<std::mutex> lock(mutex_);
        
        // Создаем ключ для хранения: user_id + type
        std::string key = request.user_id() + "_" + std::to_string(static_cast<int>(request.type()));
        
        // Сохраняем значение
        metrics_[key].push_back(request.value());
        
        lifeos::MetricResponse response;
        response.set_success(true);
        response.set_message("Metric recorded successfully");

        call.Finish(response);
    }

    // Реализация метода GetAverage
    void GetAverage(
        lifeos::VitalSignsServiceBase::GetAverageCall& call,
        lifeos::AverageRequest&& request) override
    {
        std::lock_guard<std::mutex> lock(mutex_);
        
        std::string key = request.user_id() + "_" + std::to_string(static_cast<int>(request.type()));
        
        lifeos::AverageResponse response;
        
        auto it = metrics_.find(key);
        if (it != metrics_.end() && !it->second.empty()) {
            const auto& values = it->second;
            double sum = std::accumulate(values.begin(), values.end(), 0.0);
            double average = sum / values.size();
            
            response.set_average_value(average);
            response.set_count(static_cast<int32_t>(values.size()));
        } else {
            response.set_average_value(0.0);
            response.set_count(0);
        }

        call.Finish(response);
    }

private:
    // In-memory хранилище: ключ -> список значений
    std::unordered_map<std::string, std::vector<double>> metrics_;
    std::mutex mutex_;
};

// Функция для регистрации компонента
void AppendVitalSigns(userver::components::ComponentList& component_list) {
    component_list.Append<VitalSignsServiceComponent>();
}

} // namespace lifeos
