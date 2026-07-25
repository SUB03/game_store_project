import os
from pwdlib import PasswordHash

password_hash = PasswordHash.recommended()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"
DUMMY_HASH = password_hash.hash("daoGiMoiajhsdaih")

assert SECRET_KEY != None, "SECRET_KEY is not defined in environment variables"

def verify_password(plain_password, hashed_password):
    return password_hash.verify(plain_password, hashed_password)

def verify_dummy(password):
    password_hash.verify(password, DUMMY_HASH)

def get_password_hash(password):
    return password_hash.hash(password)