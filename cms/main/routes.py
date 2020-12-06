from flask import Blueprint, request, render_template
from flask_paginate import Pagination
import json

from cms import mongo
from cms.models import DB, Post

main = Blueprint('main', __name__)


@main.route('/')
@main.route('/home')
def home():
    '''
    Retrives all the posts present in
    the database and sends along with
    pagination

    :return: posts data and pagination object
    '''
    page = request.args.get('page', 1, type=int)
    posts = DB.retrieve_posts(page, 5)
    data = []
    for post in posts:
        data.append(Post(post))
    pagination = Pagination(page=page, total=len([d for d in posts]), per_page=5, offset=page, css_framework='bootstrap4')
    return render_template('home.html', posts=data, pagination=pagination)


@main.route('/about')
def about():
    return render_template('about.html', title='About CMS')
