#!/bin/bash

echo "Iniciando el servidor..."
poetry run uvicorn app.main:app --host 0.0.0.0 --port 7013 &

echo "Esperando a que el backend esté listo..."
while ! curl -s http://backend:7013/health > /dev/null; do
  echo "Server is not ready retry in 2 seconds..."
  sleep 2
done


echo "callling the endpoint /init..."
curl -X POST http://localhost:7013/init

wait