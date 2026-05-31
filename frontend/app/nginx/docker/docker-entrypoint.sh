#!/bin/sh
set -eu

DOMAIN_HOST="${DOMAIN#http://}"
DOMAIN_HOST="${DOMAIN_HOST#https://}"
DOMAIN_HOST="${DOMAIN_HOST%%/*}"
export DOMAIN_HOST

if [ -f "/etc/letsencrypt/live/${DOMAIN_HOST}/fullchain.pem" ]; then
  envsubst '${DOMAIN_HOST}' \
    < /etc/nginx/templates/ssl.conf.template \
    > /etc/nginx/conf.d/ssl.conf
  envsubst '${DOMAIN_HOST}' <<EOF > /etc/nginx/conf.d/default.conf
server {
    listen 80;
    server_name ${DOMAIN_HOST};

    location /.well-known/acme-challenge/ {
        root /var/www/certbot;
    }

    location / {
        return 301 https://\$host\$request_uri;
    }
}
EOF
else
  envsubst '${DOMAIN_HOST}' \
    < /etc/nginx/templates/default.conf.template \
    > /etc/nginx/conf.d/default.conf
fi

exec nginx -g 'daemon off;'
