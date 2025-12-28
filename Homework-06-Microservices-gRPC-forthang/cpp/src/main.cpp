#include <userver/components/minimal_server_component_list.hpp>
#include <userver/ugrpc/server/server_component.hpp>
#include <userver/utils/daemon_run.hpp>

// Подключаем наш сервис
namespace lifeos {
    void AppendVitalSigns(userver::components::ComponentList& component_list);
}

int main(int argc, char* argv[]) {
    // Список стандартных компонентов (логгер, конфиг и т.д.)
    auto component_list = userver::components::MinimalServerComponentList()
                              .Append<userver::ugrpc::server::ServerComponent>();

    // Добавляем наш gRPC сервис
    lifeos::AppendVitalSigns(component_list);

    return userver::utils::DaemonMain(argc, argv, component_list);
}
