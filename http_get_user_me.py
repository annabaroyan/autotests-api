import httpx  # Импортируем библиотеку HTTPX

# Инициализируем JSON-данные, которые будем отправлять в API
login_payload = {
    "email": "test@example.com",
    "password": "12345Test"
}


# Выполняем запрос на аутентификацию
login_response = httpx.post("http://localhost:8000/api/v1/authentication/login", json=login_payload)
login_response_data = login_response.json()

# Выводим полученные токены
print("Login response:", login_response_data)
print("Status Code:", login_response.status_code)



headers = {"Authorization": f"Bearer {login_response_data['token']['accessToken']}"}

# Выполняем запрос к эндпоинту /api/v1/users/me
users_me_response = httpx.get("http://localhost:8000/api/v1/users/me", headers=headers)
users_me_response_data = users_me_response.json()

# Выводим JSON-ответ в консоль
print("Users me:", users_me_response_data)
print("Status Code:", users_me_response.status_code)