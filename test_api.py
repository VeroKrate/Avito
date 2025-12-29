import pytest
import requests
import random
import time

BASE_URL = "https://qa-internship.avito.com"
API_VERSION = "1"

def generate_seller_id():
    #Генерация уникального sellerID в диапазоне 
    return random.randint(111111, 999999)

def generate_ad_id():
    #Генерация случайного строкового ID для негативных тестов
    return f"test_invalid_{random.randint(10000, 99999)}"

@pytest.fixture
def unique_seller_id():
    #генерация уникального sellerID
    return generate_seller_id()

@pytest.fixture
def created_ad_data(unique_seller_id):
    #создания объявления и возврата его данных
    test_data = {
        "sellerID": unique_seller_id,
        "name": f"Тестовый товар от {unique_seller_id}",
        "price": random.randint(100, 100000),
        "statistics": {
            "likes": random.randint(0, 50),
            "viewCount": random.randint(0, 1000),
            "contacts": random.randint(0, 20)
        }
    }
    
    try:
        response = requests.post(f"{BASE_URL}/api/{API_VERSION}/item", json=test_data, timeout=10)
        # Если API недоступно, пропускаем тест
        if response.status_code != 200:
            pytest.skip(f"API недоступно или вернуло ошибку: {response.status_code}")
        
        created_ad = response.json()
        time.sleep(0.5)  # Пауза для стабилизации данных
        return created_ad
    except requests.exceptions.RequestException:
        pytest.skip("API недоступно, пропускаем тест")

class TestCreateAd:
    # Тестирование создания объявления
    
    def test_create_ad_success(self, unique_seller_id):
        #TC-API-1.1: Успешное создание объявления с валидными данными
        test_data = {
            "sellerID": unique_seller_id,
            "name": "Смартфон Samsung Galaxy S23",
            "price": 75000,
            "statistics": {
                "likes": 42,
                "viewCount": 1000,
                "contacts": 15
            }
        }
        
        response = requests.post(f"{BASE_URL}/api/{API_VERSION}/item", json=test_data, timeout=10)
        print(f"[INFO] Запрос POST /api/{API_VERSION}/item, Ответ: {response.status_code}")
        
        # Проверка результата
        assert response.status_code == 200, f"Ожидался код 200, получен {response.status_code}"
        
        response_json = response.json()
        
        # Проверяем обязательные поля
        assert "id" in response_json, "Поле 'id' отсутствует в ответе"
        assert "sellerId" in response_json, "Поле 'sellerId' отсутствует в ответе"
        assert "name" in response_json, "Поле 'name' отсутствует в ответе"
        assert "price" in response_json, "Поле 'price' отсутствует в ответе"
        assert "createdAt" in response_json, "Поле 'createdAt' отсутствует в ответе"
        assert "statistics" in response_json, "Поле 'statistics' отсутствует в ответе"
        
        # Проверяем значения полей
        assert response_json["sellerId"] == test_data["sellerID"], "Несоответствие sellerId"
        assert response_json["name"] == test_data["name"], "Несоответствие name"
        assert response_json["price"] == test_data["price"], "Несоответствие price"
        
        stats = response_json["statistics"]
        assert stats["likes"] == test_data["statistics"]["likes"], "Несоответствие likes"
        assert stats["viewCount"] == test_data["statistics"]["viewCount"], "Несоответствие viewCount"
        assert stats["contacts"] == test_data["statistics"]["contacts"], "Несоответствие contacts"
    
    def test_create_ad_bad_request(self):
        # TC-API-1.2: Создание объявления с невалидными данными
        response = requests.post(f"{BASE_URL}/api/{API_VERSION}/item", json={}, timeout=10)
        print(f"[INFO] Запрос POST с пустым телом, Ответ: {response.status_code}")
        
        # Проверка результата
        assert response.status_code == 400, f"Ожидался код 400 для невалидного запроса, получен {response.status_code}"

class TestGetAdById:
    # Тестирование получения объявления по ID
    
    def test_get_ad_by_id_success(self, created_ad_data):
        #TC-API-2.1: Успешное получение существующего объявления
        ad_id = created_ad_data["id"]
        response = requests.get(f"{BASE_URL}/api/{API_VERSION}/item/{ad_id}", timeout=10)
        print(f"[INFO] Запрос GET /api/{API_VERSION}/item/{ad_id}, Ответ: {response.status_code}")
        
        # Проверка результата
        assert response.status_code == 200, f"Ожидался код 200, получен {response.status_code}"
        
        response_json = response.json()
        
        # Проверяем, что ответ является массивом
        assert isinstance(response_json, list), "Ответ должен быть массивом"
        assert len(response_json) > 0, "Массив ответа не должен быть пустым"
        
        # Ищем наше объявление в массиве
        found_ad = next((ad for ad in response_json if ad["id"] == ad_id), None)
        assert found_ad is not None, f"Объявление с id {ad_id} не найдено в ответе"
        assert found_ad["sellerId"] == created_ad_data["sellerId"], "Несоответствие sellerId"
        assert found_ad["name"] == created_ad_data["name"], "Несоответствие name"
    
    def test_get_ad_by_id_not_found(self):
        #TC-API-2.2: Запрос несуществующего объявления
        non_existent_id = generate_ad_id()
        response = requests.get(f"{BASE_URL}/api/{API_VERSION}/item/{non_existent_id}", timeout=10)
        print(f"[INFO] Запрос GET с несуществующим ID, Ответ: {response.status_code}")
        
        # Проверка результата
        assert response.status_code == 404, f"Ожидался код 404 для несуществующего ID, получен {response.status_code}"

class TestGetStatistic:
    # Тестирование получения статистики
    
    def test_get_statistic_success(self, created_ad_data):
        #TC-API-3.1: Успешное получение статистики существующего объявления
        ad_id = created_ad_data["id"]
        response = requests.get(f"{BASE_URL}/api/{API_VERSION}/statistic/{ad_id}", timeout=10)
        print(f"[INFO] Запрос GET /api/{API_VERSION}/statistic/{ad_id}, Ответ: {response.status_code}")
        
        # Проверка результата
        assert response.status_code == 200, f"Ожидался код 200, получен {response.status_code}"
        
        stats_list = response.json()
        
        # Проверяем, что ответ является массивом
        assert isinstance(stats_list, list), "Ответ со статистикой должен быть массивом"
        
        # Проверяем структуру первого элемента, если массив не пустой
        if len(stats_list) > 0:
            stat_item = stats_list[0]
            assert "likes" in stat_item, "Поле 'likes' отсутствует в статистике"
            assert "viewCount" in stat_item, "Поле 'viewCount' отсутствует в статистике"
            assert "contacts" in stat_item, "Поле 'contacts' отсутствует в статистике"
    
    def test_get_statistic_not_found(self):
        """TC-API-3.2: Статистика по несуществующему объявлению"""
        non_existent_id = generate_ad_id()
        response = requests.get(f"{BASE_URL}/api/{API_VERSION}/statistic/{non_existent_id}", timeout=10)
        print(f"[INFO] Запрос GET статистики с несуществующим ID, Ответ: {response.status_code}")
        
        # Проверка результата
        assert response.status_code == 404, f"Ожидался код 404, получен {response.status_code}"

if __name__ == "__main__":
    # Запуск тестов напрямую через pytest
    pytest.main([__file__, "-v", "--tb=short"])