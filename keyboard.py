from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


TextButtonList = {
    'home': '↩️ На главную!',
    'settings': '⚙️ Настройки',
    'groups': '📚 Список групп',
    'users': '👤 Список пользователей',
    'status_parsing': '🪧 Статус парсинга',
    'add_model': '➕ Добавить новую группу',
    'add_user': '➕ Выдать доступ пользователю к боту',
    'report': '📝 Получить отчет',
    'log': '📜 Получить лог',
    'delDataFromDB': '❌ Удалить данные из БД',
}
ButtonList = {
    'home': KeyboardButton(TextButtonList['home']),
    'settings': KeyboardButton(TextButtonList['settings']),
    'groups': KeyboardButton(TextButtonList['groups']),
    'users': KeyboardButton(TextButtonList['users']),
    'status_parsing': KeyboardButton(TextButtonList['status_parsing']),

    'add_model': KeyboardButton(TextButtonList['add_model']),
    'add_user': KeyboardButton(TextButtonList['add_user']),

    'report': KeyboardButton(TextButtonList['report']),
    'log': KeyboardButton(TextButtonList['log']),
    'delDataFromDB': KeyboardButton(TextButtonList['delDataFromDB']),
}


homeMenu = ReplyKeyboardMarkup(resize_keyboard=True).add(ButtonList['status_parsing']).add(ButtonList['groups']).add(ButtonList['users']).add(ButtonList['report']).add(ButtonList['log']).add(ButtonList['settings'])
settingsMenu = ReplyKeyboardMarkup(resize_keyboard=True).add(ButtonList['home']).add(ButtonList['add_model']).add(ButtonList['add_user']).add(ButtonList['delDataFromDB'])
