FROM nginx:1.13-alpine
RUN rm /etc/nginx/conf.d/default.conf

# Note that this considers that the context is at: ../../
# this dockerfile is located at: docker/proxy/
COPY docker/proxy/nginx.conf /etc/nginx/nginx.conf
COPY src/restapi/static usr/src/app/src/restapi/static
