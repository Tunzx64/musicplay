from flask_wtf import FlaskForm
from wtforms import StringField, FileField, SubmitField, IntegerField, EmailField, PasswordField, SelectField
from wtforms.validators import DataRequired, Email, Length

class FormMusicas(FlaskForm):
    title = StringField(validators=[DataRequired()])
    filename = FileField(validators=[DataRequired()])
    submit = SubmitField('Enviar')

class FormPlaylist(FlaskForm):
    title = StringField(validators=[DataRequired()])
    submit = SubmitField('Criar Playlist')

class FormLogin(FlaskForm):
    email = EmailField(validators=[DataRequired(), Email()])
    password = PasswordField(validators=[DataRequired(), Length(min=8)])
    submit = SubmitField('Login')

class FormRegister(FlaskForm):
    name = StringField(validators=[DataRequired(), Length(min=3)])
    email = EmailField(validators=[DataRequired(), Email()])
    password = PasswordField(validators=[DataRequired(), Length(min=8)])
    submit = SubmitField('Cadastrar')

class FormAddMusicPlaylist(FlaskForm):
    playlist_id = SelectField(validate_choice=[DataRequired()], coerce=int)
    submit = SubmitField('Adicionar a uma playlist') 