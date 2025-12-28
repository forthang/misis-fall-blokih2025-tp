#include <iostream>
#include <memory>
#include <string>
#include <random>
#include <thread>
#include <chrono>

#include <grpcpp/grpcpp.h>

// Подключаем сгенерированный заголовок
#include <metrics.grpc.pb.h>

using grpc::Channel;
using grpc::ClientContext;
using grpc::Status;
using lifeos::VitalSignsService;
using lifeos::MetricRequest;
using lifeos::MetricResponse;
using lifeos::AverageRequest;
using lifeos::AverageResponse;
using lifeos::MetricType;

class VitalSignsClient {
public:
    VitalSignsClient(std::shared_ptr<Channel> channel)
        : stub_(VitalSignsService::NewStub(channel)) {}

    // Реализация метода отправки метрики
    bool RecordMetric(const std::string& user, MetricType type, double value) {
        MetricRequest request;
        request.set_user_id(user);
        request.set_type(type);
        request.set_value(value);
        request.set_timestamp(std::chrono::duration_cast<std::chrono::seconds>(
            std::chrono::system_clock::now().time_since_epoch()).count());

        MetricResponse response;
        ClientContext context;

        Status status = stub_->RecordMetric(&context, request, &response);

        if (status.ok()) {
            std::cout << "✓ Recorded " << value << " for user " << user << std::endl;
            return response.success();
        } else {
            std::cout << "✗ Failed to record metric: " << status.error_message() << std::endl;
            return false;
        }
    }

    // Реализация метода получения среднего
    void GetAverage(const std::string& user, MetricType type) {
        AverageRequest request;
        request.set_user_id(user);
        request.set_type(type);

        AverageResponse response;
        ClientContext context;

        Status status = stub_->GetAverage(&context, request, &response);

        if (status.ok()) {
            std::cout << "📊 Average for user " << user << ": " 
                      << response.average_value() << " (based on " 
                      << response.count() << " measurements)" << std::endl;
        } else {
            std::cout << "✗ Failed to get average: " << status.error_message() << std::endl;
        }
    }

private:
    std::unique_ptr<VitalSignsService::Stub> stub_;
};

int main(int argc, char** argv) {
    // Создаем канал
    std::string target_str = "localhost:50051";
    VitalSignsClient client(grpc::CreateChannel(
        target_str, grpc::InsecureChannelCredentials()));

    std::string user_id = "student_cpp";

    std::cout << "=== gRPC Vital Signs Client Demo ===" << std::endl;
    std::cout << "Sending metrics for " << user_id << "..." << std::endl;

    // Генератор случайных чисел
    std::random_device rd;
    std::mt19937 gen(rd());
    std::uniform_real_distribution<> heart_rate_dist(60.0, 100.0);
    std::uniform_real_distribution<> stress_dist(0.0, 100.0);

    // Отправляем несколько измерений пульса
    std::cout << "\n1. Recording heart rate measurements:" << std::endl;
    for (int i = 0; i < 7; ++i) {
        double heart_rate = heart_rate_dist(gen);
        client.RecordMetric(user_id, MetricType::HEART_RATE, heart_rate);
        std::this_thread::sleep_for(std::chrono::milliseconds(100));
    }

    // Отправляем несколько измерений стресса
    std::cout << "\n2. Recording stress level measurements:" << std::endl;
    for (int i = 0; i < 5; ++i) {
        double stress = stress_dist(gen);
        client.RecordMetric(user_id, MetricType::STRESS_LEVEL, stress);
        std::this_thread::sleep_for(std::chrono::milliseconds(100));
    }

    // Получаем средние значения
    std::cout << "\n3. Getting averages:" << std::endl;
    client.GetAverage(user_id, MetricType::HEART_RATE);
    client.GetAverage(user_id, MetricType::STRESS_LEVEL);

    // Тестируем с другим пользователем
    std::cout << "\n4. Testing with another user:" << std::endl;
    std::string user2 = "test_user_2";
    client.RecordMetric(user2, MetricType::HEART_RATE, 85.5);
    client.RecordMetric(user2, MetricType::HEART_RATE, 90.2);
    client.GetAverage(user2, MetricType::HEART_RATE);

    std::cout << "\n=== Demo completed ===" << std::endl;
    return 0;
}
