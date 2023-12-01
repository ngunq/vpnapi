from cryptography.fernet import Fernet
from django.conf import settings

def encrypt(s:str):
    fernet = Fernet(settings.FERNET_KEY)
    return fernet.encrypt(s.encode()).decode()

def decrypt(s:str):
    fernet = Fernet(settings.FERNET_KEY)
    return fernet.decrypt(s.encode()).decode()
