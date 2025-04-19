#!/bin/sh

if [ -f /home/node/.n8n/credentials.json ]; then
  n8n import:credentials --input /home/node/.n8n/credentials.json || true
fi

n8n import:workflow --input /home/node/.n8n/workflows.json || true

echo "Activando workflows importados..."
n8n update:workflow --all --active=true || true

exec n8n
