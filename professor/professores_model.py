users = {
    "Professores": [
        {"id": 1, "nome": "Simonica", "idade": 34, "materia": "matematica", "salario": 3500.00},
        {"id": 2, "nome": "Ione", "idade": 35, "materia": "portugues", "salario": 3800.00},
        {"id": 3, "nome": "Francisco", "idade": 74, "materia": "Ed. Fisica", "salario": 5200.00},
        {"id": 4, "nome": "Daniel", "idade": 74, "materia": "Historia", "salario": 1800.00},
        {"id": 5, "nome": "Mariana", "idade": 28, "materia": "Artes", "salario": 3200.00},
        {"id": 6, "nome": "Patricia", "idade": 34, "materia": "Quimica", "salario": 4200.00},
        {"id": 7, "nome": "Maria", "idade": 67, "materia": "Portugues", "salario": 1900.00}
    ]
}

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