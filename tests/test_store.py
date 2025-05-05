import allure
import pytest
import requests
import jsonschema

from .conftest import create_order
from .schemas.store_schema import ORDER_SCHEMA, INVENTORY_SCHEMA

BASE_URL = "http://5.181.109.28:9090/api/v3"

@allure.feature("Store")
class TestStore:
    @allure.title("Размещение заказа")
    def test_placing_an_order(self):
        with allure.step("Отпарвка запроса на размещение заказа"):
            payload = {
                "id": 1,
                "petId": 1,
                "quantity": 1,
                "status": "placed",
                "complete": True
            }
            response = requests.post(url=f'{BASE_URL}/store/order', json=payload)
            response_json = response.json()
        with allure.step("Проверка статуса ответа"):
            assert response.status_code == 200, "Статус код не соответствует ожидаемому"
            jsonschema.validate(response_json, ORDER_SCHEMA)
        with allure.step("Проверка парамтеров заказа в ответе"):
            assert response_json["id"] == payload["id"], "id не соответствует ожидаемому"
            assert response_json["petId"] == payload["petId"], "petId не соответствует ожидаемому"
            assert response_json["quantity"] == payload["quantity"], "quantity не соответствует ожидаемому"
            assert response_json["status"] == payload["status"], "status не соответствует ожидаемому"
            assert response_json["complete"] == payload["complete"], "id не соответствует ожидаемому"

    @allure.title("Получение информации о заказе по ID")
    def test_get_order_info_by_id(self, create_order):
        with allure.step("Получение информации о заказе по ID"):
            order_id = create_order["id"]
        with allure.step("Отправка запроса на получение информации о заказе по id"):
            response = requests.get(url=f'{BASE_URL}/store/order/{order_id}')
        with allure.step("Проверка статуса ответа и данных заказа"):
            assert response.status_code == 200, "Статус код не соответствует ожидаемому"
            assert response.json()["id"] == order_id

    @allure.title("Удаление заказа по ID")
    def test_delete_order_by_id(self, create_order):
        with allure.step("Получение информации о заказе по ID"):
            order_id = create_order["id"]
        with allure.step("Отправка запроса на удаление заказа по id"):
            response = requests.delete(url=f'{BASE_URL}/store/order/{order_id}')
        with allure.step("Проверка статуса ответа"):
            assert response.status_code == 200, "Статус код не соответствует ожидаемому"
        with allure.step("Отправка запроса на получение информации о заказе по id"):
            response = requests.get(url=f'{BASE_URL}/store/order/{order_id}')
        with allure.step("Проверка статуса ответа"):
            assert response.status_code == 404, "Статус код не соответствует ожидаемому"
        with allure.step("Проверка текстового содержания ответа"):
            assert  response.text == "Order not found", "Текст ответа не соответствует ожидаемому"

    @allure.title("Попытка получить информацию о несуществующем заказе")
    def test_get_nonexistent_order(self):
        with allure.step("Отправка запроса на получение информации о несуществующем заказе"):
            response = requests.get(url=f'{BASE_URL}/store/order/9999')
        with allure.step("Проверка статуса ответа"):
            assert response.status_code == 404, "Статус код не соответствует ожидаемому"
        with allure.step("Проверка текстового содержания ответа"):
            assert  response.text == "Order not found", "Текст ответа не соответствует ожидаемому"

    @allure.title("Получение инвентаря магазина")
    def test_get_inventory(self):
        with allure.step("Отправка запроса на получение инвентаря"):
            response = requests.get(url=f'{BASE_URL}/store/inventory')
        with allure.step("Проверка статуса ответа"):
            assert response.status_code == 200, "Статус код не соответствует ожидаемому"
        with allure.step("Проверка данных инвентаря"):
            inventory_data = response.json()
            jsonschema.validate(inventory_data, INVENTORY_SCHEMA)