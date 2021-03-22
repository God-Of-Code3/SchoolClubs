from db.connection import *
import hashlib


def hash_password(string):
    string = string.encode()
    salt = "salt123"
    dk = hashlib.pbkdf2_hmac('sha256', string, salt.encode(), 100000)
    return dk.hex()
