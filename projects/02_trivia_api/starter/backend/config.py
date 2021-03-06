import os

from util import get_localhost_address

address = get_localhost_address()
port = 5000
db_user = 'postgres'
db_psw = 'postgres'
db_port = 5432
db_name = 'trivia'

DEBUG = True
SECRET_KEY = os.urandom(32)
SERVER_NAME = f'{address}:{port}'
SQLALCHEMY_DATABASE_URI = f'postgres://{db_user}:{db_psw}@{address}:{db_port}/{db_name}'
SQLALCHEMY_TRACK_MODIFICATIONS = False
