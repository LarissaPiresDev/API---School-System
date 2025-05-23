from turma.turmas_model import Turma
from datetime import datetime, date
from config import db

class Aluno(db.Model):
    __tablename__= 'alunos'
    
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(150), nullable=False)
    idade = db.Column(db.Integer, nullable=False)
    data_nascimento = db.Column(db.Date, nullable=False)
    nota_primeiro_semestre = db.Column(db.Float, nullable=True)
    nota_segundo_semestre = db.Column(db.Float, nullable=True)
    media_final = db.Column(db.Float, nullable=True)

    turma_id = db.Column(db.Integer, db.ForeignKey("turmas.id"), nullable=False)
    turma = db.relationship("Turma", back_populates="alunos")
    
    def __init__(self, nome, data_nascimento, nota_primeiro_semestre, nota_segundo_semestre, turma_id):
        self.nome = nome
        self.data_nascimento = data_nascimento
        self.nota_primeiro_semestre = nota_primeiro_semestre
        self.nota_segundo_semestre = nota_segundo_semestre
        self.media_final = self.calcular_media_final()
        self.turma_id = turma_id
        self.idade = self.calcular_idade()
        
    def calcular_idade(self):
        hoje = date.today()
        return hoje.year - self.data_nascimento.year - ((hoje.month, hoje.day) < (self.data_nascimento.month, self.data_nascimento.day))
    
    def calcular_media_final(self):
        media = (self.nota_primeiro_semestre + self.nota_segundo_semestre) / 2
        return media
    
    def to_dict(self):
        return{'id': self.id, 'nome':self.nome, 'turma_id': self.turma_id, 'idade': self.idade,'data_nascimento': self.data_nascimento.strftime("%Y-%m-%d"), 'nota primeiro semestre': self.nota_primeiro_semestre, 'nota segundo semestre': self.nota_segundo_semestre, 'media final': self.media_final}      
        
class AlunoNaoEncontrado(Exception):
    pass

class AlunoIdNaoInteiro(Exception):
    pass

class AlunoIdMenorQueUm(Exception):
    pass

def listar_alunos():
    alunos = Aluno.query.all()
    return [aluno.to_dict() for aluno in alunos]

def aluno_por_id(id):
    try:
        id = int(id)
    except ValueError:
        raise AlunoIdNaoInteiro
    if id <= 0:
        raise AlunoIdMenorQueUm
    
    aluno = Aluno.query.get(id)
    if not aluno:
        raise AlunoNaoEncontrado
    return aluno.to_dict()

def criar_aluno(novo_aluno):
    from turma.turmas_model import Turma
    turma = Turma.query.get(novo_aluno['turma_id'])
    if not turma:
        raise TurmaNaoEncontrada
    
    if isinstance(novo_aluno['data_nascimento'], str):
        data_nascimento = datetime.strptime(novo_aluno['data_nascimento'], "%Y-%m-%d").date()
    else:
        data_nascimento = novo_aluno['data_nascimento']
    new_aluno = Aluno(
        nome=str(novo_aluno['nome']),
        data_nascimento=data_nascimento,
        nota_primeiro_semestre=float(novo_aluno['nota_primeiro_semestre']),
        nota_segundo_semestre=float(novo_aluno['nota_segundo_semestre']),
        turma_id=int(novo_aluno['turma_id'])
    )
    
    db.session.add(new_aluno)
    db.session.commit()
    return new_aluno.to_dict()

def atualizar_aluno(id, aluno_atualizado):
    try:
        id = int(id)
    except ValueError:
        raise AlunoIdNaoInteiro
    if id <= 0:
        raise AlunoIdMenorQueUm
    
    aluno = Aluno.query.get(id)
    if not aluno:
        raise AlunoNaoEncontrado
    if 'turma_id' in aluno_atualizado:
        turma = Turma.query.get(aluno_atualizado['turma_id'])
        if not turma:
            raise TurmaNaoEncontrada
    
    if 'nome' in aluno_atualizado:
        aluno.nome = aluno_atualizado['nome']
    if 'data_nascimento' in aluno_atualizado:
        aluno.data_nascimento = aluno_atualizado['data_nascimento']
    if 'nota_primeiro_semestre' in aluno_atualizado:
        aluno.nota_primeiro_semestre = aluno_atualizado['nota_primeiro_semestre']
    if 'nota_segundo_semestre' in aluno_atualizado:
        aluno.nota_segundo_semestre = aluno_atualizado['nota_segundo_semestre']
    aluno.media_final = aluno.calcular_media_final()
    if 'turma_id' in aluno_atualizado:
        aluno.turma_id = aluno_atualizado['turma_id']
    aluno.idade = aluno.calcular_idade()
    
    db.session.commit()

def deletar_aluno(id):
    try:
        id = int(id)
    except ValueError:
        raise AlunoIdNaoInteiro
    if id <= 0:
        raise AlunoIdMenorQueUm
    
    aluno = Aluno.query.get(id)
    if not aluno:
        raise AlunoNaoEncontrado
    
    db.session.delete(aluno)
    db.session.commit()

class TurmaNaoEncontrada(Exception):
    pass