#!/bin/sh

# Iniciar n8n en segundo plano
n8n &

# Esperar a que n8n esté completamente levantado
echo "Esperando a que n8n esté listo..."
MAX_RETRIES=30
RETRY_COUNT=0

while ! curl -s http://localhost:5678/api/v1/workflows > /dev/null; do
  RETRY_COUNT=$((RETRY_COUNT + 1))
  if [ "$RETRY_COUNT" -ge "$MAX_RETRIES" ]; then
    echo "n8n no está listo después de $MAX_RETRIES intentos. Abortando."
    exit 1
  fi
  echo "Intento $RETRY_COUNT/$MAX_RETRIES: n8n no está listo. Reintentando en 5 segundos..."
  sleep 5
done

# Importar el workflow
echo "n8n está listo. Importando workflow..."
curl -X POST http://localhost:5678/rest/workflows \
  -H "Content-Type: application/json" \
  -u admin:admin \
  -d @/home/node/.n8n/workflows.json

# Mantener el contenedor corriendo
wait
