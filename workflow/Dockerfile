FROM n8nio/n8n:latest

USER root
RUN apk add --no-cache curl

# Keep running as root to set up scripts
 COPY init_n8n.sh /workflow/init_n8n.sh
 COPY entrypoint.sh /usr/local/bin/entrypoint.sh
 RUN chmod +x /usr/local/bin/entrypoint.sh /workflow/init_n8n.sh
USER node
ENTRYPOINT ["entrypoint.sh"]