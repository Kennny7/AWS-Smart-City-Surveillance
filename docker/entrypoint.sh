#!/usr/bin/env bash

# Exit immediately if a command exits with a non-zero status
set -e

# =======================
# 1. BOOTSTRAP OR INIT
# =======================
echo "Performing container initialization..."

# Example: Environment variable setup, waiting for dependencies, etc.
# Uncomment if needed:
# echo "Waiting for Kafka on host: $KAFKA_HOST..."
# sleep 5  # Simulate wait

# =======================
# 2. Debugging Information
# =======================
echo "Starting the app..."

# =======================
# 3. EXECUTE ORIGINAL CMD
# =======================
# Pass arguments from CMD in the Dockerfile (or docker-compose)
if [[ $# -eq 0 ]]; then
  # If no CMD args are passed, default to running the app
  exec python src/web_dashboard/app.py
else
  # If CMD args exist, execute them
  exec "$@"
fi
