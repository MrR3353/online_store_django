Установите Python 3.11

Перейдите в каталог проекта (myshop) и создайте виртуальное окружение (если оно еще не создано):

```sh
python -m venv venv
```
Затем активируйте виртуальное окружение:

Для Linux/Mac:
```
source venv/bin/activate
```
Для Windows:

```
.\venv\Scripts\activate
```
Установите зависимости:
```sh
pip install -r requirements.txt
```

Примените миграции для создания базы данных:
```sh
python manage.py migrate
```

Создайте суперпользователя (по желанию):
```sh
python manage.py createsuperuser
```

Запустите сервер:

```sh
python manage.py runserver
```
По умолчанию, сервер будет доступен по адресу http://127.0.0.1:8000/.