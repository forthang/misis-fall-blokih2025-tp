import os
import sys
import time
import subprocess
import grpc
import random
from concurrent import futures

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
PROTO_PATH = os.path.join(PROJECT_ROOT, 'proto')
PYTHON_OUT = os.path.join(PROJECT_ROOT, 'tests', 'generated')

os.makedirs(PYTHON_OUT, exist_ok=True)

def generate_proto():
    print(f"[*] Generating proto code for testing from {PROTO_PATH}...")
    cmd = [
        sys.executable, "-m", "grpc_tools.protoc",
        f"-I{PROTO_PATH}",
        f"--python_out={PYTHON_OUT}",
        f"--grpc_python_out={PYTHON_OUT}",
        os.path.join(PROTO_PATH, "metrics.proto")
    ]
    subprocess.check_call(cmd)
    sys.path.append(PYTHON_OUT)

def is_python_track():
    server_path = os.path.join(PROJECT_ROOT, 'python', 'custom_service', 'server.py')
    if not os.path.exists(server_path):
        return False
    return os.path.getsize(server_path) > 0

def is_cpp_track():
    service_path = os.path.join(PROJECT_ROOT, 'cpp', 'src', 'service.cpp')
    return os.path.exists(service_path) and os.path.getsize(service_path) > 500

def run_integration_test(port=50051):
    import metrics_pb2
    import metrics_pb2_grpc

    print(f"[*] Connecting to server on localhost:{port}...")
    channel = grpc.insecure_channel(f'localhost:{port}')
    stub = metrics_pb2_grpc.VitalSignsServiceStub(channel)

    try:
        grpc.channel_ready_future(channel).result(timeout=10)
    except grpc.FutureTimeoutError:
        print("[!] Connection timed out. Server did not start.")
        return False

    try:
        user_id = "test_user_1"

        print("[*] Sending metrics...")
        values = [60, 70, 80, 90, 100]
        for val in values:
            stub.RecordMetric(metrics_pb2.MetricRequest(
                user_id=user_id,
                type=metrics_pb2.HEART_RATE,
                value=val,
                timestamp=int(time.time())
            ))

        print("[*] Requesting average...")
        response = stub.GetAverage(metrics_pb2.AverageRequest(
            user_id=user_id,
            type=metrics_pb2.HEART_RATE
        ))

        expected_avg = sum(values) / len(values)
        print(f"[*] Got: {response.average_value}, Expected: {expected_avg}")

        if abs(response.average_value - expected_avg) < 0.01:
            print("[+] Test PASSED!")
            return True
        else:
            print("[-] Test FAILED: Wrong average calculation.")
            return False

    except grpc.RpcError as e:
        print(f"[!] RPC Error: {e}")
        return False

def main():
    generate_proto()

    server_process = None

    try:
        if is_cpp_track() and not os.environ.get("FORCE_PYTHON"):
            print("=== Detected C++ Track ===")
            build_dir = os.path.join(PROJECT_ROOT, 'cpp', 'build')
            os.makedirs(build_dir, exist_ok=True)

            print("[*] Running CMake...")
            subprocess.check_call(['cmake', '-DCMAKE_BUILD_TYPE=Debug', '..'], cwd=build_dir)

            print("[*] Compiling (this may take time)...")
            subprocess.check_call(['make', '-j', '2'], cwd=build_dir)

            print("[*] Starting C++ Server...")
            exe_path = os.path.join(build_dir, 'lifeos_grpc_service-server')
            config_path = os.path.join(PROJECT_ROOT, 'cpp', 'config.yaml')

            server_process = subprocess.Popen([exe_path, '--config', config_path])

        elif is_python_track():
            print("=== Detected Python Track ===")
            print("[*] Installing package...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", "-e", "."], cwd=os.path.join(PROJECT_ROOT, 'python'))

            print("[*] Starting Python Server...")
            server_process = subprocess.Popen(
                [sys.executable, "-m", "custom_service.server"],
                cwd=os.path.join(PROJECT_ROOT, 'python')
            )

        else:
            print("[!] Neither Python nor C++ solution detected (files are empty or missing).")
            sys.exit(1)

        time.sleep(5)

        success = run_integration_test()

        if not success:
            sys.exit(1)

    except subprocess.CalledProcessError as e:
        print(f"[!] Build/Setup failed: {e}")
        sys.exit(1)
    finally:
        if server_process:
            print("[*] Stopping server...")
            server_process.terminate()
            server_process.wait()

if __name__ == "__main__":
    main()
