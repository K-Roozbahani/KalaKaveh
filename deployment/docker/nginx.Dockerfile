# ------------------------------
# Base Image
# ------------------------------
FROM nginx:1.28-alpine

# ------------------------------
# Remove Default Configuration
# ------------------------------
RUN rm -f /etc/nginx/conf.d/default.conf

# ------------------------------
# Copy Nginx Configuration
# ------------------------------
COPY deployment/nginx/nginx.conf /etc/nginx/nginx.conf

COPY deployment/nginx/conf.d/ /etc/nginx/conf.d/

# ------------------------------
# Expose Port
# ------------------------------
EXPOSE 80

# ------------------------------
# Default Command
# ------------------------------
CMD ["nginx", "-g", "daemon off;"]