#!/bin/sh
set -eu
docker compose exec -T postgres psql -U "${POSTGRES_USER:-givinity}" -d "${POSTGRES_DB:-shortlink}" -c "REINDEX TABLE tasks; ALTER DATABASE shortlink REFRESH COLLATION VERSION;"
