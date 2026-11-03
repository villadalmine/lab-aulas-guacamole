#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
command -v docker >/dev/null
docker compose version >/dev/null
umask 077
mkdir -p initdb backups
if [[ ! -f .env ]]; then
  cp .env.example .env
  python3 - <<'PY'
from pathlib import Path
import secrets
p=Path('.env');s=p.read_text()
for key in ('POSTGRES_PASSWORD','DESKTOP_PASSWORD','GRAFANA_PASSWORD'):
 s=s.replace(key+'=cambiar_con_preparar',key+'='+secrets.token_hex(24))
p.write_text(s)
PY
fi
# No regenerar ni truncar el esquema de una base ya iniciada.
if [[ ! -s initdb/001-guacamole.sql ]]; then
  version=$(sed -n 's/^GUACAMOLE_VERSION=//p' .env)
  docker run --rm "guacamole/guacamole:${version}" /opt/guacamole/bin/initdb.sh --postgresql > initdb/001-guacamole.sql.tmp
  test -s initdb/001-guacamole.sql.tmp
  mv initdb/001-guacamole.sql.tmp initdb/001-guacamole.sql
fi
docker compose config --quiet
printf 'Preparado. Ejecutar: docker compose --profile escritorio up -d --build\n'
