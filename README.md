# Задание
## Пререквизиты
Установить [docker](https://www.digitalocean.com/community/tutorials/how-to-install-and-use-docker-on-ubuntu-18-04), [docker-compose](https://docs.docker.com/compose/install/), склонировать репозиторий и собрать сервисы с помощью docker-compose
```shell script
git clone https://github.com/AnnaRodionova/giftshop.git
cd giftshop
docker-compose build --no-cache
```

## Запуск тестов
```shell script
docker-compose run web python3 manage.py test
```

## Запуск окружения
```shell script
docker-compose -f docker-compose.yml -f docker-compose.prod.yml run web python3 manage.py migrate
docker-compose -f docker-compose.yml -f docker-compose.prod.yml up
```

## Остановить и удалить контейнеры
```shell script
docker-compose down --remove-orphans
```

## Зависимости
* **Django (2.2.4)** - MVC веб фреймворк
* **djangorestframework (3.10.2)** - библиотека для REST API в Django
* **gunicorn (19.9.0)** - WSGI HTTP сервер
* **numpy (1.17.0)** - библиотека для подсчета персентиля
* **psycopg2 (2.8.3)** - адаптер для PostreSQL
* **pytz (2019.2)** - зависимость Django для тайм-зон
* **sqlparse (0.3.0)** - зависимость Django, парсер sql 