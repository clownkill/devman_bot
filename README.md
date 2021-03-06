# devman_bot
 
Скрипт для отслеживания статуса проверки отправленного на проверку урока на [dvmn.org](https://dvmn.org).

Для взаимодействия с [API dvmn.org](https://dvmn.org/api/docs/) используется `Long polling`.
 Результат проверки отправляется в Telegram-бот.

### Как установить
Python3 должен быть уже установлен. Затем используйте 'pip' (или 'pip3', если есть конфликт с Python2) для установки зависимостей.

```
pip install -r requirements.txt
```

### Объявление переменных окружения
Перед запуском скрипта в одном каталоге с файлом `main.py` необходимо создать файл для хранения переменных окружения с именем `.env` со следующим содержимым:
```
DEVMAN_TOKEN=[TOKEN]
TELEGRAM_TOKEN=[TOKEN]
TELEGRAM_CHAT_ID=[ID]
```
В переменной `DEVMAN_TOKEN` хранится API-токен, полученный от [dvmn.org](https://dvmn.org/api/docs/).

В переменной `TELEGRAM_API` хранится API-токен Telegram-бота.

В переменной `CHAT_ID` хранится ID чата в который будут отправляться сообщения с результатами проверки.

### Инструкция
Для запуска скрипта используйте: 
```
python main.py
```


### Запуск с Docker
Клонируйте репозиторий:
```
git clone https://github.com/clownkill/devman_bot
```
Для запуска бота с помощью докера используйте следующие комманды:
```
docker build -t [имя docker-контейнера] .
```
Перед запуском контейнера в одном каталоге с файлом `main.py` необходимо создать файл для хранения переменных окружения с именем `.env` со следующим содержимым:
```
DEVMAN_TOKEN=[TOKEN]
TELEGRAM_TOKEN=[TOKEN]
TELEGRAM_CHAT_ID=[ID]
```
```
docker run -d --env-file ./.env [имя docker-контейнера]
```

### Деплой

Для деплоя проекта необходимо воспользоваться инструкцией на [heroku](https://devcenter.heroku.com/articles/build-docker-images-heroku-yml).


### Цель проекта

Код написан в образовательных целях на онлайн-курсе для веб-разработчиков [dvmn.org](https://dvmn.org).
