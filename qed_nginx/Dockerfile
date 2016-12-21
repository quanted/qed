FROM nginx:stable

# Remove default configuration from Nginx
RUN rm /etc/nginx/conf.d/default.conf
# Overwrite the NGINX conf
COPY nginx.conf /etc/nginx/conf.d/
