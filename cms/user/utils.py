import os
import secrets

from PIL import Image
from flask import current_app


def save_picture(form_picture):
    '''
    Stores the compressed image to project directory

    :param form_picture:
    :return:
    '''
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_filename = random_hex + f_ext
    picture_path = os.path.join(current_app.root_path, 'static/display_pics', picture_filename)
    output_size = (600, 600)
    image = Image.open(form_picture)
    image.thumbnail(output_size)
    image.save(picture_path)
    return picture_filename
