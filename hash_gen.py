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
