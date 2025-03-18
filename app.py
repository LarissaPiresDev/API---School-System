from flask import Flask, jsonify, request
from users import users

app = Flask(__name__)


#--------------------------------------------PROFESSORES------------------------------------------- #

@app.route('/professores/', methods=['GET'])
@app.route('/professores', methods=['GET'])
def get_professores():
    professores = users['Professores']
    return jsonify(professores)

@app.route('/professores/<id>', methods=['GET'])
def profPorId(id):
    try:
        id = int(id)
    except ValueError:
        return jsonify({'mensagem': 'ID inserido para professor precisa ser um numero inteiro'}), 400
    
    if id <= 0:
        return jsonify({'mensagem': 'ID do professor nao pode ser menor ou igual a que zero'}), 400
    
    professores = users['Professores']
    for professor in professores:
        if professor['id'] == id:
            return jsonify(professor)
            
    return jsonify({'mensagem': 'Professor(a) nao encontrado(a)/inexistente'}), 404

@app.route('/professores', methods=['POST'])
def criar_professor():
    dict = request.json

    if not dict.get('nome') or not dict.get('materia'):
        return jsonify({'mensagem': 'Para criar um novo professor preciso que voce me passe os parâmetros nome e materia'}), 400
    
    if 'idade' not in dict:
        return jsonify({'mensagem': 'Idade e obrigatoria, por favor insira-a'}), 400
    
    if not isinstance(dict['nome'], str) or not isinstance(dict['materia'], str):
        return jsonify({'mensagem': 'Os parametros nome e/ou materia precisam ser do tipo STRING'}), 400
    
    if not isinstance(dict['idade'], int):
        return jsonify({'mensagem': 'Idade precisa ser um número INTEIRO'}), 400
    
    if not isinstance(dict['salario'], (int, float)):
        return jsonify({'mensagem':'O parametro de salário precisa ser um número do tipo float ou int'}), 400

    id_novo = max([professor['id'] for professor in users['Professores']]) + 1
    dict['id'] = id_novo
    users['Professores'].append(dict)

    return jsonify(users['Professores']), 201 
    


# ---------------------------------------------TURMAS------------------------------------------------ #

@app.route('/turmas/', methods=['GET'])
@app.route('/turmas', methods=['GET'])
def get_turmas():
    turmas = users['Turmas']
    return jsonify(turmas)


@app.route('/turmas/<id>', methods=['GET'])
def turmaPorId(id):
    try:
        id = int(id)
    except ValueError:
        return jsonify({'mensagem': 'ID inserido para turma precisa ser um numero inteiro'}), 400
    if id <=0:
        return jsonify({'mensagem': 'ID de turma nao pode ser menor ou igual a que zero'}), 400
    turmas = users['Turmas']
    for turma in turmas:
        if turma['id'] == id:
            return jsonify(turma)
            
    return jsonify({'mensagem': 'Turma nao encontrada/inexistente'}), 404



# -----------------------------------------------ALUNOS---------------------------------------------- #
@app.route('/alunos/', methods=['GET'])
@app.route('/alunos', methods=['GET'])
def get_alunos():
    alunos = users['Alunos']
    return jsonify(alunos)

@app.route('/alunos/<id>', methods=['GET'])
def alunoPorId(id):
    try:
        id = int(id)
    except ValueError:
        return jsonify({'mensagem': 'ID inserido para aluno tem que ser um numero inteiro'}), 400
    
    if id <=0:
        return jsonify({'mensagem': 'ID do aluno nao pode ser menor ou igual a que zero'}), 400
    
    alunos = users['Alunos']
    for aluno in alunos:
        if aluno['id'] == id:
            return jsonify(aluno)
    
    
    return jsonify({'mensagem': 'Aluno(a) nao encontrado(a)/inexistente'}), 404


if __name__ == '__main__':
    app.run(host='localhost', port = 5003,debug=True)
