from flask import Flask, render_template, request, url_for, redirect, flash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
from sqlalchemy import Enum
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from flask_wtf import FlaskForm
from wtforms import (StringField, TextAreaField, IntegerField, BooleanField,RadioField,SelectField)
from wtforms.validators import InputRequired, Length
import enum
from datetime import datetime


 
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://postgres:admin@localhost:5432/portal_demandas'
app.secret_key = 'super secret key'
db = SQLAlchemy()
 
login_manager = LoginManager()
login_manager.init_app(app)

class NivelAcesso(enum.Enum):
    ADMINISTRADOR = 1
    INTELIGENCIA = 2
    COMUM = 3

class TipoDemanda(enum.Enum):
    SIMPLES = 1
    COMPLEXA = 2

class CategoriaDemanda(enum.Enum):
    CONSULTA = 1
    OQC = 2
    RELATORIO = 3

class Status(enum.Enum):
    ABERTA = 1
    AGUARDANDO_DISTRIBUICAO = 2
    ATRIBUIDA = 3
    FAZENDO = 4
    FINALIZADA = 5
    COM_IMPEDIMENTO = 6
    CANCELADA = 7

class Usuario(UserMixin, db.Model):
    id = db.Column(db.BigInteger, primary_key=True)
    nomeCompleto = db.Column(db.String(250), unique=True, nullable=False)
    senha = db.Column(db.String(250), nullable=False)
    cargo = db.Column(db.String(250))
    cpf = db.Column(db.String(250))
    matricula = db.Column(db.String(250))
    email = db.Column(db.String(250))
    nivelAcesso = db.Column(Enum(NivelAcesso))
    #manytoone
    demandas_solicitadas = relationship("Demanda", primaryjoin="Usuario.id == Demanda.id_usuario_demandante")
    demandas_atribuidas = relationship("Demanda", primaryjoin="Usuario.id == Demanda.id_analista_responsavel")

class Demanda(db.Model):
    id = db.Column(db.BigInteger, primary_key=True)
    dataAbertura = db.Column(db.DateTime)
    dataFinalizacao = db.Column(db.DateTime)
    #manytoone
    id_usuario_demandante = db.Column(db.Integer, db.ForeignKey('usuario.id'))
    usuario_demandante = relationship("Usuario", foreign_keys=[id_usuario_demandante])
	#manytoone
    id_analista_responsavel = db.Column(db.Integer, db.ForeignKey('usuario.id'))
    analista_responsavel = relationship("Usuario",foreign_keys=[id_analista_responsavel])
    titulo = db.Column(db.String(250))
    descricao = db.Column(db.String(250))
    tipo = db.Column(Enum(TipoDemanda))
    prazoEntraga = db.Column(db.DateTime)
    categoria = db.Column(Enum(CategoriaDemanda))
	#onetomany
    anexos = relationship("Anexo", back_populates="demanda")
    status = db.Column(Enum(Status))
class Anexo(db.Model):
    id = db.Column(db.BigInteger, primary_key=True)
    caminho_arquivo = db.Column(db.String(250))
    nome_arquivo = db.Column(db.String(250))
    mime_type = db.Column(db.String(250))
    #manytoone
    id_usuario_cadastro = db.Column(db.BigInteger, db.ForeignKey("usuario.id"))
    data_cadastro = db.Column(db.DateTime)
    id_demanda = db.Column(db.BigInteger, db.ForeignKey("demanda.id"))
    demanda = relationship("Demanda", back_populates="anexos")

db.init_app(app)
 
 
with app.app_context():
    db.create_all()

class CadastroDemandaForm(FlaskForm):
    titulo = StringField('titulo', validators=[InputRequired(message="Informe o título"),Length(min=1, max=200)])
    descricao = TextAreaField('descricao',validators=[InputRequired(message="Informe a descrição"),Length(max=240)])
    categoria = SelectField('categoria',choices=[i.value for i in CategoriaDemanda],coerce=int, validators=[InputRequired(message="Escolha uma opção")])
 
 
@login_manager.user_loader
def loader_user(user_id):
    return Usuario.query.get(user_id)
 

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        user = Usuario.query.filter_by(cpf=request.form.get("username")).first()
        if user != None and user.senha == request.form.get("password"):
            login_user(user)
            return redirect(url_for("home"))
    flash("Verifique o usuário e senha.")
    return render_template("index.html")
 
 
@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("index"))

@app.route("/home")
@login_required
def home():
    return render_template("home.html")

@app.route("/inicio_cadastro_demanda")
@login_required
def redirecionaCadastroDemanda():
    return render_template("cadastrar_demanda.html", categorias = [i for i in CategoriaDemanda])

@app.route("/cadastrar_demanda", methods=["GET", "POST"])
@login_required
def cadastrarDemanda():
    if request.method == "POST":
        form = CadastroDemandaForm(meta={'csrf' : False})
        if form.validate_on_submit():
            demanda = Demanda(titulo=form.titulo.data, descricao = form.descricao.data, dataAbertura=datetime.now(), status = Status.ABERTA, 
                              tipo = TipoDemanda.SIMPLES, usuario_demandante = current_user, categoria = CategoriaDemanda(form.categoria.data))
            db.session.add(demanda)
            db.session.commit()
            flash("Solicitação realizada com sucesso.")
        else:
            for erro in form.errors.items():
                flash(str(erro[0]) + ": " + str(erro[1]))
            return render_template("cadastrar_demanda.html",categorias = [i for i in CategoriaDemanda])
        return render_template("home.html")
    if request.method == "GET":
        return render_template("cadastrar_demanda.html",categorias = [i for i in CategoriaDemanda])



@app.route("/listar_demandas")
@login_required
def redirecionaListarDemanda():
    demandas = Demanda.query.filter_by(status = Status.ABERTA)
    return render_template("listar_demandas.html", demandas = demandas)
 
@app.route("/iniciar_editar_demanda/<int:id>")
@login_required
def iniciarEditarDemanda(id):
    demanda = Demanda.query.filter_by(id = id).first_or_404()
    return render_template("editar_demanda.html", demanda = demanda, categorias = [i for i in CategoriaDemanda])
 
@app.route("/editar_demanda/<int:id>", methods=["GET", "POST"])
@login_required
def editarDemanda(id):
    if request.method == "POST":
        form = CadastroDemandaForm(meta={'csrf' : False})
        demanda = Demanda.query.filter_by(id = id).first_or_404()
        if form.validate_on_submit():
            demanda.titulo = form.titulo.data
            demanda.descricao = form.descricao.data
            demanda.categoria = CategoriaDemanda(form.categoria.data).name
            db.session.commit()
            flash("Editado com sucesso.")
            demandas = Demanda.query.all()
            return render_template("listar_demandas.html", demandas = demandas)
        else:
            for erro in form.errors.items():
                flash(str(erro[0]) + ": " + str(erro[1]))
            demanda = Demanda.query.filter_by(id = id).first_or_404()
            return render_template("editar_demanda.html", demanda = demanda, categorias = [i for i in CategoriaDemanda])
    if request.method == "GET":
        return render_template("home.html")

@app.route("/excluir_demanda/<int:id>")
@login_required
def excluirDemanda(id):
    demanda = Demanda.query.filter_by(id = id).first_or_404()
    demanda.status = Status.CANCELADA
    db.session.commit()
    flash("Demanda excluida com sucesso.")
    demandas = Demanda.query.all()
    return render_template("listar_demandas.html", demandas = demandas)

@app.route("/acompanhamento")
@login_required
def redirecionaAcompanhamento():
    demandas = Demanda.query.filter_by(usuario_demandante = current_user, status = Status.CANCELADA)
    return render_template("acompanhamento.html", demandas = demandas)

if __name__ == "__main__":
    app.run(debug=True)