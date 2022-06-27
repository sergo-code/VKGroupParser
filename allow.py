def LoadAllow():
    try:
        with open('data/allow.txt') as file:
            models = [row.strip().lower() for row in file]
    except Exception as e:
        return e
    return models


def CheckAllow(userid):
    if str(userid) in LoadAllow():
        return True
    else:
        return False


def AddAllow(userid):
    if str(userid) in LoadAllow():
        return f'Пользователь есть в этом списке.'
    try:
        with open('data/allow.txt', 'a') as file:
            file.write(f'\n{userid}')
    except Exception as e:
        return e
    return f'Пользователь {userid} успешно добавлен.'


def DeleteAllow(userid):
    userlist = LoadAllow()
    if str(userid) not in userlist:
        return f'Пользователь не найден.'
    userlist.remove(userid)
    try:
        with open('data/allow.txt', 'w') as file:
            for row in userlist:
                file.write(f'{row}\n')
    except Exception as e:
        return e
    return f'Пользователь {userid} успешно удалён.'