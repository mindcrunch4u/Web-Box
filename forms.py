from flask_wtf import FlaskForm
from wtforms import StringField, TextField, SubmitField, PasswordField
from wtforms.validators import DataRequired, Length
from wtforms.widgets import TextArea

class MsgForm(FlaskForm):
    content = TextField('Content', widget=TextArea(), render_kw={
        "onchange":"show_keyfield()",
        "onkeyup":"show_keyfield()"
        })
    post_id = StringField('Post ID: ', validators=[])
    password = PasswordField('Password: ', validators=[])
    submit = SubmitField('Schicken', render_kw={
        "onclick":"encrypt()"
        })
