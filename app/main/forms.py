from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField,TextAreaField
from wtforms.validators import DataRequired,ValidationError,Length
from app.models import User

class PostForm(FlaskForm):
    post = TextAreaField('Say something',validators=[DataRequired(), Length(min=1, max=140)],render_kw={"style":"height: 180px"})
    submit = SubmitField('Submit')

class EditProfileForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    about_me = TextAreaField('About me', validators=[Length(min=0, max=140)])
    submit = SubmitField('Submit')

    def __init__(self, original_username,*args, **kwargs):
        super().__init__(*args, **kwargs)
        self.original_username = original_username

    def validate_username(self,username):
            if username.data != self.original_username:
                user = User.query.filter_by(username=self.username.data).first()
                if user is not None:
                    raise ValidationError('Username been used, please use a different username.')

class EmptyForm(FlaskForm):
    submit = SubmitField('Submit')

class MessageForm(FlaskForm):
    message = TextAreaField('Message', validators=[DataRequired(), Length(min=0, max=140)])
    submit = SubmitField('Submit')