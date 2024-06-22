from wtforms import (StringField, TextAreaField, IntegerField, BooleanField,RadioField,SelectField)
from flask_wtf import FlaskForm
from wtforms.validators import InputRequired, Length
from models import CategoriaDemanda

class CadastroDemandaForm(FlaskForm):
    titulo = StringField('titulo', validators=[InputRequired(message="Informe o título"),Length(min=1, max=200)])
    descricao = TextAreaField('descricao',validators=[InputRequired(message="Informe a descrição"),Length(max=240)])
    categoria = SelectField('categoria',choices=[i.value for i in CategoriaDemanda],coerce=int, validators=[InputRequired(message="Escolha uma opção")])
 