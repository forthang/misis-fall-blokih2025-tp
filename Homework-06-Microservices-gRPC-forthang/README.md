# HW-06: Life OS | Vital Signs Service (gRPC)

![Points](../../blob/badges/.github/badges/points.svg)

**Дедлайн:** 3 недели.
**Технологии:** Python (grpcio) **ИЛИ** C++ (userver).

## 1. Легенда и Контекст
Вы развиваете экосистему **Life OS**. Для функции мониторинга здоровья в реальном времени (пульс во время бега, уровень стресса) использование REST API неэффективно из-за накладных расходов HTTP/1.1.

**Ваша задача:** Разработать микросервис **Metric Collector** на базе протокола **gRPC** (HTTP/2 + Protobuf). Сервис должен принимать поток данных от биосенсоров и отдавать агрегированную статистику.

## 2. Структура проекта

Мы подготовили для вас каркас приложения. Выберите `python` или `cpp` для реализации.

```text
hw-06-grpc/
├── proto/
│   └── metrics.proto          # Контракт сервиса (уже описан)
├── python/                    # ТРЕК A: Python
│   ├── pyproject.toml         # Конфигурация сборки и зависимостей
│   └── custom_service/
│       ├── __init__.py
│       ├── client.py          # Скрипт клиента (нужно дописать)
│       └── server.py          # Сервер gRPC (нужно дописать)
└── cpp/                       # ТРЕК B: C++ (Userver)
    ├── CMakeLists.txt         # Сборка + скачивание userver
    ├── config.yaml            # Конфиг запуска сервиса
    └── src/
        ├── main.cpp           # Точка входа
        └── service.cpp        # Реализация сервиса (нужно дописать)
```

---

## 3. Задание

### Шаг 1: Изучите контракт (`proto/metrics.proto`)
В файле уже описаны методы:
1.  `RecordMetric` — принимает `MetricRequest` (user_id, type, value), сохраняет метрику.
2.  `GetAverage` — принимает `AverageRequest`, возвращает среднее значение метрики.

### Шаг 2: Реализуйте Сервер
Вам нужно написать логику методов `RecordMetric` и `GetAverage`.
*   Данные храните в памяти (in-memory словарь/map).
*   **Логика:** При запросе `GetAverage` нужно найти все метрики указанного типа для пользователя и вернуть их среднее арифметическое.

### Шаг 3: Реализуйте Клиент
Напишите скрипт, который:
1.  Генерирует 5-10 случайных значений пульса (HEART_RATE).
2.  Отправляет их на сервер по gRPC.
3.  Запрашивает среднее значение и выводит его в консоль.

---

## 4. Инструкция: Python Track

Для работы требуется Python 3.9+.

### Установка и Генерация
Мы используем `pyproject.toml` для управления зависимостями.

1.  **Установка пакета в режиме разработки:**
    ```bash
    cd python
    pip install -e .
    ```
    *Это установит `grpcio`, `protobuf` и сам ваш пакет `lifeos_grpc_service`.*

2.  **Генерация кода из Proto:**
    Находясь в папке `python`, выполните:
    ```bash
    python -m grpc_tools.protoc -I../proto --python_out=./custom_service --grpc_python_out=./custom_service ../proto/metrics.proto
    ```
    *В папке `custom_service` появятся файлы `metrics_pb2.py` и `metrics_pb2_grpc.py`.*

### Запуск
1.  **Сервер:**
    ```bash
    python -m custom_service.server
    ```
2.  **Клиент (в новом терминале):**
    ```bash
    python -m custom_service.client
    ```

---

## 5. Инструкция: C++ Track (Userver)

Этот трек для тех, кто хочет максимальной производительности. Используется фреймворк **userver** от Яндекс.

> **Важно:** Сборка работает только на **Linux** или **WSL2** (Windows Subsystem for Linux). Нативная сборка под Windows через MSVC не поддерживается.

### Подготовка (Ubuntu/Debian)
Установите системные зависимости (компиляторы, cmake, python3 для скриптов userver):
```bash
sudo apt update
sudo apt install -y cmake build-essential libboost-all-dev libyaml-cpp-dev \
    libev-dev libssl-dev libnghttp2-dev libjemalloc-dev \
    protobuf-compiler grpc-compiler python3-dev
```

### Сборка
Userver будет скачан автоматически при первом запуске cmake (это займет время).

```bash
cd cpp
mkdir build && cd build

# Конфигурация проекта (скачивание userver)
cmake -DCMAKE_BUILD_TYPE=Debug ..

# Компиляция (используем все ядра процессора)
make -j $(nproc)
```

### Запуск
После успешной сборки в папке `build` появится исполняемый файл. Ему нужно передать конфиг.

```bash
# Запуск сервера
./lifeos_grpc_service-server --config ../config.yaml
```

Для проверки клиента (если вы не писали C++ клиент) можно использовать Python-клиент из соседней папки, так как gRPC — это кросс-языковой протокол!

---


## Полезные ссылки
*   [gRPC Python Quickstart](https://grpc.io/docs/languages/python/quickstart/)
*   [Userver gRPC Service Tutorial](https://userver.tech/de/d6a/md_en_2index.html)
*   [Protocol Buffers Guide](https://protobuf.dev/programming-guides/proto3/)
