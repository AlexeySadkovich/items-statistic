***Переменные окружения:***
```
REDIS_HOST
REDIS_PORT

MONGO_HOST
MONGO_PORT

MONGO_INITDB_DATABASE
MONGO_INITDB_ROOT_USERNAME
MONGO_INITDB_ROOT_PASSWORD
```
Расположить в файле .env в корне проекта

***Запуск:***
```
$ docker-compose up --build
```

***swagger:*** 
```
http://127.0.0.1:8000/docs
```

***API:***

```/add``` - Сохранить поисковую фразу и регион<br>
```/stat``` - Посмотреть статистику по запросу<br>
```/top``` - Посмотреть топ 5 объявлений
