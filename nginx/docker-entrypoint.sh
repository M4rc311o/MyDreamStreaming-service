#!/usr/bin/env bash
set -Eeuo pipefail

envsubst '${DOMAIN}' < /etc/nginx/templates/nginx.conf.template > /etc/nginx/nginx.conf

exec "$@"