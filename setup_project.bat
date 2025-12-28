@echo off
echo Настройка проекта тестирования API Avito
echo.

echo 1. Проверка Git...
git --version
if errorlevel 1 (
    echo Git не установлен. Скачайте с https://git-scm.com/
    pause
    exit /b 1
)

echo 2. Проверка Python...
python --version
if errorlevel 1 (
    echo Python не установлен. Скачайте с https://python.org/
    pause
    exit /b 1
)

echo 3. Установка зависимостей...
pip install -r requirements.txt

echo 4. Инициализация Git...
git init
git add .
git commit -m "Initial commit: Тесты API Avito"

echo.
echo Проект настроен!
echo.
echo Команды для запуска:
echo   python run_tests.py     - запуск тестов
echo   python -m pytest -v     - запуск через pytest
echo.
pause