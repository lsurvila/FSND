address = 'localhost'
db_user = 'postgres'
db_psw = 'postgres'
db_port = 5432
db_name = 'trivia_test'

DEBUG = True
SQLALCHEMY_DATABASE_URI = f'postgres://{db_user}:{db_psw}@{address}:{db_port}/{db_name}'
SQLALCHEMY_TRACK_MODIFICATIONS = False
