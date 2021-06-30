import os

CELERY_BROKER_URL = "redis://localhost:6379/0"
CELERY_RESULT_BACKEND = "redis://localhost:6379/0"

SQLALCHEMY_TRACK_MODIFICATIONS = True
SECRET_KEY = "thisismysecretkeydonotstealit"
SQLALCHEMY_DATABASE_URI = "sqlite:///db.sqlite3"

MAIL_SERVER = "smtp.gmail.com"
MAIL_PORT = 587
MAIL_USERNAME = "niksan870@gmail.com"
MAIL_PASSWORD = "hlqnbtacqusvztlb"
MAIL_USE_TLS = True
MAIL_DEFAULT_SENDER = "niksan870@gmail.com"
