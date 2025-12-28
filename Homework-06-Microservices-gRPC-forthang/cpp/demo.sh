#!/bin/bash

echo "=== gRPC Vital Signs Service Demo ==="
echo

cd build

echo "1. Starting gRPC server..."
./grpc_server > server.log 2>&1 &
SERVER_PID=$!
echo "   Server started with PID: $SERVER_PID"

echo "2. Waiting for server to initialize..."
sleep 2

echo "3. Running client demo..."
echo
./grpc_client

echo
echo "4. Server log output:"
echo "-------------------"
cat server.log

echo
echo "5. Stopping server..."
kill $SERVER_PID 2>/dev/null
wait $SERVER_PID 2>/dev/null

echo "=== Demo completed ==="
