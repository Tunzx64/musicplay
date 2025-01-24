# Primeira vez usando relações entre tabelas no banco de dados
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

db = SQLAlchemy()

class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    name = db.Column(db.String(250), nullable=False)
    email = db.Column(db.String(250), nullable=False, unique=True)
    password = db.Column(db.String(250), nullable=False)
    ip_adress = db.Column(db.String(250), nullable=False)
    # Relação entre musicas
    musics = db.relationship('Musics', backref='uploader', lazy=True)
    # Relação entre playlist
    playlist = db.relationship('PlayList', backref='onwer', lazy=True)
    
# Tabela intermediaria entre a playlist e as musicas para que a playlist possa ter varias musicas e uma musica possa estar em varias playlists
playlist_music = db.Table('playlist_music',
    db.Column('music_id',db.Integer, db.ForeignKey('musics.id'), primary_key=True),
    db.Column('playlist_id',db.Integer, db.ForeignKey('playlists.id'), primary_key=True)
)
class Musics(db.Model):
    __tablename__ = 'musics'
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    title = db.Column(db.String(250), nullable=False)
    filename = db.Column(db.String(250), nullable=False)
    # ID do usuario que fez upload da musica
    upload_user = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    # A que playlist esta musica pertence
    playlist = db.relationship('PlayList', secondary=playlist_music, back_populates ='musics')

class PlayList(db.Model):
    __tablename__ = 'playlists'
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    title = db.Column(db.String(250), nullable=False)
    # Esta se referindo a tabela User
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    # Esta se referindo a tabela Musics, isso fara com que minha playlist se comunique com a tabela musics entre a tabela intermediaria
    musics = db.relationship('Musics', secondary=playlist_music, back_populates ='playlist')
                                                                 # back_populates serve para fazer a comunicação entre atributos de tabelas entre tabelas usando os nomes dos atributos para fazer isso 
"""

    Explicação do oque eu aprendi
    1 - No codigo db.ForeignKey('musics.id') eu não me referencio ao nome da classe Musics e sim ao nome da tabela '__tablename__' que no caso
    o SQLAlchemy já escreve automaticamente para musics que no caso eu irei ta acessando o atributo id dessa tabela

    2 - O backref é uma forma de criar uma relação reversa automaticamente entre as tabelas. Ou seja, ao definir um backref em um relacionamento, você está criando um acesso de volta ao objeto relacionado, sem precisar definir explicitamente a relação no outro modelo.
    Exemplo: 
    2.1 - musics = db.relationship('Musics', backref='users', lazy=True)
            No modelo User, você está criando um relacionamento com a tabela Musics. Quando você define o backref='users', o SQLAlchemy cria um atributo users automaticamente no modelo Musics, permitindo que você acesse o usuário associado a cada música.

            Quando você usa user.musics, você obtém todas as músicas associadas a um usuário.
            Quando você usa music.users, você obtém o usuário que fez o upload da música.
            Isso significa que o backref='users' em User cria um acesso reverso em Musics, para você poder saber facilmente qual é o usuário que fez o upload daquela música

"""
    