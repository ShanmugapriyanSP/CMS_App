import datetime

from bson import ObjectId
from flask_login import UserMixin

from cms import login_manager, Config, mongo


@login_manager.user_loader
def load_user(user_id):
    user = DB.retrieve_login(user_id)
    return User(user)


class DB:
    '''
    Methods to store the data in Mongo DB
    '''
    @staticmethod
    def create_user(name, email, hashed_password, image_file='default.jpg'):
        _id = mongo.db.user.insert_one(
            {'name': name, 'email': email, 'password': hashed_password, "image_file": image_file})
        return _id

    @staticmethod
    def store_post(title, content, user, media=''):
        _id = mongo.db.post.insert_one(
            {'title': title, 'date_posted': datetime.datetime.now(), 'content': content, 'user_id': user,
             'media': media})
        return _id

    @staticmethod
    def retrieve_posts(offset, limit):
        if mongo.db.post is None:
            return None
        else:
            return (list(mongo.db.post.find().skip(offset).limit(limit)))

    @staticmethod
    def is_user_exist(name):
        user = mongo.db.user.find_one({'name': name})
        if user is not None and len(user) > 0:
            return True
        else:
            return False

    @staticmethod
    def is_email_exist(email):
        user = mongo.db.user.find_one({'email': email})
        if user is not None and len(user) > 0:
            return True
        else:
            return False

    @staticmethod
    def retrieve_user(name):
        user = mongo.db.user.find_one({'name': name})
        if len(user) > 0:
            return user
        else:
            return None

    @staticmethod
    def retrieve_login(id):
        user = mongo.db.user.find_one({'_id': ObjectId(id)})
        if user is not None and len(user) > 0:
            return user
        else:
            return None

    @staticmethod
    def update_account(user):
        return mongo.db.user.replace_one({'_id': ObjectId(user.user_json['_id'])}, user.user_json, True)


class User(UserMixin):
    '''
    User info class
    '''
    def __init__(self, user_json):
        self.user_json = user_json

    def get_id(self):
        object_id = self.user_json['_id']
        return str(object_id)


class Post:
    '''
    Post info class
    '''
    def __init__(self, values):
        self.user_id = values['user_id']
        self.title = values['title']
        self.content = values['content']
        self.date_posted = values['date_posted']
        self.id = values['_id']
