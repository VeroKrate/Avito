@echo off
echo Установка зависимостей...
pip install -r requirements.txt
echo.
echo Запуск тестов...
pytest test_api.py -v
echo.
pause