from pymongo import MongoClient
import asyncio
from logger import *


class MongoDB:
    def __init__(self):
        self.client = MongoClient('localhost', 27017)
        self.db = self.client['vk']
        self.collections = self.db['user']

    async def func(self):
        await asyncio.sleep(0.01)
        return self.collections.find()

    async def insert(self, data):
        await asyncio.sleep(0.01)
        try:
            self.collections.insert_one(data)
        except Exception as e:
            logging.error(f'{e} {data}')

    async def deleteData(self):
        await asyncio.sleep(0.01)
        response = self.collections.delete_many({})
        if response.acknowledged:
            logging.info('Данные успешно удалены!')
            return 'Данные успешно удалены!'
        else:
            logging.error('Не удалось удалить данные.')
            return 'Не удалось удалить данные.'
