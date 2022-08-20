from threading import Thread
import subprocess
import time

from mongodb import MongoDB
from pandas import ExcelWriter
import pandas

import asyncio
from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text

from aiogram.types import InlineKeyboardMarkup

from models import LoadModels, LoadModelsKey, AddModel, DelModel, activeModel, toggleActiveModel
from allow import CheckAllow, AddAllow, DeleteAllow, LoadAllow
from keyboard import homeMenu, settingsMenu, TextButtonList
from config import token
from logger import *

bot = Bot(token=token)
dp = Dispatcher(bot, storage=MemoryStorage())
startedGroupList = []   # Лист запущенных групп
startedGroupTread = []  # Лист запущенных групп в потоке
connectionGroupList = []    # Лист с запущенными процессами


class Models(StatesGroup):
    link = State()
    token = State()


class UserAllow(StatesGroup):
    addUser = State()
    addModel = State()


class GroupState(StatesGroup):
    name = State()


@dp.message_handler(commands=['start'])
async def echo(message: types.Message):
    if CheckAllow(message.from_user.id):
        text = 'VK Parser\nДля подробной инфомрации обо всем функционале воспользуйтесь командой /help.'
        await message.answer(text, reply_markup=homeMenu)


@dp.message_handler(commands=['help'])
async def echo(message: types.Message):
    if CheckAllow(message.from_user.id):
        await message.answer('Парсер групп Вконтакте')


#   Главная страница:
@dp.message_handler(text=[TextButtonList['home']])
async def process_hi1_command(message: types.Message):
    if CheckAllow(message.from_user.id):
        await message.answer(f'Мы на главной!\nВыбери пункт, который тебе нужен.', reply_markup=homeMenu)


#   Настройки:
@dp.message_handler(text=[TextButtonList['settings']])
async def process_hi1_command(message: types.Message):
    if CheckAllow(message.from_user.id):
        await message.answer(f'Мы в настройках!', reply_markup=settingsMenu)


#   Статус парсинга:
@dp.message_handler(text=[TextButtonList['status_parsing']])
async def process_hi1_command(message: types.Message):
    if CheckAllow(message.from_user.id):
        await message.answer(activeModel())


# Список групп
@dp.message_handler(text=[TextButtonList['groups']])
async def process_help_command(message: types.Message):
    if CheckAllow(message.from_user.id):
        listGroupMenu = InlineKeyboardMarkup()
        for i in LoadModelsKey():
            listGroupMenu.add(types.InlineKeyboardButton(text=i, callback_data=f'link:{i}'))
        listGroupMenu.add(types.InlineKeyboardButton(text='Отменить', callback_data=f'link:cancel'))
        await message.answer(f"Список групп.", reply_markup=listGroupMenu)


@dp.callback_query_handler(Text(startswith="link:"))
async def callbacks_num(call: types.CallbackQuery):
    if call.data == 'link:cancel':
        await call.answer()
        await call.message.delete()
        return
    if CheckAllow(call.from_user.id):

        deleteUserBtn = types.InlineKeyboardMarkup()
        deleteUserBtn.add(types.InlineKeyboardButton(text='Запустить', callback_data=f'runGroup_{call.data.split(":")[1]}'))
        deleteUserBtn.add(types.InlineKeyboardButton(text='Остановить', callback_data=f'stopGroup_{call.data.split(":")[1]}'))
        deleteUserBtn.add(types.InlineKeyboardButton(text='Удалить', callback_data=f'delGroup_{call.data.split(":")[1]}'))
        deleteUserBtn.add(types.InlineKeyboardButton(text='Отменить', callback_data=f'link:cancel'))
        await call.message.answer(f"Выберите действие с группой", reply_markup=deleteUserBtn)

    await call.message.delete()


@dp.callback_query_handler(Text(startswith="runGroup_"))
async def runGroup(call: types.CallbackQuery, state: FSMContext):
    data = call.data.split("_")[1]
    if call.data not in startedGroupList:
        startedGroupList.append(data)
        await call.message.answer(f"Группа {data} добавлена в список запущенных.", reply_markup=homeMenu)
    else:
        await call.message.answer(f"Группа {data} уже списке запущенных.", reply_markup=homeMenu)
    await state.finish()
    await call.message.delete()


@dp.callback_query_handler(Text(startswith="stopGroup_"))
async def stopGroup(call: types.CallbackQuery, state: FSMContext):
    data = call.data.split("_")[1]
    if data in startedGroupList:
        startedGroupList.remove(data)
        await call.message.answer(f"Группа {data} убрана из списка запущенных.", reply_markup=homeMenu)
    else:
        await call.message.answer(f"Группа {data} не находится в списке запущенных.", reply_markup=homeMenu)
    await state.finish()
    await call.message.delete()


@dp.callback_query_handler(Text(startswith="delGroup_"))
async def delGroup(call: types.CallbackQuery, state: FSMContext):
    data = call.data.split("_")[1]
    await call.message.answer(DelModel(data), reply_markup=homeMenu)
    await state.finish()
    await call.message.delete()


# Список пользователей:
@dp.message_handler(text=[TextButtonList['users']])
async def process_help_command(message: types.Message):
    if CheckAllow(message.from_user.id):
        listUserBtn = InlineKeyboardMarkup()
        for i in LoadAllow():
            listUserBtn.add(types.InlineKeyboardButton(text=i, callback_data=f'userid_{i}'))
        listUserBtn.add(types.InlineKeyboardButton(text='Отменить', callback_data='userid_:cancel'))
        await message.answer(f"Выбери пользователя, которого хочешь удалить.", reply_markup=listUserBtn)


@dp.callback_query_handler(Text(startswith="userid_"))
async def callbacks_num(call: types.CallbackQuery):
    if call.data == 'userid_:cancel':
        await call.answer()
        await call.message.delete()
        return
    if CheckAllow(call.from_user.id):
        listUserMenu = InlineKeyboardMarkup()
        listUserMenu.add(types.InlineKeyboardButton(text='Удалить пользователя', callback_data=f'delUserid_{call.data.split("_")[1]}'))
        listUserMenu.add(types.InlineKeyboardButton(text='Отменить', callback_data='userid_:cancel'))
        await call.message.answer('Выберите действие с пользователем.', reply_markup=listUserMenu)


@dp.callback_query_handler(Text(startswith="delUserid_"))
async def callbacks_num(call: types.CallbackQuery):
    if CheckAllow(call.from_user.id):
        await call.message.answer(DeleteAllow(call.data.split("_")[1]), reply_markup=homeMenu)

    await call.answer()
    await call.message.delete()


#   Добавить группу:
@dp.message_handler(text=[TextButtonList['add_model']])
async def user_register(message: types.Message):
    if CheckAllow(message.from_user.id):
        await message.answer("Введите ссылку на группу (пример https://vk.com/club1)")
        await Models.link.set()


@dp.message_handler(state=Models.link)
async def get_username(message: types.Message, state: FSMContext):
    await state.update_data(link=message.text.split('/')[-1])
    await message.answer("Отлично! Теперь введите Token VK API.")
    await Models.token.set()


@dp.message_handler(state=Models.token)
async def get_address(message: types.Message, state: FSMContext):
    await state.update_data(token=message.text)
    data = await state.get_data()
    await message.answer(AddModel(data['link'], data['token']), reply_markup=homeMenu)
    await state.finish()


# Добавить пользователя:
@dp.message_handler(text=[TextButtonList['add_user']])
async def process_help_command(message: types.Message):
    if CheckAllow(message.from_user.id):
        await UserAllow.addUser.set()
        deleteUserBtn = types.InlineKeyboardMarkup()
        deleteUserBtn.add(types.InlineKeyboardButton(text='Отменить', callback_data=f'cancelAddUser'))
        await message.answer(f"Введите ID пользователя (пример 12345678):", reply_markup=deleteUserBtn)


@dp.message_handler(state=UserAllow.addUser)
async def process_name(message: types.Message, state: FSMContext):
    if CheckAllow(message.from_user.id):
        try:
            id_ = int(message.text)
        except:
            await message.answer(f'ID должен состоять только из цифр.', reply_markup=homeMenu)
            await state.finish()
            return
        await message.answer(AddAllow(id_), reply_markup=homeMenu)

    await state.finish()


@dp.callback_query_handler(state='*', text="cancelAddUser")
async def cancelAddUser(call: types.CallbackQuery, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.finish()
    await call.message.delete()


# Получить отчет
@dp.message_handler(text=[TextButtonList['report']])
async def callbacks_num12(message: types.Message):
    if CheckAllow(message.from_user.id):
        data = await mongo.func()
        file_name = time.strftime('%Y.%m.%d_%H-%M-%S')
        df = pandas.DataFrame(data)
        temp_write = 0
        while temp_write != 1:
            writer = ExcelWriter(f'reports/{file_name}.xlsx')
            df.to_excel(writer, f'{file_name}')
            writer.save()
            temp_write = 1

        subprocess.call(f"python3 files.py {file_name} xlsx {message.from_user.id}", shell=True)


# Получить лог
@dp.message_handler(text=[TextButtonList['log']])
async def callbacks_num12(message: types.Message):
    if CheckAllow(message.from_user.id):
        subprocess.call(f"python3 files.py app log {message.from_user.id}", shell=True)


# Удаление данных из БД
@dp.message_handler(text=[TextButtonList['delDataFromDB']])
async def process_hi1_command(message: types.Message):
    if CheckAllow(message.from_user.id):
        await message.answer(await mongo.deleteData(), reply_markup=homeMenu)


# Алгоритм запуска группы
def StartGroup(groupname):
    try:
        modelsList = LoadModels()
        if groupname in modelsList:
            userdata = modelsList[groupname]
            userdata['name'] = groupname
            cmd = ['python3', 'vk.py', groupname, f'{userdata["group_id"]}', f'{userdata["token"]}']
            userdata['process'] = subprocess.Popen(cmd)
            connectionGroupList.append(userdata)

    except Exception as e:
        logging.error(f'[{groupname}] {e}')

    while True:
        time.sleep(1)

        if groupname not in startedGroupList:
            for i in range(len(connectionGroupList)):
                if connectionGroupList[i]['name'] == groupname:
                    connectionGroupList[i]['process'].terminate()
                    connectionGroupList.pop(i)
                    startedGroupTread.remove(groupname)
                    toggleActiveModel(groupname, "0")
                    logging.info(f'[{groupname}] Поток остановлен через бота.')
                    return


async def main():
    while True:
        await asyncio.sleep(5)
        try:
            if startedGroupList:
                for item in startedGroupList:
                    if item not in startedGroupTread:
                        Thread(target=StartGroup, args=(item,)).start()
                        startedGroupTread.append(item)
        except Exception as e:
            logging.error(f'{e}')


if __name__ == '__main__':
    mongo = MongoDB()
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.create_task(main())
    executor.start_polling(dp, skip_updates=True)
