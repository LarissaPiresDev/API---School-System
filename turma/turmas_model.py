users = {
    "Turmas": [
        {"id": 11, "descricao": "7 Ano A", "professor_id": 1, "ativo": True},
        {"id": 12, "descricao": "7 Ano B", "professor_id": 2, "ativo": True},
        {"id": 13, "descricao": "7 Ano C", "professor_id": 3, "ativo": False},
    ],

    "Professores": [
        {"id": 1, "nome": "Simonica", "idade": 34, "materia": "matematica", "salario": 3500.00},
        {"id": 2, "nome": "Ione", "idade": 35, "materia": "portugues", "salario": 3800.00},
        {"id": 3, "nome": "Francisco", "idade": 74, "materia": "Ed. Fisica", "salario": 5200.00},
        {"id": 4, "nome": "Daniel", "idade": 74, "materia": "Historia", "salario": 1800.00},
        {"id": 5, "nome": "Mariana", "idade": 28, "materia": "Artes", "salario": 3200.00},
        {"id": 6, "nome": "Patricia", "idade": 34, "materia": "Quimica", "salario": 4200.00},
        {"id": 7, "nome": "Maria", "idade": 67, "materia": "Portugues", "salario": 1900.00}
    ],
}

class TurmaNaoEncontrada(Exception):
    pass

def listarTurmas():
    return users["Turmas"]
