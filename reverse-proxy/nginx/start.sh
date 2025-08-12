#!/bin/sh
set -e

CONF_DIR="/etc/nginx/conf.d"
ROUTES="/etc/nginx/routes.map"
TPL_HTTP="/etc/nginx/templates/vhost.http.tmpl"
TPL_HTTPS="/etc/nginx/templates/vhost.https.tmpl"

# Ensure conf dir exists and clear old vhosts (but keep common file)
mkdir -p "$CONF_DIR"
find "$CONF_DIR" -maxdepth 1 -type f -name '*.conf' ! -name '00_http_common.conf' -delete

if [ ! -f "$ROUTES" ]; then
  echo "[start] routes.map not found at $ROUTES"
  exit 1
fi

while IFS= read -r line; do
  # Skip blanks/comments
  [ -z "$line" ] && continue
  echo "$line" | grep -q '^[[:space:]]*#' && continue

  DOMAIN="$(echo "$line" | cut -d= -f1 | tr -d ' ')"
  UPSTREAM="$(echo "$line" | cut -d= -f2 | tr -d ' ')"

  [ -z "$DOMAIN" ] || [ -z "$UPSTREAM" ] && {
    echo "[start] invalid line in routes.map: $line"
    continue
  }

  CERT_DIR="/etc/letsencrypt/live/${DOMAIN}"
  OUT="${CONF_DIR}/${DOMAIN}.conf"

  if [ -f "${CERT_DIR}/fullchain.pem" ] && [ -f "${CERT_DIR}/privkey.pem" ]; then
    echo "[start] ${DOMAIN}: certs found → HTTPS"
    sed -e "s/__DOMAIN__/${DOMAIN}/g" \
        -e "s#__UPSTREAM__#${UPSTREAM}#g" \
        "$TPL_HTTPS" > "$OUT"
  else
    echo "[start] ${DOMAIN}: no cert yet → HTTP only"
    sed -e "s/__DOMAIN__/${DOMAIN}/g" \
        -e "s#__UPSTREAM__#${UPSTREAM}#g" \
        "$TPL_HTTP" > "$OUT"
  fi
done < "$ROUTES"

# Validate and run
nginx -t
exec nginx -g 'daemon off;'