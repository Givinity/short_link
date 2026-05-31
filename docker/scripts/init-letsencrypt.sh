#!/bin/sh
# Первый выпуск сертификата (прод, домен указывает на сервер):
#   ./docker/scripts/init-letsencrypt.sh your-domain.com you@example.com
set -eu

DOMAIN="${1:?usage: init-letsencrypt.sh <domain> <email>}"
EMAIL="${2:?usage: init-letsencrypt.sh <domain> <email>}"

cd "$(dirname "$0")/../.."

docker compose up -d frontend

docker compose run --rm certbot certonly \
  --webroot \
  -w /var/www/certbot \
  -d "$DOMAIN" \
  --email "$EMAIL" \
  --agree-tos \
  --no-eff-email \
  --force-renewal

docker compose restart frontend
echo "Готово. Проверьте https://${DOMAIN}/"
