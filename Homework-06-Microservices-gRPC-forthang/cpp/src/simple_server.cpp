#include <grpcpp/grpcpp.h>
#include <memory>
#include <string>
#include <unordered_map>
#include <vector>
#include <mutex>
#include <numeric>
#include <iostream>

#include "metrics.grpc.pb.h"

using grpc::Server;
using grpc::ServerBuilder;
using grpc::ServerContext;
using grpc::Status;
using lifeos::VitalSignsService;
using lifeos::MetricRequest;
using lifeos::MetricResponse;
using lifeos::AverageRequest;
using lifeos::AverageResponse;
using lifeos::MetricType;

class VitalSignsServiceImpl final : public VitalSignsService::Service {
public:
    Status RecordMetric(ServerContext* context, const MetricRequest* request,
                       MetricResponse* response) override {
        std::lock_guard<std::mutex> lock(mutex_);
        
        // Создаем ключ для хранения: user_id + type
        std::string key = request->user_id() + "_" + std::to_string(static_cast<int>(request->type()));
        
        // Сохраняем значение
        metrics_[key].push_back(request->value());
        
        response->set_success(true);
        response->set_message("Metric recorded successfully");
        
        std::cout << "Recorded metric: " << request->value() 
                  << " for user " << request->user_id() 
                  << " type " << request->type() << std::endl;
        
        return Status::OK;
    }

    Status GetAverage(ServerContext* context, const AverageRequest* request,
                     AverageResponse* response) override {
        std::lock_guard<std::mutex> lock(mutex_);
        
        std::string key = request->user_id() + "_" + std::to_string(static_cast<int>(request->type()));
        
        auto it = metrics_.find(key);
        if (it != metrics_.end() && !it->second.empty()) {
            const auto& values = it->second;
            double sum = std::accumulate(values.begin(), values.end(), 0.0);
            double average = sum / values.size();
            
            response->set_average_value(average);
            response->set_count(static_cast<int32_t>(values.size()));
            
            std::cout << "Calculated average: " << average 
                      << " from " << values.size() << " measurements"
                      << " for user " << request->user_id() << std::endl;
        } else {
            response->set_average_value(0.0);
            response->set_count(0);
            
            std::cout << "No data found for user " << request->user_id() 
                      << " type " << request->type() << std::endl;
        }
        
        return Status::OK;
    }

private:
    // In-memory хранилище: ключ -> список значений
    std::unordered_map<std::string, std::vector<double>> metrics_;
    std::mutex mutex_;
};

void RunServer() {
    std::string server_address("0.0.0.0:50051");
    VitalSignsServiceImpl service;

    ServerBuilder builder;
    builder.AddListeningPort(server_address, grpc::InsecureServerCredentials());
    builder.RegisterService(&service);
    
    std::unique_ptr<Server> server(builder.BuildAndStart());
    std::cout << "Server listening on " << server_address << std::endl;

    server->Wait();
}

int main(int argc, char** argv) {
    RunServer();
    return 0;
}
