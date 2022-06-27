# -*- coding: UTF-8 -*-
import asyncio
import aiofiles
from fuzzywuzzy import process
from enchant.checker import SpellChecker


async def loadWords():
    try:
        async with aiofiles.open('data/words.txt', mode='r') as file:
            models = [row.strip().lower() async for row in file]
    except Exception as e:
        return e
    return models


async def checkWords(message):
    await asyncio.sleep(0.01)
    words = await loadWords()
    word1 = process.extractOne(message, words)

    if word1[1] >= 60:
        words.remove(word1[0])
        word2 = process.extractOne(message, words)
        if word2[1] >= 60:
            if len(message)*1.5 < len(word1[0]) and len(message)*1.5 < len(word2[0]):
                return False, None, None
            else:
                return True, word1, word2
        else:
            checker = SpellChecker("ru_RU")
            checker.set_text(message)
            temp = 0
            sum_words = len(message.split())
            for i in checker:
                temp += 1
            if temp/sum_words > 0.3:
                if len(message) * 1.5 < len(word1[0]):
                    return False, None, None
                else:
                    return True, word1, 'орфографические ошибки'
            else:
                return False, None, None
    else:
        return False, None, None


if __name__ == '__main__':
    text = '🤯 Dəт$k0ē n/ø/pño смо/Tpu-ka zdecь👩🏻👨‍👩‍👧‍👦 ТГГГГ'
    temp = asyncio.get_event_loop().run_until_complete(checkWords(text))
    print(temp[0])
    print(temp[1])
    print(temp[2])
