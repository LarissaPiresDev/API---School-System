
from turma.turmas_model import listarTurmas
from datetime import datetime, date
from config import db

class Professores(db.Model):
    __tablename__ = "professores"
    
    id = db.Column (db.Integer, primary_key=True)
    nome = db.Column (db.String(100), nullable=False)
    idade = db.Column (db.Integer, nullable=False)
    data_nascimento = db.Column (db.Date, nullable=False)
    

    turma = db.relationship("Turma", back_populates="professores")
    turma_id = db.Column (db.Integer, db.ForeignKey("turmas.id"), nullable=False)
    
    def __init__ (self, nome, idade, turma, turma_id):
        self.nome = nome
        self.idade =  idade
        self.turma = turma
        self.turma_id = turma_id
    

class ProfessorNaoEncontrado(Exception):
    pass

class ProfessorIdNaoInteiro(Exception):
    pass

class ProfessorIdMenorQueUm(Exception):
    pass

def listar_professores():
    return users["Professores"]

def listar_professor_por_id(id):
    try:
        id = int(id)
    except ValueError:
        raise ProfessorIdNaoInteiro
    if id <= 0:
        raise ProfessorIdMenorQueUm
    professores = users['Professores']
    for professor in professores:
        if professor['id'] == id:
            return professor
    raise ProfessorNaoEncontrado

def criar_professor(novo_professor):
    id_novo = max([professor['id'] for professor in users['Professores']]) + 1
    novo_professor['id'] = id_novo
    users["Professores"].append(novo_professor)
    return novo_professor

def atualizar_professor(id, prof_atualizado):
    professor = listar_professor_por_id(id)
    professor.update(prof_atualizado)
    
def deletar_professor(id):
    professor = listar_professor_por_id(id)
    users["Professores"].remove(professor)