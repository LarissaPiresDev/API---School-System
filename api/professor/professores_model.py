from turma.turmas_model import Turma
from config import db


class Professor(db.Model):
    __tablename__ = "professores"

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    idade = db.Column(db.Integer, nullable=False)
    materia = db.Column(db.String(50), nullable=True)
    salario = db.Column(db.Float, nullable=True)

    turmas = db.relationship("Turma", back_populates="professor")

    def __init__(self, nome, idade, materia, salario):
        self.nome = nome
        self.idade = idade
        self.materia = materia
        self.salario = salario
        
    def to_dict(self):
        return {'id': self.id, 'nome': self.nome, 'idade': self.idade, 'materia': self.materia, 'salario': self.salario}
    
    

# Exceções personalizadas
class ProfessorNaoEncontrado(Exception): 
    pass
class ProfessorIdNaoInteiro(Exception): 
    pass
class ProfessorIdMenorQueUm(Exception): 
    pass

# CRUD
def listar_professores():
    professores = Professor.query.all()
    return [professor.to_dict() for professor in professores]

def listar_professor_por_id(id):
    try:
        id = int(id)
    except ValueError:
        raise ProfessorIdNaoInteiro
    if id <= 0:
        raise ProfessorIdMenorQueUm

    professor = Professor.query.get(id)
    if not professor:
        raise ProfessorNaoEncontrado
    
    return professor.to_dict()

def criar_professor (novo_professor):
    new_professor = Professor(
        nome=str(novo_professor['nome']), 
        idade=int(novo_professor['idade']),
        materia=str(novo_professor['materia']),
        salario=float(novo_professor['salario'])
        
    )
    
    db.session.add(new_professor)
    db.session.commit()
    


def atualizar_professor(id, professor_atualizado):
    try:
        id = int(id)
    except ValueError:
        raise ProfessorIdNaoInteiro
    if id <= 0:
        raise ProfessorIdMenorQueUm

    professor = Professor.query.get(id)
    if not professor:
        raise ProfessorNaoEncontrado
    
    
    professor.nome=professor_atualizado['nome']
    professor.idade=professor_atualizado['idade']
    professor.materia=professor_atualizado['materia']
    professor.salario=professor_atualizado['salario']
    
    db.session.commit()

def deletar_professor(id):
    try:
        id = int(id)
    except ValueError:
        raise ProfessorIdNaoInteiro
    if id <= 0:
        raise ProfessorIdMenorQueUm

    professor = Professor.query.get(id)
    if not professor:
        raise ProfessorNaoEncontrado
    db.session.delete(professor)
    db.session.commit()
