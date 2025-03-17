from flask import Flask, jsonify
import users

app = Flask(__name__)
dados = users.users

#--------------------------------------------PROFESSORES------------------------------------------- #

@app.route('/professores/', methods=['GET'])
@app.route('/professores', methods=['GET'])
def get_professores():
    professores = dados['Professores']
    return jsonify(professores)

@app.route('/professores/<id>', methods=['GET'])
def profPorId(id):
    try:
        id = int(id)
    except ValueError:
        return jsonify({'mensagem': 'ID inserido para professor precisa ser um numero inteiro'}), 400
    
    if id <= 0:
        return jsonify({'mensagem': 'ID do professor nao pode ser menor ou igual a que zero'}), 400
    
    professores = dados['Professores']
    for professor in professores:
        if professor['id'] == id:
            return jsonify(professor)
            
    return jsonify({'mensagem': 'Professor(a) nao encontrado(a)/inexistente'}), 404

# ---------------------------------------------TURMAS------------------------------------------------ #

@app.route('/turmas/', methods=['GET'])
@app.route('/turmas', methods=['GET'])
def get_turmas():
    turmas = dados['Turmas']
    return jsonify(turmas)


@app.route('/turmas/<id>', methods=['GET'])
def turmaPorId(id):
    try:
        id = int(id)
    except ValueError:
        return jsonify({'mensagem': 'ID inserido para turma precisa ser um numero inteiro'}), 400
    if id <=0:
        return jsonify({'mensagem': 'ID de turma nao pode ser menor ou igual a que zero'}), 400
    turmas = dados['Turmas']
    for turma in turmas:
        if turma['id'] == id:
            return jsonify(turma)
            
    return jsonify({'mensagem': 'Turma nao encontrada/inexistente'}), 404



# -----------------------------------------------ALUNOS---------------------------------------------- #
@app.route('/alunos/', methods=['GET'])
@app.route('/alunos', methods=['GET'])
def get_alunos():
    alunos = dados['Alunos']
    return jsonify(alunos)

@app.route('/alunos/<id>', methods=['GET'])
def alunoPorId(id):
    try:
        id = int(id)
    except ValueError:
        return jsonify({'mensagem': 'ID inserido para aluno tem que ser um numero inteiro'}), 400
    
    if id <=0:
        return jsonify({'mensagem': 'ID do aluno nao pode ser menor ou igual a que zero'}), 400
    
    alunos = dados['Alunos']
    for aluno in alunos:
        if aluno['id'] == id:
            return jsonify(aluno)
    
    
    return jsonify({'mensagem': 'Aluno(a) nao encontrado(a)/inexistente'}), 404


if __name__ == '__main__':
    app.run(host='localhost', port = 5002,debug=True)
