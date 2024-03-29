from flask import (
    Blueprint, render_template, request, session, flash, redirect, url_for
)
from ..database.db import get_db

from .auth import login_required

bp = Blueprint('vacinas', __name__,)


@bp.route('/<id_pet>/vacinas', methods=('GET',))
@login_required
def lista(id_pet):
    busca = request.args.get('search')
    query = 'SELECT * FROM vacina WHERE pet_id = %s'
    parameters = (id_pet,)

    if busca:
        query += ' and nome ilike %s'
        parameters += ('%' + (busca if busca else '') + '%',)
        print(parameters)

    with get_db() as conn:
        with conn.cursor() as curs:
            curs.execute(
                query,
                parameters
            )
            vacinas = curs.fetchall()

    if busca and not vacinas:
        vacinas = 'Nenhuma vacina encontrada...'

    return render_template('vacinas/vacinas.html', vacinas=vacinas, pet_id=id_pet)


@bp.route('/<id_pet>/vacinas/incluir', methods=('GET', 'POST'))
@login_required
def incluir(id_pet):
    if request.method == 'POST':
        pet_id = id_pet
        nome = request.form['nome'].title()
        lote = request.form['lote']
        data_aplicacao = request.form['data_aplicacao']
        data_reforco = request.form['data_reforco']
        
        error = None

        if not nome:
            error = 'O nome é obrigatório.'
        elif not lote:
            error = 'O lote é obrigatório.'
        elif not data_aplicacao:
            error = 'A data de aplicação é obrigatória.'
        elif not data_reforco:
            error = 'A data de reforço é obrigatória.'
        elif data_reforco <= data_aplicacao:
            error = 'A data de reforço deve ser maior que a data de aplicação.'

        if error is None:
            with get_db() as conn:
                with conn.cursor() as curs:
                    curs.execute(
                        '''INSERT INTO vacina (pet_id, nome, data_aplicacao,
                            prox_reforco, lote)
                            VALUES (%s, %s, %s, %s, %s)''',
                        (pet_id, nome, data_aplicacao, data_reforco, lote))
            return redirect(url_for('pets.vacinas.lista', id_pet=pet_id))
            
        flash(error)

    return render_template('vacinas/incluir.html')


@bp.route('/<id_pet>/vacinas/<id_vacina>/alterar', methods=('GET', 'POST'))
@login_required
def alterar(id_pet, id_vacina):

    if request.method == 'POST':
        nome = request.form['nome'].title()
        lote = request.form['lote']
        data_aplicacao = request.form['data_aplicacao']
        data_reforco = request.form['data_reforco']
        
        error = None

        if not nome:
            error = 'O nome é obrigatório.'
        elif not lote:
            error = 'O lote é obrigatório.'
        elif not data_aplicacao:
            error = 'A data da aplicacao é obrigatória.'
        elif not data_reforco:
            error = 'A data do reforço é obrigatória.'
        elif data_reforco <= data_aplicacao:
            error = 'A data de reforço deve ser maior que a data de aplicação.'

        if error is None:
            with get_db() as conn:
                with conn.cursor() as curs:
                    curs.execute(
                        '''UPDATE vacina SET nome = %s, data_aplicacao = %s,
                        prox_reforco = %s, lote = %s WHERE id = %s ''',
                        (nome, data_aplicacao, data_reforco, lote, id_vacina))
            # o redirect espera uma url que é retornada pela função url_for
            # a forma de escrita do parametro para a url_for é <controller>.<função>
            # analisar se é um filho e adicionar o controller pai <controller_pai>.<controller_filho>.<função>
            return redirect(url_for('pets.vacinas.lista', id_pet=id_pet))

        flash(error)

    with get_db() as conn:
        with conn.cursor() as curs:
            curs.execute(
                'SELECT * FROM vacina WHERE id = %s',
                (id_vacina,)
            )
            vacina = curs.fetchone()

    return render_template('vacinas/alterar.html', vacina=vacina)


@bp.route('/<id_pet>/vacinas/<id_vacina>/excluir', methods=('GET',))
@login_required
def excluir(id_pet, id_vacina):
    with get_db() as conn:
        with conn.cursor() as curs:
            curs.execute(
                'DELETE FROM vacina WHERE id = %s',
                (id_vacina,)
            )
    return redirect(url_for('pets.vacinas.lista', id_pet=id_pet))

