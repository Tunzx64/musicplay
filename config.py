import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

class Config():
    SECRET_KEY = 'minha_chave'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = f'sqlite:///{os.path.join(BASE_DIR, "instance", "banco.db")}'