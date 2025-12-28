import logging
import random
import time

import grpc

# Импортируем сгенерированные файлы.
# Обратите внимание: в Python при запуске модуля как пакета (python -m ...)
# импорты должны быть относительными или через имя пакета.
from custom_service import metrics_pb2
from custom_service import metrics_pb2_grpc

def run():
    # Адрес сервера. Если вы запускаете C++ сервер, порт тот же (50051).
    server_address = 'localhost:50051'

    print(f"Connecting to server at {server_address}...")

    # Создаем небезопасный канал (без SSL)
    # with grpc.insecure_channel(server_address) as channel:
    #     stub = metrics_pb2_grpc.VitalSignsServiceStub(channel)
    #
    #     TODO: 1. Сгенерируйте 5-10 значений пульса (HEART_RATE)
    #     TODO: 2. В цикле отправьте их через stub.RecordMetric
    #     TODO: 3. Вызовите stub.GetAverage и выведите результат в консоль

    print("Client implementation is missing! See client.py to fix this.")

if __name__ == '__main__':
    logging.basicConfig()
    run()
