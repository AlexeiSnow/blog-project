
## Установка и запуск

### 1. Клонировать репозиторий
```bash
git clone https://github.com/AlexeiSnow/blog-project.git
cd blog-project
```

### 2. Создать виртуальное окружение

**Linux**
```bash
python -m venv venv
source venv/bin/activate
```

**Windows**
```bash
python -m venv venv
venv\Scripts\activate
```

### 3. Установить зависимости
```bash
pip install -r requirements.txt
```

### 4. Настроить PostgreSQL

```bash
# Linux
sudo -u postgres psql

# Windows — открыть pgAdmin или запустить:
# psql -U postgres
```

Выполнить в консоли PostgreSQL:
```sql
CREATE DATABASE blog_db;
CREATE USER blog_user WITH PASSWORD 'придумайте_пароль';
GRANT ALL PRIVILEGES ON DATABASE blog_db TO blog_user;
GRANT ALL ON SCHEMA public TO blog_user;
\q
```

### 5. Создать файл .env
Создай файл `.env` в корне проекта (рядом с manage.py):

SECRET_KEY=любой_случайный_набор_символов_от_50_знаков
DB_PASSWORD=пароль_который_указали_в_шаге_4
DEBUG=True

### 6. Применить миграции
```bash
python manage.py migrate
```

### 7. Загрузить демонстрационные данные (опционально)
```bash
python manage.py loaddata fixtures/initial_data.json
```

### 8. Запустить сервер
```bash
python manage.py runserver
```

Сайт будет доступен по адресу: http://127.0.0.1:8000