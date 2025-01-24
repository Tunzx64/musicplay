from flask import Blueprint, render_template, url_for, redirect, flash
from models import db, Musics, PlayList
from utils.form import FormMusicas, FormPlaylist, FormAddMusicPlaylist
import uuid, os
from werkzeug.utils import secure_filename
from flask_login import current_user, login_required
import magic

setup_musics = Blueprint('music_setup', __name__)
UPLOAD_MUSICS = os.path.join('static', 'uploads')
MAX_FILE_SIZE_MB = 20

@setup_musics.route('/add_music', methods=['POST', 'GET'])
@login_required
def adicionar_musica():
    form = FormMusicas()
    if form.validate_on_submit(): 
        title = form.title.data
        file = form.filename.data
        
        if file:
            # Verificações de Segurança
            file_magic = magic.Magic(mime=True)
            file_type = file_magic.from_buffer(file.read()) 
            file.seek(0)

            if not file_type.startswith('audio'):
                flash('O arquivo não é um tipo de áudio válido.')
                return redirect(url_for('home.index'))

            valid_extensions = ['.mp3', '.wav', '.flac', '.ogg', '.aac']
            _, ext = os.path.splitext(file.filename)
            if ext.lower() not in valid_extensions:
                flash('A extensão do arquivo não é válida para uma música.')
                return redirect(url_for('home.index'))
        
            file_size_mb = len(file.read()) / (1024 * 1024)
            file.seek(0) 
            if file_size_mb > MAX_FILE_SIZE_MB:
                flash(f'O arquivo é muito grande! O tamanho máximo permitido é {MAX_FILE_SIZE_MB} MB.')

                return redirect(url_for('home.index'))
            filename = f'{uuid.uuid4().hex}_{secure_filename(file.filename)}'
            file_path = os.path.join(UPLOAD_MUSICS, filename)
            file.save(file_path)
            if Musics.query.filter_by(title=title).first():
                flash('Já existe uma musica com esse nome !')
                return redirect(url_for('home.index'))
            
            new_music = Musics(title=title, filename=filename, upload_user=current_user.id)
            db.session.add(new_music)
            db.session.commit()
            flash('Musica adicionada com sucesso !')
            return redirect(url_for('home.index'))
        else:
            flash('Escolha um arquivo !')
            return redirect(url_for('home.index'))      
    return

@setup_musics.route('/created_playlist', methods=['POST', 'GET'])
@login_required
def criar_playlist():
    form = FormPlaylist()
    if form.validate_on_submit():
        title = form.title.data
        if PlayList.query.filter_by(title=title).first():
            flash('Já existe uma playlist com esse nome !')
            return redirect(url_for('home.index'))
        new_playlist = PlayList(title=title, user_id=current_user.id)
        db.session.add(new_playlist)
        db.session.commit()
        flash('Playlist salva agora adicione musicas a essa playlist !')
        return redirect(url_for('home.index'))
    return

@setup_musics.route('/delet_playlist/<int:playlist_id>', methods=['POST', 'GET'])
def deletar_playlist(playlist_id):
    playlist = PlayList.query.get(playlist_id)
    if playlist:
        db.session.delete(playlist)
        db.session.commit()
        flash('PlayList Excluida !')
        return redirect(url_for('home.playlist'))
    else:
        flash('PlayList não existe !')
        return redirect(url_for('home.index'))

@setup_musics.route('/remove_music_playlist/<int:playlist_id>/<int:music_id>', methods=['POST', 'GET'])
def remover_music_playlist(playlist_id, music_id):
    playlist = PlayList.query.get(playlist_id)
    music = Musics.query.get(music_id)
    if music in playlist.musics:
        playlist.musics.remove(music)
        db.session.commit()
        flash('Musica removida da PlayList !')
        return redirect(url_for('home.playlist_musicas', playlist_id=playlist.id))
    else:
        flash('Essa musica não esta na playlist !')
        return redirect(url_for('home.index'))

@setup_musics.route('/add_playlist/<int:music_id>', methods=['POST', 'GET'])
@login_required
def adicionar_musica_playlist(music_id):
    music = Musics.query.get(music_id)
    if not music_id:
        flash('Musica não encontrada !')
        return redirect(url_for('home.index'))
    
    formPM = FormAddMusicPlaylist()
    playlist = PlayList.query.filter_by(user_id=current_user.id).all()
    formPM.playlist_id.choices = [(play.id, play.title) for play in playlist]

    if formPM.validate_on_submit():
        playlist_id = formPM.playlist_id.data
        select_playlist = PlayList.query.get(playlist_id)
        if select_playlist:
            if music not in select_playlist.musics:
                select_playlist.musics.append(music)
                db.session.commit()
                flash('Musica adicionada a playlist !')
                return redirect(url_for('home.index'))
            else:
                flash('Esta musica já esta na playlist !')
                return redirect(url_for('home.index'))
        else:
            flash('Playlist não encontrada')
            return redirect(url_for('home.index'))

    return render_template('add_playlist.html', formPM=formPM)
