import functools
import psycopg2
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash
from ..database.db import get_db

bp = Blueprint('auth', __name__)


@bp.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        nome = request.form['nome'].title()
        senha = request.form['senha']
        email = request.form['email']
        telefone = request.form['telefone']

        error = None

        if not nome:
            error = 'O nome é obrigatório.'
        elif not senha:
            error = 'A senha é obrigatória.'
        elif not email:
            error = 'O email é obrigatório.'

        if error is None:
            try:
                with get_db() as conn:
                    with conn.cursor() as curs:
                        curs.execute(
                            '''INSERT INTO tutor (nome, email, telefone, senha) 
                            VALUES (%s, %s, %s, %s)''',
                            (nome, email, telefone, 
                             generate_password_hash(senha))
                        )
            except psycopg2.IntegrityError:
                error = f"Usuário {nome} já está cadastrado."
            else:
                return redirect(url_for("auth.login"))

        flash(error)

    return render_template('auth/register.html')


@bp.route('/', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        email = request.form['email']
        senha = request.form['senha']

        error = None

        if not senha:
            error = 'A senha é obrigatória.'
        elif not email:
            error = 'O email é obrigatório.'

        with get_db() as conn:
            with conn.cursor() as curs:
                curs.execute(
                    'SELECT * FROM tutor WHERE email = %s',
                    (email,)
                )
                tutor = curs.fetchone()

        if tutor is None:
            error = 'Dados incorretos.'

        elif not check_password_hash(tutor[4], senha):
            error = 'Dados incorretos.'

        if error is None:
            session.clear()
            session['tutor_id'] = tutor[0]
            return redirect(url_for('pets.lista'))

        flash(error)
    
    if 'tutor_id' in session:
        return redirect(url_for('pets.lista'))

    return render_template('auth/login.html')


@bp.before_app_request
def load_logged_in_user():
    tutor_id = session.get('tutor_id')

    if tutor_id is None:
        g.tutor = None
    else:
        with get_db() as conn:
            with conn.cursor() as curs:
                curs.execute(
                    'SELECT * FROM tutor WHERE id = %s', (tutor_id,)
                )
                g.tutor = curs.fetchone()


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.tutor is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view


@bp.route('/logout')
@login_required
def logout():
    session.clear()
    return redirect(url_for('auth.login'))