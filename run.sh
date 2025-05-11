#!/usr/bin/env bash

set -e  # Fail on first error

COMPOSE_FILE="docker-compose.yml"
IMAGE_NAME="fastapi-otel-app"
SERVICE_NAME="fastapi-otel"
CONTAINERS=("fastapi-otel")

echo "📦 Cloning SigNoz repository (if needed)..."
if [ ! -d "signoz" ]; then
  git clone https://github.com/SigNoz/signoz.git
else
  echo "✅ 'signoz' directory already exists."
fi

echo "🚀 Starting SigNoz stack..."
cd signoz/deploy/docker
docker compose up -d
cd ../../..

echo "🧹 Removing old containers from the project..."
for NAME in "${CONTAINERS[@]}"; do
  if docker ps -a --format '{{.Names}}' | grep -q "^${NAME}\$"; then
    echo "⛔ Stopping and removing container: $NAME"
    docker rm -f "$NAME"
  else
    echo "✅ Container $NAME is not running."
  fi
done

# List of images to remove
IMAGES=("fastapi-otel-app-fastapi-otel")

echo "🧹 Removing old images..."
for IMAGE in "${IMAGES[@]}"; do
  if docker images --format '{{.Repository}}:{{.Tag}}' | grep -q "^${IMAGE}:latest\$"; then
    echo "🗑️  Removing image: $IMAGE:latest"
    docker rmi -f "${IMAGE}:latest"
  else
    echo "✅ Image $IMAGE:latest not found."
  fi
done

echo "🔧 Building custom Docker image: $IMAGE_NAME"
docker compose -f $COMPOSE_FILE build $SERVICE_NAME

echo "🧹 Stopping old containers if any"
docker compose -f $COMPOSE_FILE down --remove-orphans

echo "🚀 Starting current project services"
docker compose -f $COMPOSE_FILE up -d

echo "✅ All set!"
echo "🌐 FastAPI available at: http://localhost:8000"
echo "📊 SigNoz available at: http://localhost:3301"
