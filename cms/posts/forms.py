from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed
from wtforms import StringField, TextAreaField, SubmitField, FileField
from wtforms.validators import DataRequired


class NewPostForm(FlaskForm):
    '''
    Flask form for creating new post

    '''
    title = StringField('Title', validators=[DataRequired()])
    content = TextAreaField('Content', validators=[DataRequired()])
    media = FileField('Upload media content', validators=[FileAllowed(['jpg', 'png', 'pdf'])])
    submit = SubmitField('Post')
