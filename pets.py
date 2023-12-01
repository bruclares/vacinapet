from flask import (
    Blueprint, render_template, request, session, flash, redirect, url_for
)
from .db import get_db

bp = Blueprint('pets', __name__, url_prefix='/pets')


@bp.route('/', methods=('GET', 'POST'))
def lista():
    tutor_id = session.get('tutor_id')
    with get_db() as conn:
        with conn.cursor() as curs:
            curs.execute(
                'SELECT * FROM pet WHERE tutor_id = %s',
                (tutor_id,)
            )
            pets = curs.fetchall()

    return render_template('pets/meuspets.html', pets=pets)


@bp.route('/criar', methods=('GET', 'POST'))
def criar():
    if request.method == 'POST':
        tutor_id = session.get('tutor_id')
        nome = request.form['nome'].title()
        especie = request.form['especie'].title()
        genero = request.form['genero'].title()
        peso = request.form['peso']
        idade = request.form['idade']
        castrado = request.form['castrado'] if "castrado" in request.form else '0'

        error = None

        if not nome:
            error = 'O nome é obrigatório.'
            flash(error)
        elif not especie:
            error = 'A espécie é obrigatória.'
            flash(error)
            
        if error is None:
            with get_db() as conn:
                with conn.cursor() as curs:
                    curs.execute(
                        '''INSERT INTO pet (tutor_id, nome, especie, genero,
                         peso, idade, castrado) VALUES
                           (%s, %s, %s, %s, %s, %s, %s)''',
                        (tutor_id, nome, especie, genero, peso, idade, 
                         castrado))
            return redirect(url_for('pets.lista'))

    return render_template('pets/criar.html')
