from app import db

class Paciente(db.Model):
    id        = db.Column(db.Integer, primary_key=True)
    nome      = db.Column(db.String(100), nullable=False)
    cpf       = db.Column(db.String(14), unique=True)
    telefone  = db.Column(db.String(20))
    email     = db.Column(db.String(100))
    nascimento = db.Column(db.String(10))
    # Um paciente pode ter varias consultas
    consultas = db.relationship('Consulta', backref='paciente', lazy=True)


class Consulta(db.Model):
    id          = db.Column(db.Integer, primary_key=True)
    paciente_id = db.Column(db.Integer, db.ForeignKey('paciente.id'), nullable=False)
    data        = db.Column(db.String(10), nullable=False)
    hora        = db.Column(db.String(5))
    dentista    = db.Column(db.String(100))
    observacao  = db.Column(db.Text)
    valor       = db.Column(db.Float, default=0.0)
    status_pag  = db.Column(db.String(20), default='pendente')
    # Uma consulta pode ter varias anotacoes no prontuario
    prontuarios = db.relationship('Prontuario', backref='consulta', lazy=True)


class Prontuario(db.Model):
    id          = db.Column(db.Integer, primary_key=True)
    consulta_id = db.Column(db.Integer, db.ForeignKey('consulta.id'), nullable=False)
    descricao   = db.Column(db.Text)
    tratamento  = db.Column(db.Text)
    data_reg    = db.Column(db.String(10))