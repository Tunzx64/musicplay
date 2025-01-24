from flask import Flask
from config import Config
from models import db, User
from flask_login import LoginManager
from routes.home import home
from routes.setup_users import setup_users
from routes.setup_musics import setup_musics

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

app.register_blueprint(setup_users)                                 
app.register_blueprint(home)
app.register_blueprint(setup_musics)

# Configurando flask_login
login_manager = LoginManager(app)
login_manager.login_view = 'user_setup.logar_user'
login_manager.login_message = None
@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(host="0.0.0.0", port=5000)
