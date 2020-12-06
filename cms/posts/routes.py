from flask import flash, render_template, url_for, Blueprint
from flask_login import current_user
from werkzeug.utils import redirect

from cms.models import DB
from cms.posts.forms import NewPostForm
from cms.posts.utils import save_media

posts = Blueprint('posts', __name__)


@posts.route('/post/new', methods=['GET', 'POST'])
def new_post():
    '''
    Storing new post from user into Database

    :return: sucess message and redirects to home page
    '''
    form = NewPostForm()
    if form.validate_on_submit():
        media = ''
        if form.media.data:
            media = save_media(form.media.data)
        DB.store_post(title=form.title.data, content=form.content.data, user=current_user.user_json['_id'], media=media)
        flash('Your post has been created!', 'success')
        return redirect(url_for('main.home'))
    return render_template('new_post.html', title='New Post', form=form, legend='New Post')
