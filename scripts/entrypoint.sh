#!/bin/bash
set -e
cd /app

wait_for_db() {
  echo "Waiting for database to be ready"
  python << END
import socket
import time
import os

db_host = os.getenv("POSTGRES__HOST", "database")
db_port = int(os.getenv("POSTGRES__PORT", 5432))

while True:
    try:
        with socket.create_connection((db_host, db_port), timeout=1):
            print("Database is up!")
            break
    except OSError:
        print("Database is unavailable - sleeping")
        time.sleep(1)
END
}

wait_for_db


echo "Running migrations"
alembic -c backend/kanban/alembic.ini upgrade head

echo "Starting application"
exec "$@"