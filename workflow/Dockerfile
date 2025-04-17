FROM n8nio/n8n:latest

# Instala curl usando apk (Alpine Linux)
USER root
RUN apk add --no-cache curl

# Cambia de nuevo al usuario n8n
USER node

# Cambiar la ruta de destino para que coincida con la configuración del docker-compose
COPY init_n8n.sh /workflow/init_n8n.sh
COPY entrypoint.sh /workflow/entrypoint.sh


# Usar el script de entrada personalizado
ENTRYPOINT ["/workflow/entrypoint.sh"]