users = {
        "Alunos": [

        {"id": 101, "nome": "Ana Heloisa", "idade": 13, "turma_id": 11, "data_nascimento": "10-11-2011", "nota_primeiro_semestre": 6.0, "nota_segundo_semestre": 8.0, "media_final": 7.00},

        {"id": 102, "nome": "Cauanny Alencar", "idade": 13, "turma_id": 11, "data_nascimento": "10-06-2011", "nota_primeiro_semestre": 7.5, "nota_segundo_semestre": 8.5, "media_final": 8.00},

        {"id": 103, "nome": "Eduarda Cardoso", "idade": 13, "turma_id": 11, "data_nascimento": "10-08-2011", "nota_primeiro_semestre": 9.0, "nota_segundo_semestre": 7.0, "media_final": 8.00},


        {"id": 104, "nome": "Iara Ricardo", "idade": 12, "turma_id": 12, "data_nascimento": "10-06-2012", "nota_primeiro_semestre": 8.0, "nota_segundo_semestre": 9.0, "media_final": 8.50},

        {"id": 105, "nome": "Wender da Silva", "idade": 12, "turma_id": 12, "data_nascimento": "07-08-2012", "nota_primeiro_semestre": 9.5, "nota_segundo_semestre": 9.0, "media_final": 9.25},

        {"id": 203, "nome": "Yara da Silva", "idade": 12, "turma_id": 12, "data_nascimento": "08-12-2012", "nota_primeiro_semestre": 7.5, "nota_segundo_semestre": 7.5, "media_final": 7.5},


        {"id": 106, "nome": "Arthur Santos", "idade": 12, "turma_id": 13, "data_nascimento": "08-10-2012", "nota_primeiro_semestre": 9.5, "nota_segundo_semestre": 9.5, "media_final": 9.5},

        {"id": 107, "nome": "Isabele Silva", "idade": 12, "turma_id": 13, "data_nascimento": "09-04-2012", "nota_primeiro_semestre": 10.0, "nota_segundo_semestre": 10.0, "media_final": 10.0},

        {"id": 108, "nome": "Paulo Augusto", "idade": 12, "turma_id": 13, "data_nascimento": "28-11-2012", "nota_primeiro_semestre": 8.5, "nota_segundo_semestre": 7.5, "media_final": 8.0}
        
    ]

}

class AlunoNaoEncontrado(Exception):
    pass
    
def listar_alunos():
    return users['Alunos']

def aluno_por_id(id):
    alunos = users['Alunos']
    for aluno in alunos:
        if aluno['id'] == id:
            return aluno
    raise AlunoNaoEncontrado
    
    
   
