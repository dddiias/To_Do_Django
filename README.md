# ✅ To-Do API (Django + DRF + JWT)

REST API для управления списком задач пользователя (To-Do list) с авторизацией через JWT.  
Реализовано на **Django**, **Django REST Framework**, **SimpleJWT** с поддержкой фильтров, пагинации и Docker/Postgres.

---

## ✨ Возможности
- ***Регистрация*** и ***авторизация*** пользователей (JWT)
- ***Обновление*** и отзыв токенов (refresh, blacklist)
- ***CRUD*** операций над задачами
- ***Привязка задач*** к текущему пользователю
- ***Статусы***: `pending`, `done`, `archived`
- ***Фильтры***:
  - по `status`
  - по дате создания (`date_from`, `date_to`)
  - по дедлайну (`due_on`, `due_from`, `due_to`)
- ***Пагинация*** (PAGE_SIZE=10)
- ***Unit-тесты*** (pytest/unittest)
- ***Docker-сборка с Postgres***

---

## 🛠 Стек технологий
![Python](https://img.shields.io/badge/Python-3.11-blue)
![Django](https://img.shields.io/badge/Django-5.x-success)
![DRF](https://img.shields.io/badge/DRF-3.x-red)
![Postgres](https://img.shields.io/badge/Postgres-15-blue)
![Docker](https://img.shields.io/badge/Docker-✓-blue)
- SimpleJWT (с blacklist)
- django-filter
- gunicorn

---

## 🚀 Локальный запуск (SQLite)
```bash
git clone <repo_url>
cd <repo_folder>

python -m venv .venv
.venv\Scripts\activate   # Windows
# source .venv/bin/activate # Linux/Mac

pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```
API будет доступно по адресу: http://127.0.0.1:8000/api/

---

## 🐳 Запуск в Docker
```bash
docker compose up --build
```
- Django: http://127.0.0.1:8000/api/
- Postgres: порт 5432 (db:todo/todo)

***Создать суперпользователя***:
```bash
python manage.py createsuperuser
```

---

## 🔑 Эндпоинты авторизации

| Метод | URL | Описание |
|-------|-----|----------|
| POST  | `/api/auth/register/`         | Регистрация |
| POST  | `/api/auth/token/`            | Получение `access` и `refresh` |
| POST  | `/api/auth/token/refresh/`    | Обновление `access` |
| POST  | `/api/auth/token/blacklist/`  | Logout |

---

## 📝 Эндпоинты задач

| Метод | URL | Описание |
|-------|-----|----------|
| GET  | `/api/tasks/`         | Список задач |
| POST  | `/api/tasks/`        | Создать задачу |
| GET  | `/api/tasks/{id}/`    | Получить задачу |
| PATCH  | `/api/tasks/{id}/`  | Обновить задачу |
| DELETE  | `/api/tasks/{id}/` | Удалить задачу |

***Фильтры***:
- `?status=pending`
- `?date_from=YYYY-MM-DD&date_to=YYYY-MM-DD`
- `?due_on=YYYY-MM-DD`
- `?due_from=YYYY-MM-DD&due_to=YYYY-MM-DD`

---

## 📌 Примеры curl (cmd.exe, Windows)
***Регистрация***
```cmd
Копировать
Редактировать
curl -X POST "http://127.0.0.1:8000/api/auth/register/" ^
  -H "Content-Type: application/json" ^
  -d "{\"username\":\"user1\",\"email\":\"user1@mail.com\",\"password\":\"Test1234!\"}"
```
***Авторизация***
```cmd
curl -X POST "http://127.0.0.1:8000/api/auth/token/" ^
  -H "Content-Type: application/json" ^
  -d "{\"username\":\"user1\",\"password\":\"Test1234!\"}"
```
***Обновление access токена***
```cmd
curl -X POST "http://127.0.0.1:8000/api/auth/token/refresh/" ^
  -H "Content-Type: application/json" ^
  -d "{\"refresh\":\"<REFRESH_TOKEN>\"}"'
```
***Logout (отзыв refresh токена)***
```cmd
curl -X POST "http://127.0.0.1:8000/api/auth/token/blacklist/" ^
  -H "Content-Type: application/json" ^
  -d "{\"refresh\":\"<REFRESH_TOKEN>\"}"
```
***Создание задачи***
```cmd
curl -X POST "http://127.0.0.1:8000/api/tasks/" ^
  -H "Content-Type: application/json" ^
  -H "Authorization: Bearer <ACCESS_TOKEN>" ^
  -d "{\"title\":\"Report\",\"description\":\"Write API docs\",\"status\":\"pending\",\"due_date\":\"2025-08-15\"}"
```
***Получение списка задач (без фильтров)***
```cmd
curl -X GET "http://127.0.0.1:8000/api/tasks/" ^
  -H "Authorization: Bearer <ACCESS_TOKEN>"
```
***Получение списка задач (по статусу)***
```cmd
curl -X GET "http://127.0.0.1:8000/api/tasks/?status=pending" ^
  -H "Authorization: Bearer <ACCESS_TOKEN>"
```
***Получение списка задач (по дате создания)***
```cmd
curl -X GET "http://127.0.0.1:8000/api/tasks/?date_from=2025-08-01&date_to=2025-08-15" ^
  -H "Authorization: Bearer <ACCESS_TOKEN>"
```
***Получение списка задач (по дедлайну due_date)***
```cmd
:: точная дата
curl -X GET "http://127.0.0.1:8000/api/tasks/?due_on=2025-08-15" ^
  -H "Authorization: Bearer <ACCESS_TOKEN>"

:: диапазон дат
curl -X GET "http://127.0.0.1:8000/api/tasks/?due_from=2025-08-10&due_to=2025-08-20" ^
  -H "Authorization: Bearer <ACCESS_TOKEN>"
```
***Получение задачи по ID***
```cmd
curl -X GET "http://127.0.0.1:8000/api/tasks/1/" ^
  -H "Authorization: Bearer <ACCESS_TOKEN>"
```
***Обновление задачи (например, статус на done)***
```cmd
curl -X PATCH "http://127.0.0.1:8000/api/tasks/1/" ^
  -H "Content-Type: application/json" ^
  -H "Authorization: Bearer <ACCESS_TOKEN>" ^
  -d "{\"status\":\"done\"}"
```
***Удаление задачи***
```cmd
curl -X DELETE "http://127.0.0.1:8000/api/tasks/1/" ^
  -H "Authorization: Bearer <ACCESS_TOKEN>"
```

---

## 🧪 Запуск тестов
- Локально:
  ```bash
  python manage.py test
  ```
- В Docker:
  ```bash
  docker compose exec web python manage.py test
  ```

