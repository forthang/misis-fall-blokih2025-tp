#!/usr/bin/env python

from concurrent import futures

import grpc
import typing
import time

# Импортируем сгенерированные классы (убедитесь, что выполнили генерацию)
import metrics_pb2
import metrics_pb2_grpc

class VitalSignsServicer(metrics_pb2_grpc.VitalSignsServiceServicer):
    storage: typing.Any |None = None

    def __init__(self):
        # TODO: Инициализируйте хранилище данных (например, словарь)
        # self.storage = ...
        pass

    def RecordMetric(self, request, context):
        """
        Принимает MetricRequest, сохраняет данные в память.
        Возвращает MetricResponse.
        """
        print(f"[LOG] Received metric: {request.type} = {request.value} for user {request.user_id}")

        # TODO: 1. Проверить валидность данных
        # TODO: 2. Сохранить значение в список для данного пользователя и типа метрики

        return metrics_pb2.MetricResponse(success=True, message="Data saved")

    def GetAverage(self, request, context):
        """
        Принимает AverageRequest, считает среднее.
        Возвращает AverageResponse.
        """
        # TODO: 1. Найти данные пользователя
        # TODO: 2. Вычислить среднее (если данных нет, вернуть 0)

        average = 0.0 # Заглушка
        count = 0     # Заглушка

        return metrics_pb2.AverageResponse(average_value=average, count=count)

def serve():
    port = "50051"
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    metrics_pb2_grpc.add_VitalSignsServiceServicer_to_server(VitalSignsServicer(), server)
    server.add_insecure_port('[::]:' + port)

    print(f"Server started, listening on {port}")

    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    serve()
