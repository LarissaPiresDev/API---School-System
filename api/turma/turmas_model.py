from datetime import datetime
from config import db


class Turma(db.Model):
    __tablename__  = "turmas"
    id = db.Column(db.Integer, primary_key=True)
    descricao = db.Column(db.String(50), nullable=False)
    ativo = db.Column(db.Boolean, default=False)
    
    alunos = db.relationship("Aluno", back_populates='turma')
    professor_id = db.Column(db.Integer, db.ForeignKey("professores.id"), nullable=False)
    professor = db.relationship("Professor", back_populates='turmas')
    
    def __init__(self, descricao, ativo, professor_id):
        self.descricao = descricao
        self.ativo = ativo
        self.professor_id = professor_id
        
    def to_dict(self):
        return {'id': self.id, 'descricao': self.descricao, 'professor_id': self.professor_id, 'ativo': self.ativo}
    
    
    

class TurmaNaoEncontrada(Exception):
    pass

class TurmaIdNaoInteiro(Exception):
    pass

class TurmaIdMenorQueUm(Exception):
    pass

class turmaDescricaoJaExiste(Exception):
    pass

class ProfessorJaEstaEmUmaSala(Exception):
    pass

def listarTurmas():
    turmas = Turma.query.all()
    return [turma.to_dict() for turma in turmas]

def listarTurmaPorId(id):
    try:
        id = int(id)
    except ValueError:
        raise TurmaIdNaoInteiro
    
    if id <= 0:
        raise TurmaIdMenorQueUm
    
    turma = Turma.query.get(id)
    if not turma:
        raise TurmaNaoEncontrada
    return turma.to_dict()

def deletarTurma(id):
    try:
        id = int(id)
    except ValueError:
        raise TurmaIdNaoInteiro
    
    if id <= 0:
        raise TurmaIdMenorQueUm
    
    turma = Turma.query.get(id)
    if not turma:
        raise TurmaNaoEncontrada

    db.session.delete(turma)
    db.session.commit()
    
def criarturma(nova_turma):
    from professor.professores_model import Professor
    turmas = Turma.query.all()
    for turma in turmas:
        turma_dict = turma.to_dict()
        if nova_turma['descricao'].strip().lower() == turma_dict['descricao'].strip().lower():
            raise turmaDescricaoJaExiste
        
        if turma_dict['professor_id'] == nova_turma['professor_id']:
            raise ProfessorJaEstaEmUmaSala
        
    new_turma = Turma(
        descricao = nova_turma['descricao'],
        professor_id = nova_turma['professor_id'],
        ativo = nova_turma['ativo']
        )
    
    db.session.add(new_turma)
    db.session.commit()
    return new_turma.to_dict()
    
    
def atualizar_turma(id, turma_atualizada):
    from professor.professores_model import Professor

    try:
        id = int(id)
    except ValueError:
        raise TurmaIdNaoInteiro
    
    if id <= 0:
        raise TurmaIdMenorQueUm

    
    turmas = Turma.query.all()
    
    turma = Turma.query.get(id)
    if not turma:
        raise TurmaNaoEncontrada

    for clas in turmas:
        turma_dict = clas.to_dict()

        if turma_atualizada['descricao'].strip().lower() == turma_dict['descricao'].strip().lower():
            raise turmaDescricaoJaExiste        
        if turma_dict['professor_id'] == turma_atualizada['professor_id'] and id != turma_dict['id']:
            raise ProfessorJaEstaEmUmaSala

    
    turma.descricao = turma_atualizada['descricao']
    turma.professor_id = turma_atualizada['professor_id']
    turma.ativo = turma_atualizada['ativo']
    
    db.session.commit()
    
    
class ProfessorNaoEncontrado(Exception):
    pass

def achar_professor(professor_id):
    from professor.professores_model import Professor
    professores = Professor.query.all()
    for professor in professores:
        professor = professor.to_dict()
        if professor['id'] == professor_id:
            return True
    raise ProfessorNaoEncontrado
        