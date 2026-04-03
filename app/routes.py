from flask import Blueprint, render_template, request, redirect, url_for, flash
from app import db
from app.models import Paciente, Consulta, Prontuario

bp = Blueprint('main', __name__)

# ============================================================
# FUNCIONALIDADE 1 - CADASTRO DE PACIENTES (AC1)
# ============================================================

@bp.route('/')
@bp.route('/pacientes')
def listar_pacientes():
    pacientes = Paciente.query.all()
    return render_template('pacientes/lista.html', pacientes=pacientes)


@bp.route('/pacientes/novo', methods=['GET', 'POST'])
def novo_paciente():
    if request.method == 'POST':
        paciente = Paciente(
            nome=request.form['nome'],
            cpf=request.form['cpf'],
            telefone=request.form['telefone'],
            email=request.form['email'],
            nascimento=request.form['nascimento']
        )
        db.session.add(paciente)
        db.session.commit()
        return redirect(url_for('main.listar_pacientes'))
    return render_template('pacientes/form.html', paciente=None)


@bp.route('/pacientes/editar/<int:id>', methods=['GET', 'POST'])
def editar_paciente(id):
    paciente = Paciente.query.get_or_404(id)

    if request.method == 'POST':
        paciente.nome = request.form['nome']
        paciente.cpf = request.form['cpf']
        paciente.telefone = request.form['telefone']
        paciente.email = request.form['email']
        paciente.nascimento = request.form['nascimento']
        db.session.commit()
        return redirect(url_for('main.listar_pacientes'))

    return render_template('pacientes/form.html', paciente=paciente)


@bp.route('/pacientes/deletar/<int:id>')
def deletar_paciente(id):
    paciente = Paciente.query.get_or_404(id)
    db.session.delete(paciente)
    db.session.commit()
    return redirect(url_for('main.listar_pacientes'))


# ================================================================
# FUNCIONALIDADE 2 - AGENDAMENTO DE CONSULTAS (AC2)
# ================================================================

@bp.route('/consultas')
def listar_consultas():
    consultas = Consulta.query.all()
    return render_template('consultas/lista.html', consultas=consultas)

@bp.route('/consultas/nova', methods=['GET', 'POST'])
def nova_consulta():
    pacientes = Paciente.query.all()
    if request.method == 'POST':
        consulta = Consulta(
            paciente_id=request.form['paciente_id'],
            data=request.form['data'],
            hora=request.form['hora'],
            dentista=request.form['dentista'],
            observacao=request.form['observacao'],
            valor=float(request.form['valor'] or 0),
            status_pag='pendente'
        )
        db.session.add(consulta)
        db.session.commit()
        return redirect(url_for('main.listar_consultas'))
    return render_template('consultas/form.html', pacientes=pacientes, consulta=None)

@bp.route('/consultas/editar/<int:id>', methods=['GET', 'POST'])
def editar_consulta(id):
    consulta = Consulta.query.get_or_404(id)
    pacientes = Paciente.query.all()
    if request.method == 'POST':
        consulta.paciente_id = request.form['paciente_id']
        consulta.data = request.form['data']
        consulta.hora = request.form['hora']
        consulta.dentista = request.form['dentista']
        consulta.observacao = request.form['observacao']
        consulta.valor = float(request.form['valor'] or 0)
        db.session.commit()
        return redirect(url_for('main.listar_consultas'))
    return render_template('consultas/form.html', pacientes=pacientes, consulta=consulta)

@bp.route('/consultas/deletar/<int:id>')
def deletar_consulta(id):
    consulta = Consulta.query.get_or_404(id)
    db.session.delete(consulta)
    db.session.commit()
    return redirect(url_for('main.listar_consultas'))

# ================================================================
# FUNCIONALIDADE 3 - PRONTUARIO / HISTORICO (AC3)
# ================================================================

@bp.route('/prontuario')
def listar_prontuario():
    consultas = Consulta.query.all()
    return render_template('prontuario/lista.html', consultas=consultas)

@bp.route('/prontuario/novo/<int:consulta_id>', methods=['GET', 'POST'])
def novo_prontuario(consulta_id):
    consulta = Consulta.query.get_or_404(consulta_id)
    if request.method == 'POST':
        pront = Prontuario(
            consulta_id=consulta_id,
            descricao=request.form['descricao'],
            tratamento=request.form['tratamento'],
            data_reg=request.form['data_reg']
        )
        db.session.add(pront)
        db.session.commit()
        return redirect(url_for('main.listar_prontuario'))
    return render_template('prontuario/form.html', consulta=consulta)

@bp.route('/prontuario/editar/<int:id>', methods=['GET', 'POST'])
def editar_prontuario(id):
    prontuario = Prontuario.query.get_or_404(id)
    consulta = Consulta.query.get_or_404(prontuario.consulta_id)
    if request.method == 'POST':
        prontuario.descricao = request.form['descricao']
        prontuario.tratamento = request.form['tratamento']
        prontuario.data_reg = request.form['data_reg']
        db.session.commit()
        return redirect(url_for('main.listar_prontuario'))
    return render_template('prontuario/form.html', consulta=consulta, prontuario=prontuario)

@bp.route('/prontuario/deletar/<int:id>')
def deletar_prontuario(id):
    prontuario = Prontuario.query.get_or_404(id)
    db.session.delete(prontuario)
    db.session.commit()
    return redirect(url_for('main.listar_prontuario'))

# ================================================================
# FUNCIONALIDADE 4 - CONTROLE FINANCEIRO (FINAL)
# ================================================================

@bp.route('/financeiro')
def financeiro():
    consultas = Consulta.query.all()
    total = sum(c.valor for c in consultas)
    recebido = sum(c.valor for c in consultas if c.status_pag == 'pago')
    pendente = sum(c.valor for c in consultas if c.status_pag == 'pendente')
    return render_template('financeiro/lista.html',
                           consultas=consultas,
                           total=total,
                           recebido=recebido,
                           pendente=pendente)

@bp.route('/financeiro/pagar/<int:id>')
def marcar_pago(id):
    consulta = Consulta.query.get_or_404(id)
    consulta.status_pag = 'pago'
    db.session.commit()
    return redirect(url_for('main.financeiro'))
