from flask import Blueprint, render_template, redirect, url_for, flash, current_app
from models import Musics, PlayList, db
from flask_login import current_user
from utils.form import FormMusicas, FormPlaylist, FormAddMusicPlaylist
from flask_login import login_required
import os


home = Blueprint('home', __name__)

@home.route('/', methods=['GET', 'POST'])
@login_required
def index():
    musicas = Musics.query.all()
    formM = FormMusicas()
    formP = FormPlaylist()
    formPM = FormAddMusicPlaylist()
    return render_template('home.html', musics=musicas, formM=formM, formP=formP, formPM=formPM, is_home_page=True)


@home.route('/playlists', methods=['POST', 'GET'])
@login_required
def playlist():
    form = FormAddMusicPlaylist()
    playlist = PlayList.query.filter_by(user_id=current_user.id).all()
    return render_template('playlist_list.html', playlist=playlist, form=form)

@home.route('/playlist_musics/<int:playlist_id>', methods=['POST', 'GET'])
@login_required
def playlist_musicas(playlist_id):
    playlist = PlayList.query.get(playlist_id)
    if not playlist:
        flash('Playlist não encontrada !')
        return redirect(url_for('home.index'))
    
    musics = playlist.musics
    return render_template('playlist_musics.html', playlist=playlist, musics=musics)


@home.route('/my_musics/<int:user_id>', methods=['POST', 'GET'])
@login_required
def minhas_musicas(user_id):
    musicas = Musics.query.filter_by(upload_user=user_id).all()
    return render_template('minhas_musicas.html', musicas=musicas)


@home.route('/remove_music/<int:music_id>', methods=['POST', 'GET'])
def remover_musica(music_id):
    musica = Musics.query.get(music_id)
    file_music = os.path.join(current_app.root_path, 'static', 'uploads', musica.filename)
    if os.path.exists(file_music):
        os.remove(file_music)
    if musica:
        db.session.delete(musica)
        db.session.commit()
        flash('Musica removida !')
    else:
        flash('Musica não encontrada !')
        return redirect(url_for('home.index'))
    return redirect(url_for('home.minhas_musicas', user_id=current_user.id))
    