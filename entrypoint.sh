#!/bin/sh

set -e

 until pg_isready -h "$PG_HOST" -p "$PG_PORT"; do
       echo "Waiting for database..."
       sleep 2
     done

echo "Running Alembic migrations..."
alembic upgrade head
echo "Alembic migrations complete."

exec "$@"
