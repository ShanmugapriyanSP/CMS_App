import os


class Config:
    '''
    Database configurations

    '''
    SECRET_KEY = os.environ.get('SECRET_KEY')
    MONGO_URI = os.environ.get('MONGO_URI') + 'cms'
