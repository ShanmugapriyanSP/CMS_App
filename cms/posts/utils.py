import os
import secrets


from flask import current_app


def save_media(form_media):
    '''
    Stores the media content in the project directory

    :param form_media:
    :return:
    '''
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_media.filename)
    filename = random_hex + f_ext
    media_path = os.path.join(current_app.root_path, 'static/posts_media', filename)
    form_media.save(media_path)
    return filename
