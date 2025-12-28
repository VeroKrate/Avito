#!/usr/bin/env python3

# Скрипт для запуска тестов API Avito


import subprocess
import sys
import os

def run_tests():
    #Запускает тесты проекта
    
    print("=" * 60)
    print("Запуск тестов API микросервиса объявлений Avito")
    print("=" * 60)
    
    # Проверяем зависимости
    print("\n🔍 Проверка зависимостей...")
    try:
        import pytest
        import requests
        print(f"✅ pytest {pytest.__version__}")
        print(f"✅ requests {requests.__version__}")
    except ImportError:
        print("❌ Зависимости не установлены")
        print("Установите: pip install -r requirements.txt")
        return 1
    
    # Запускаем тесты
    print("\n🚀 Запуск тестов...")
    print("-" * 60)
    
    # Команда для запуска pytest
    cmd = [
        sys.executable, "-m", "pytest",
        "test_api.py",
        "-v",
        "--tb=short",
        "--color=yes"
    ]
    
    result = subprocess.run(cmd)
    
    print("-" * 60)
    if result.returncode == 0:
        print("✅ Все тесты пройдены успешно!")
    else:
        print("❌ Некоторые тесты не пройдены")
    
    return result.returncode

if __name__ == "__main__":
    sys.exit(run_tests())