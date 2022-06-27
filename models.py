import json
from requests import post


def LoadModels():
    with open('data/group.json') as file:
        models = json.load(file)
    return models


def LoadModelsKey():
    with open('data/group.json') as file:
        models = json.load(file)
    secondList = []
    for key in models.keys():
        secondList.append(key)
    return secondList


def AddModel(link, token):
    try:
        with open('data/group.json') as file:
            models = json.load(file)
            url = f"https://api.vk.com/method/utils.resolveScreenName?v=5.131&access_token={token}&screen_name={link}"

            response = post(url).text

            owner_id = json.loads(response)

            if 'response' in owner_id.keys():
                if 'object_id' in owner_id['response'].keys():
                    owner_id = owner_id['response']['object_id']
                    models.update({link: {"group_id": owner_id, "token": token, "active": "0"}})

                    with open('data/group.json', 'w') as file:
                        json.dump(models, file)
                else:
                    text = 'Ссылка введена неверно!'
                    return f'{link} не удалось добавить в список\n{text}'
            elif 'error' in owner_id.keys():
                text = 'Введен неверный токен!'
                return f'{link} не удалось добавить в список\n{text}'
    except:
        return f'{link} не удалось добавить в список'
    return f'Группа {link} успешно добавлена/обновлена.'


def DelModel(link):
    with open('data/group.json') as file:
        models = json.load(file)
    if link in models:
        del models[link]
    else:
        return f'Не удалось удалить {link}'
    with open('data/group.json', 'w') as file:
        json.dump(models, file)
    return f'Группа {link} успешно удалена.'


def toggleActiveModel(domain, toggle):
    with open('data/group.json') as file:
        models = json.load(file)
    models[domain]['active'] = toggle
    with open('data/group.json', 'w') as file:
        json.dump(models, file)


def activeModel():
    with open('data/group.json') as file:
        models = json.load(file)

    text = 'Список запущенных групп:\n'
    temp = len(text)
    for item in models.keys():
        if models[item]['active'] == '1':
            text += f'{item}\n'

    if temp != len(text):
        return text
    else:
        return 'В данный момент запущенных групп нет.'
