from flask import (
    Blueprint, render_template, request, session, flash, redirect, url_for
)
from ..database.db import get_db

from .auth import login_required

bp = Blueprint('pets', __name__, url_prefix='/pets')


@bp.route('/', methods=('GET',))
@login_required
def lista():
    busca = request.args.get('search')
    query = 'SELECT * FROM pet WHERE tutor_id = %s'
    parameters = (session.get('tutor_id'),)

    if busca:
        query += ' and nome ilike %s'
        parameters += ('%' + (busca if busca else '') + '%',)
      
    with get_db() as conn:
        with conn.cursor() as curs:
            curs.execute(
                query,
                parameters
            )
            pets = curs.fetchall()
    
    if busca and not pets:
        pets = 'Nenhum pet encontrado...'
    
    return render_template('pets/meuspets.html', pets=pets)


@bp.route('/criar', methods=('GET', 'POST'))
@login_required
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
        elif not especie:
            error = 'A espécie é obrigatória.'
        elif not peso:
            error = 'O peso é obrigatório.'
        elif not idade:
            error = 'A idade é obrigatória.'

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
        
        flash(error)

    return render_template('pets/criar.html')


@bp.route('<id>/alterar', methods=('GET', 'POST'))
@login_required
def alterar(id):
    pet_id = id
    if request.method == 'POST':
        nome = request.form['nome'].title()
        especie = request.form['especie'].title()
        genero = request.form['genero'].title()
        peso = request.form['peso']
        idade = request.form['idade']
        castrado = request.form['castrado'] if "castrado" in request.form else '0'

        error = None

        if not nome:
            error = 'O nome é obrigatório.'
        elif not especie:
            error = 'A espécie é obrigatória.'
        elif not peso:
            error = 'O peso é obrigatório.'
        elif not idade:
            error = 'A idade é obrigatória.'

        if error is None:
            with get_db() as conn:
                with conn.cursor() as curs:
                    curs.execute(
                        '''UPDATE pet SET nome = %s, especie = %s, genero = %s,
                        peso = %s, idade = %s, castrado = %s WHERE id = %s ''',
                        (nome, especie, genero, peso, idade, castrado, pet_id))
            return redirect(url_for('pets.lista'))
        
        flash(error)

    with get_db() as conn:
        with conn.cursor() as curs:
            curs.execute(
                'SELECT * FROM pet WHERE id = %s',
                (pet_id,)
            )
            pet = curs.fetchone()

    return render_template('pets/alterar.html', pet=pet)


@bp.route('/<int:id>/excluir', methods=('GET',))
@login_required
def excluir(id):
    with get_db() as conn:
        with conn.cursor() as curs:
            curs.execute(
                'DELETE FROM pet WHERE id = %s',
                (id,)
            )
    return redirect(url_for('pets.lista'))
