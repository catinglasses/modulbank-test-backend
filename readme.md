# Запуск проекта

Для запуска проекта:

1. Клонируем репозиторий:
    ```sh
    git clone <URL_репозитория>
    ```

2. Переходим в директорию проекта:
    ```sh
    cd modulbank-test-backend
    ```

3. Для корректной работы кода необходимо создать переменную окружения (`.env`) на уровне проекта (`/modulbank-test-backend`), где хранятся данные для подключения к БД.  
   Ниже представлен пример моего .env.
   ```
   DB_HOST=postgres
   DB_PORT=5432
   DB_USER=postgres
   DB_PASS=postgres
   DB_NAME=modulbank_db
   ```

3. Создаем виртуальное окружение:
    ```sh
    python -m venv venv
    ```

4. Активируем виртуальное окружение:
    ```sh
    source venv/Scripts/activate
    ```

5. Установка зависимостей для работы клиента:
    ```sh
    pip install -r requirements.txt
    ```

6. Запуск Docker Compose:
    ```sh
    docker compose up --build
    ```

7. (ВАЖНО: при работе на Windows-системе исполнять команду в `cmd`, не `Git Bash`, т.к. [последний работает некорректно с путями](https://stackoverflow.com/questions/76505589/docker-exec-workdir-does-not-work-in-git-bash).)  
    Миграции базы данных :
    ```sh
    docker exec -w /app/server -it modulbank-test-backend-fastapi-1-1 alembic upgrade head
    ```

8. Запуск клиента:
    ```sh
    python client/main.py
    ```

Пример итогов работы `client/main.py`:
```sh
INFO - ==========  |   RESULTS   |  ==========
INFO - Total time: 50.88 s
INFO - Successful requests: 4948/5000 (1.0% loss)
INFO - Throughput: 97.25 req/s
INFO - Average latency: 278.19 ms
```
