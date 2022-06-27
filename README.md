# Парсер групп Вконтакте

### Описание
Программа собирает посты и комментарии с социальной сети Вконтакте, отбирает сообщения по ключевым словам нечетким сравнением и проверкой орфографии, сохраняет сообщения в нереляционную базу данных MongoDB. Реализован телеграмм бот для удаленного управления.

### Апробация программы
Windows 11  
Python 3.10.5  
MongoDB 5.0.9

В  Linux Ubuntu и macOS возникли ошибки с библиотекой pyenchant (для проверки орфографии).

### Выполните следующие действия
1) Установите MongoDB (MongoDB Community Server, https://www.mongodb.com/try/download)  
2) Подключитесь к интерфейсу:  
```
mongo shell
```  
3) Создайте БД с именем 'vk':  
```
use vk
```  
4) Создайте коллекцию с именем 'user':  
```
db.createCollection('user')
```  
5) Установите все зависимости:  
```
python3 install -r requirements.txt
```
6) Добавить словарь для поддержки русского языка в pyenchant  
Словари в папке dictionary: ru_RU.aff и ru_RU.dic  
Скопировать в папку со словарями:  
C:\Users\username\AppData\Local\Programs\Python\Python39\Lib\site-packages\enchant\data\mingw64\share\enchant\hunspell
7) Создайте свое приложение (Standalone-приложение):
https://vk.com/apps?act=manage  
Входные данные для получения токена  
client_id - id приложения  
scope - права доступа (https://dev.vk.com/reference/access-rights)  
Запрос для получения токена:  
https://oauth.vk.com/authorize?client_id=111111&display=mobile&redirect_uri=https://oauth.vk.com/blank.html&scope=wall,offline&response_type=token&v=5.131
8) Для работы без телеграмм бота:  
```
python3 .\vk.py <DOMAIN> <OWNER_ID> <TOKEN_VK_API>
```  
DOMAIN - Короткий адрес сообщества.  
OWNER_ID - Идентификатор сообщества, со стены которого необходимо получить записи
9) Для работы с телеграмм ботом  
В data/allow.txt добавить пользователей (каждого с новой строки).  
В data/words.txt добавить слова (каждое с новой строки).  
В data/group.json добавляется через телеграмм бота, в дальнейшем можно править вручную.  
Создать телеграмм бота через https://t.me/BotFather  
Добавить токен нового бота в config.py  
```
python3 .\bot.py
```

### Как отозвать токен?  
Вы можете принудительно отозвать токен (например, в том случае, если он стал известен постороннему), сбросив сеансы в настройках безопасности вашего аккаунта или сменив пароль. Также, если речь идет о токене не из вашего собственного приложения, можно просто удалить приложение из настроек: https://vk.com/settings?act=apps
