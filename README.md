## Установка

Для запуска приложения проделайте следующие шаги:

1. Склонируйте репозиторий.

2. Перейдите в папку с кодом и создайте виртуальное окружение:
```
python -m venv venv
```

3. Активируйте виртуальное окружение:
```
source venv\scripts\activate
```
4. Установите зависимости:
```
python -m pip install -r requirements.txt
```
5. Выполните миграции:
```
python manage.py migrate
```
6. Создайте суперпользователя:
```
python manage.py createsuperuser
```
7. Запустите сервер:
```
python manage.py runserver
```

## Загрузка данных из csv в БД

Чтобы загрузить таблицы из csv в базу данных:
```
python manage.py load_csv --all
```
Чтобы очистить базу данных: 
```
python manage.py load_csv --clear
```