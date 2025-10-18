# PowerShell скрипт для передачи файлов на сервер
# Использование: .\transfer-to-server.ps1

$SERVER = "89.223.67.136"
$USER = "natalia"
$REMOTE_PATH = "/home/natalia/telegram-bot"

Write-Host "====================================================" -ForegroundColor Cyan
Write-Host "  Передача файлов на сервер $SERVER" -ForegroundColor Cyan
Write-Host "====================================================" -ForegroundColor Cyan
Write-Host ""

# Проверка наличия SSH
if (-not (Get-Command ssh -ErrorAction SilentlyContinue)) {
    Write-Host "ОШИБКА: SSH не установлен!" -ForegroundColor Red
    Write-Host "Установите OpenSSH или Git Bash" -ForegroundColor Yellow
    exit 1
}

# Файлы для передачи
$files = @(
    "docker-compose.yml",
    "docker-compose.prod.yml",
    "docker-compose.dev.yml",
    "docker-compose.local.yml",
    "docker-compose.registry.yml",
    "Dockerfile.bot",
    "Dockerfile.api",
    "Dockerfile.frontend",
    "ENV_EXAMPLE.txt",
    ".dockerignore",
    "Makefile",
    "pyproject.toml",
    "uv.lock",
    "alembic.ini",
    "QUICKSTART.md",
    "DEPLOYMENT_GUIDE.md",
    "DOCKER_ORCHESTRATION_README.md",
    "DEPLOY_TO_SERVER.md",
    "DOCKER_SETUP_SUMMARY.md"
)

$folders = @(
    "src",
    "alembic",
    "prompts",
    "secrets"
)

Write-Host "Шаг 1: Создание директории на сервере..." -ForegroundColor Yellow
ssh ${USER}@${SERVER} "mkdir -p $REMOTE_PATH"

Write-Host "Шаг 2: Передача файлов..." -ForegroundColor Yellow
foreach ($file in $files) {
    if (Test-Path $file) {
        Write-Host "  Копирование: $file" -ForegroundColor Green
        scp $file ${USER}@${SERVER}:${REMOTE_PATH}/
    } else {
        Write-Host "  Пропуск (не найден): $file" -ForegroundColor Gray
    }
}

Write-Host "Шаг 3: Передача директорий..." -ForegroundColor Yellow
foreach ($folder in $folders) {
    if (Test-Path $folder) {
        Write-Host "  Копирование: $folder/" -ForegroundColor Green
        scp -r $folder ${USER}@${SERVER}:${REMOTE_PATH}/
    } else {
        Write-Host "  Пропуск (не найден): $folder/" -ForegroundColor Gray
    }
}

Write-Host ""
Write-Host "====================================================" -ForegroundColor Green
Write-Host "  ✓ Передача завершена!" -ForegroundColor Green
Write-Host "====================================================" -ForegroundColor Green
Write-Host ""
Write-Host "Следующие шаги:" -ForegroundColor Cyan
Write-Host "1. Подключитесь к серверу: ssh ${USER}@${SERVER}" -ForegroundColor White
Write-Host "2. Перейдите в директорию: cd $REMOTE_PATH" -ForegroundColor White
Write-Host "3. Создайте .env файл: cp ENV_EXAMPLE.txt .env" -ForegroundColor White
Write-Host "4. Отредактируйте .env: nano .env" -ForegroundColor White
Write-Host "5. Запустите систему: docker compose -f docker-compose.local.yml up -d --build" -ForegroundColor White
Write-Host ""
Write-Host "Подробная инструкция: cat DEPLOY_TO_SERVER.md" -ForegroundColor Yellow
