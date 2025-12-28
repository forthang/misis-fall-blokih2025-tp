.PHONY: build clean run-server run-client install-deps

# Установка зависимостей (для Ubuntu/Debian)
install-deps:
	sudo apt update
	sudo apt install -y cmake build-essential libboost-all-dev libyaml-cpp-dev \
		libev-dev libssl-dev libnghttp2-dev libjemalloc-dev \
		protobuf-compiler libgrpc++-dev python3-dev

# Сборка проекта
build:
	mkdir -p build
	cd build && cmake -DCMAKE_BUILD_TYPE=Release .. && make -j$$(nproc)

# Сборка в debug режиме
build-debug:
	mkdir -p build
	cd build && cmake -DCMAKE_BUILD_TYPE=Debug .. && make -j$$(nproc)

# Запуск сервера
run-server: build
	cd build && ./lifeos_grpc_service-server --config ../config.yaml

# Запуск клиента
run-client: build
	cd build && ./lifeos_grpc_service-client

# Очистка
clean:
	rm -rf build

# Быстрая пересборка
rebuild: clean build
