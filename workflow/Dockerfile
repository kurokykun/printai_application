FROM n8nio/n8n:latest

USER root
RUN apk add --no-cache curl

# Copiar solo el entrypoint actualizado
COPY entrypoint.sh /usr/local/bin/entrypoint.sh
RUN chmod +x /usr/local/bin/entrypoint.sh
USER node
ENTRYPOINT ["entrypoint.sh"]