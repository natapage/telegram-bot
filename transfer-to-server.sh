#!/bin/bash
# Bash скрипт для передачи файлов на сервер
# Использование: ./transfer-to-server.sh

SERVER="89.223.67.136"
USER="natalia"
REMOTE_PATH="/home/natalia/telegram-bot"

echo "===================================================="
echo "  Передача файлов на сервер $SERVER"
echo "===================================================="
echo ""

# Проверка наличия SSH
if ! command -v ssh &> /dev/null; then
    echo "ОШИБКА: SSH не установлен!"
    exit 1
fi

# Файлы для передачи
files=(
    "docker-compose.yml"
    "docker-compose.prod.yml"
    "docker-compose.dev.yml"
    "docker-compose.local.yml"
    "docker-compose.registry.yml"
    "Dockerfile.bot"
    "Dockerfile.api"
    "Dockerfile.frontend"
    "ENV_EXAMPLE.txt"
    ".dockerignore"
    "Makefile"
    "pyproject.toml"
    "uv.lock"
    "alembic.ini"
    "QUICKSTART.md"
    "DEPLOYMENT_GUIDE.md"
    "DOCKER_ORCHESTRATION_README.md"
    "DEPLOY_TO_SERVER.md"
    "DOCKER_SETUP_SUMMARY.md"
)

folders=(
    "src"
    "alembic"
    "prompts"
    "secrets"
)

echo "Шаг 1: Создание директории на сервере..."
ssh ${USER}@${SERVER} "mkdir -p $REMOTE_PATH"

echo "Шаг 2: Передача файлов..."
for file in "${files[@]}"; do
    if [ -f "$file" ]; then
        echo "  Копирование: $file"
        scp "$file" ${USER}@${SERVER}:${REMOTE_PATH}/
    else
        echo "  Пропуск (не найден): $file"
    fi
done

echo "Шаг 3: Передача директорий..."
for folder in "${folders[@]}"; do
    if [ -d "$folder" ]; then
        echo "  Копирование: $folder/"
        scp -r "$folder" ${USER}@${SERVER}:${REMOTE_PATH}/
    else
        echo "  Пропуск (не найден): $folder/"
    fi
done

echo ""
echo "===================================================="
echo "  ✓ Передача завершена!"
echo "===================================================="
echo ""
echo "Следующие шаги:"
echo "1. Подключитесь к серверу: ssh ${USER}@${SERVER}"
echo "2. Перейдите в директорию: cd $REMOTE_PATH"
echo "3. Создайте .env файл: cp ENV_EXAMPLE.txt .env"
echo "4. Отредактируйте .env: nano .env"
echo "5. Запустите систему: docker compose -f docker-compose.local.yml up -d --build"
echo ""
echo "Подробная инструкция: cat DEPLOY_TO_SERVER.md"
