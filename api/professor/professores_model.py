from sqlalchemy import create_engine, Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import declarative_base, relationship, sessionmaker
from datetime import date

# Banco de dados
engine = create_engine("sqlite:///Api.db", echo=True)
Base = declarative_base()
Session = sessionmaker(bind=engine)


# Professor
class Professor(Base):
    __tablename__ = "professores"

    id = Column(Integer, primary_key=True)
    nome = Column(String(100), nullable=False)
    idade = Column(Integer, nullable=False)
    data_nascimento = Column(Date, nullable=False)

    turma_id = Column(Integer, ForeignKey("turmas.id"), nullable=False)
    turma = relationship("Turma", back_populates="professores")

    def __init__(self, nome, idade, data_nascimento, turma_id):
        self.nome = nome
        self.idade = idade
        self.data_nascimento = data_nascimento
        self.turma_id = turma_id

Base.metadata.create_all(engine)

# Exceções personalizadas
class ProfessorNaoEncontrado(Exception): pass
class ProfessorIdNaoInteiro(Exception): pass
class ProfessorIdMenorQueUm(Exception): pass

# CRUD
def listar_professores():
    session = Session()
    professores = session.query(Professor).all()
    session.close()
    return professores

def listar_professor_por_id(id):
    try:
        id = int(id)
    except ValueError:
        raise ProfessorIdNaoInteiro
    if id <= 0:
        raise ProfessorIdMenorQueUm

    session = Session()
    professor = session.query(Professor).get(id)
    session.close()

    if not professor:
        raise ProfessorNaoEncontrado
    return professor

def adicionar_professor(nome, idade, data_nascimento, turma_id):
    session = Session()
    novo_professor = Professor(nome=nome, idade=idade, data_nascimento=data_nascimento, turma_id=turma_id)
    session.add(novo_professor)
    session.commit()
    session.close()

def atualizar_professor(id, dados_atualizados):
    session = Session()
    professor = session.query(Professor).get(id)
    if not professor:
        session.close()
        raise ProfessorNaoEncontrado
    for chave, valor in dados_atualizados.items():
        setattr(professor, chave, valor)
    session.commit()
    session.close()

def deletar_professor(id):
    session = Session()
    professor = session.query(Professor).get(id)
    if not professor:
        session.close()
        raise ProfessorNaoEncontrado
    session.delete(professor)
    session.commit()
    session.close()
