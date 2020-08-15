import uuid
import hashlib


def hash_password(password):
    # uuid используется для генерации случайного числа
    salt = uuid.uuid4().hex
    hash = hashlib.sha256(str(salt).encode() + str(password).encode()).hexdigest() + ':' + salt
    return hash[5:20]


def check_password(hashed_password, user_password):
    password, salt = hashed_password.split(':')
    return password == hashlib.sha256(str(salt).encode() + str(user_password).encode()).hexdigest()


#new_pass = input('Введите пароль: ')
#hashed_password = hash_password(new_pass)
#print('Строка для хранения в базе данных: ' + hashed_password)
#old_pass = input('Введите пароль еще раз для проверки: ')

#if check_password(hashed_password, old_pass):
 #   print('Вы ввели правильный пароль')
#else:
 #   print('Извините, но пароли не совпадают')