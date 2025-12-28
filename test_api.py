import pytest
import requests
import random
import time # подключения

BASE_URL = "https://qa-internship.avito.com" # полученый для тестирования URL
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
    #создание объявления и возврата его данных
    test_data = {
        "sellerID": unique_seller_id, # уникальный id
        "name": f"Тестовый товар от {unique_seller_id}", # название
        "price": random.randint(100, 100000), # цена
        "statistics": { #статистика объявления
            "likes": random.randint(0, 50), # отметки нравится
            "viewCount": random.randint(0, 1000), # просмотры
            "contacts": random.randint(0, 20) #контакты
        }
    }
    
    response = requests.post(f"{BASE_URL}/api/{API_VERSION}/item", json=test_data) # создание объявления
    assert response.status_code == 200, f"Не удалось создать объявление: {response.status_code}" 
     # успешно созданое объявление вернется с коом 200, иначе ошибка
    created_ad = response.json()
    time.sleep(0.5)
    return created_ad

class TestCreateAd:
    #Тестирование создания объявления
    
    def test_create_ad_success(self, unique_seller_id):
        #Успешное создание объявления
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
        
        response = requests.post(f"{BASE_URL}/api/{API_VERSION}/item", json=test_data)
        print(f"[DEBUG] POST /api/{API_VERSION}/item, Status: {response.status_code}")
        
        assert response.status_code == 200, f"Ожидался код 200, получен {response.status_code}"
        response_json = response.json()
        
        # Проверяем обязательные поля
        assert "id" in response_json, "Поле 'id' отсутствует в ответе"
        assert response_json["sellerId"] == test_data["sellerID"], f"Несоответствие sellerId: {response_json['sellerId']} != {test_data['sellerID']}" # проверка id
        assert response_json["name"] == test_data["name"], f"Несоответствие name: {response_json['name']} != {test_data['name']}" # проверка названия 
        assert response_json["price"] == test_data["price"], f"Несоответствие price: {response_json['price']} != {test_data['price']}" # проверка цены
        assert "createdAt" in response_json, "Поле 'createdAt' отсутствует в ответе"
        
        # Проверяем statistics
        assert "statistics" in response_json, "Поле 'statistics' отсутствует в ответе"
        stats = response_json["statistics"]
        assert stats["likes"] == test_data["statistics"]["likes"], f"Несоответствие likes: {stats['likes']} != {test_data['statistics']['likes']}" #проверка отметок нравится
        assert stats["viewCount"] == test_data["statistics"]["viewCount"], f"Несоответствие viewCount: {stats['viewCount']} != {test_data['statistics']['viewCount']}" #проверка просмотров
        assert stats["contacts"] == test_data["statistics"]["contacts"], f"Несоответствие contacts: {stats['contacts']} != {test_data['statistics']['contacts']}" # проверка котактов
    
    def test_create_ad_bad_request(self):
        #Создание с невалидным телом Bad Request
        response = requests.post(f"{BASE_URL}/api/{API_VERSION}/item", json={}) # создание невалидного тела
        print(f"[DEBUG] POST с пустым телом, Status: {response.status_code}")
        assert response.status_code == 400, f"Ожидался код 400, получен {response.status_code}"

class TestGetAdById:
    #Тестирование получения объявления по ID
    
    def test_get_ad_by_id_success(self, created_ad_data):
        #Успешное получение существующего объявления
        ad_id = created_ad_data["id"]
        response = requests.get(f"{BASE_URL}/api/{API_VERSION}/item/{ad_id}") # находим и получаем наше объявление
        print(f"[DEBUG] GET /api/{API_VERSION}/item/{ad_id}, Status: {response.status_code}") # вывод 
        
        assert response.status_code == 200, f"Ожидался код 200, получен {response.status_code}"
        response_json = response.json()
        
        # Проверяем, что ответ является массивом
        assert isinstance(response_json, list), "Ответ должен быть массивом" 
        assert len(response_json) > 0, "Массив ответа не должен быть пустым"
        
        # Ищем наше объявление в массиве
        found_ad = next((ad for ad in response_json if ad["id"] == ad_id), None) # поиск нашего объявления в массиве
        assert found_ad is not None, f"Объявление с id {ad_id} не найдено в ответе" # если не найдено
        assert found_ad["sellerId"] == created_ad_data["sellerId"], f"Несоответствие sellerId: {found_ad['sellerId']} != {created_ad_data['sellerId']}"
    
    def test_get_ad_by_id_not_found(self):
        #Запрос несуществующего объявления Not Found
        non_existent_id = generate_ad_id()
        response = requests.get(f"{BASE_URL}/api/{API_VERSION}/item/{non_existent_id}") # поиск 
        print(f"[DEBUG] GET с несуществующим ID, Status: {response.status_code}")
        assert response.status_code == 404, f"Ожидался код 404, получен {response.status_code}" # вывод и получение ошибки (результата)

class TestGetStatistic:
    #Тестирование получения статистики
    
    def test_get_statistic_success(self, created_ad_data):
        #Успешное получение статистики
        ad_id = created_ad_data["id"]
        response = requests.get(f"{BASE_URL}/api/{API_VERSION}/statistic/{ad_id}") # поиск статистики по нашему объявлению 
        print(f"[DEBUG] GET /api/{API_VERSION}/statistic/{ad_id}, Status: {response.status_code}")
        
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
        #Статистика по несуществующему объявлению Not Found
        non_existent_id = generate_ad_id()
        response = requests.get(f"{BASE_URL}/api/{API_VERSION}/statistic/{non_existent_id}")
        print(f"[DEBUG] GET статистики с несуществующим ID, Status: {response.status_code}")
        assert response.status_code == 404, f"Ожидался код 404, получен {response.status_code}"

# Запуск тестов через pytest
if __name__ == "__main__":
    # Если запускаем файл напрямую, используем pytest.main()
    pytest.main([__file__, "-v", "--tb=short"])