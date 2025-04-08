from flask import Flask, jsonify, request
from users import users
from config import app
from alunos.alunos_routes import alunos_blueprint

app.register_blueprint(alunos_blueprint)


#--------------------------------------------PROFESSORES------------------------------------------- #




""" @app.route('/professores/', methods=['GET'])
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
    novo_professor = request.json

    chaves_esperadas = {'nome', 'idade', 'materia', 'salario'}
    chaves_inseridas = set(novo_professor.keys())

    chaves_invalidas = chaves_inseridas - chaves_esperadas
    if chaves_invalidas:
        return jsonify({
            'mensagem': 'Chaves adicionais não necessárias, retire-as',
            'chaves_invalidas': list(chaves_invalidas)
        }), 400
    if not novo_professor.get('nome') or not novo_professor.get('materia'):
        return jsonify({'mensagem': 'Para criar um novo professor preciso que voce me passe os parâmetros nome e materia'}), 400
    
    if 'idade' not in novo_professor:
        return jsonify({'mensagem': 'Idade e obrigatoria, por favor insira-a'}), 400
    
    if not isinstance(novo_professor['nome'], str) or not isinstance(novo_professor['materia'], str):
        return jsonify({'mensagem': 'Os parametros nome e/ou materia precisam ser do tipo STRING'}), 400
    
    if not isinstance(novo_professor['idade'], int):
        return jsonify({'mensagem': 'Idade precisa ser um número INTEIRO'}), 400
    
    if not isinstance(novo_professor['salario'], (int, float)):
        return jsonify({'mensagem':'O parametro de salário precisa ser um número do tipo float ou int'}), 400
    
    if novo_professor['idade'] >= 0 and novo_professor['idade'] < 18:
        return jsonify({'mensagem': 'Um professor precisa ter no minimo 18 anos'}), 400

    if novo_professor['idade'] >= 120:
        return jsonify({'mensagem': 'Esse professor não tem condiçoes de dar aula, idade muito alta'}), 400

    if novo_professor['idade'] < 0:
        return jsonify({'mensagem': 'Idade não pode ser negativa!!'}), 400

    if novo_professor['salario'] < 1400.00:
        return jsonify({'mensagem': 'Salario precisa ser no minino a partir de R$1400.00 e nao pode ser negativo'}), 400
    

    id_novo = max([professor['id'] for professor in users['Professores']]) + 1
    novo_professor['id'] = id_novo
    users['Professores'].append(novo_professor)

    return jsonify(users['Professores']), 201 

@app.route('/professores/<id>', methods=['PUT'])
def atualizar_professor(id):
    try:
        id = int(id)
    except ValueError:
        return jsonify({'mensagem': 'ID IVÁLIDO, id precisa ser do tipo inteiro'}), 400
    
    if id <= 0:
        return jsonify({'mensagem': 'Valor de ID inválido, ID precisa ser MAIOR QUE ZERO'}), 400
    
    prof_atualizado = request.json
    
    
    chaves_esperadas = {'nome', 'idade', 'materia', 'salario'}
    chaves_inseridas = set(prof_atualizado.keys())
    chaves_invalidas = chaves_inseridas - chaves_esperadas
    if chaves_invalidas:
        return jsonify({
            'mensagem': 'Chaves adicionais não necessárias para atualização, por favor retire-as',
            'chaves_invalidas': list(chaves_invalidas)
        }), 400
    
    if 'nome' in prof_atualizado and (not isinstance(prof_atualizado['nome'], str) or not prof_atualizado['nome'].strip()):
        return jsonify({'mensagem': 'Para realizar atualização de professor valor para a chave nome precisa ser do tipo STRING e não pode estar vazia'}), 400
    
    
    if 'idade' in prof_atualizado:
        try:
            idade = int(prof_atualizado['idade'])
        except ValueError:
            return jsonify({'mensagem': 'Essa nova idade para professor está inválida, idade tem que ser obrigatóriamente do tipo INTEIRO'}), 400
        
        if idade > 120:
            return jsonify({'mensagem': 'Essa nova idade está muito avançada para dar aulas, talvez nem esteja vivo'}), 400
        
        if idade < 18:
            return jsonify({'mensagem': 'Idade professor não pode ser negativa ou menor que 18 anos'}), 400
        
    if 'materia' in prof_atualizado:
        if not isinstance(prof_atualizado['materia'], str) or not prof_atualizado['materia'].strip():
            return jsonify({'mensagem': 'O valor inserido em chave matéria precisa ser do tipo String e não pode estar vazia'}), 400


    if 'salario' in prof_atualizado:
        try:
            salario = float(prof_atualizado['salario'])
        except ValueError:
            return jsonify({'mensagem': 'O valor da chave salário precisa ser do um número com ponto flutuante (FLOAT, ex: 1400.0), ou int(1400) para que possa existir a converção'}), 400

        if salario < 1400:
            return jsonify({'mensagem': 'O novo valor para salário deve ser no mínimo 1400 e não pode ser negativo'}), 400


    professores = users['Professores']
    for index, professor in enumerate(professores):
        if professor['id'] == id:
            prof_atualizado['id'] = professor['id']
            users['Professores'][index] = prof_atualizado
            return jsonify({'mensagem': f'Professor {prof_atualizado["nome"]} atualizado com sucesso'}), 200
    return jsonify({'mensagem': 'id não encontrado'}), 404
            

@app.route('/professores/<id>', methods=['DELETE'])
def detletar_professor(id):

    try:
        id = int(id)
    except ValueError:
        return jsonify({'mensagem': 'ID IVÁLIDO, id precisa ser do tipo inteiro para que eu possa deletar'}), 400
    
    if id <= 0:
        return jsonify({'mensagem': 'Valor de ID inválido, ID precisa ser MAIOR QUE ZERO para que eu possa deletar'}), 400
    

    for pos, professor in enumerate(users['Professores']):
        if professor['id'] == id:
            users['Professores'].pop(pos)
            return jsonify({'mensagem': f'Professor {professor["nome"]} deletado com sucesso'}), 200
    return jsonify({'mensagem': 'id de professor não encontrado, falha ao deletar'}), 404


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


@app.route('/turmas', methods=['POST'])
def criar_turma():
    nova_turma = request.json


    chaves_esperadas = {'descricao', 'professor_id', 'ativo'}
    chaves_inseridas = set(nova_turma.keys())
    chaves_invalidas = chaves_inseridas - chaves_esperadas
    if chaves_invalidas:
        return jsonify({
            'mensagem': 'Chaves adicionais não necessárias, retire-as',
            'chaves_invalidas': list(chaves_invalidas)
        }), 400

    if 'professor_id' not in nova_turma or 'descricao' not in nova_turma:
        return jsonify({'mensagem': 'Para criar uma nova turma, é obrigatório inserir a chave id_professor e descricao'}), 400
    
    if not isinstance(nova_turma['descricao'], str) or not nova_turma['descricao'].strip():
        return jsonify({'mensagem': 'decricao precisa ser uma STRING e/ou não pode estar vazia'}), 400
    

    if not isinstance(nova_turma['professor_id'], int):
         return jsonify({'mensagem': 'A chave professor_id precisa ser um número INTEIRO'}), 400
    
    if nova_turma['professor_id'] <= 0:
        return jsonify({'mensagem': 'chave professor_id Inválida!!!! O valor inserido nessa chave não pode ser menor ou igual a zero'}), 400


    if 'ativo' in nova_turma and not isinstance(nova_turma['ativo'], bool):
        return jsonify({'mensagem': 'a chave ativo, precisa ser de valor booleano (true ou false)'}), 400
    

    prof_existe = False
    for professor in users['Professores']:
        if professor['id'] == nova_turma['professor_id']:
            prof_existe = True
            break
    if not prof_existe:
        return jsonify({'mensagem':'Id de Professor não encontrado'}), 404
    
    for turma in users['Turmas']:
        if turma['descricao'].lower() == nova_turma['descricao'].lower():
            return jsonify({'mensagem': f'A turma com a descricao {turma["descricao"]} ja existe'}), 400
        
        if turma['professor_id'] == nova_turma['professor_id']:
            return jsonify({'mensagem': 'O professor cujo id mencionado já é responsavel por uma sala, insira um id de professor que nao esta sendo responsavel por alguma turma'}), 400
        
    
    if 'ativo' not in nova_turma:
        nova_turma['ativo'] = False

    id_novo = max([turma['id'] for turma in users['Turmas']]) + 1
    nova_turma['id'] = id_novo
    users['Turmas'].append(nova_turma)

    return jsonify(nova_turma), 201

@app.route('/turmas/<id>', methods=['PUT'])
def atualizar_turma(id):    
    try:
        id = int(id)
    except ValueError:
        return jsonify({'mensagem': 'ID de turma informado no end point precisa ser um número inteiro'}), 400
    
    if id <= 0:
        return jsonify({'mensagem': 'ID de turma precisa ser maior que zero'}), 400
        
    turma_atualizada = request.json

    if 'ativo' in turma_atualizada:
        if not isinstance(turma_atualizada['ativo'], bool):
            return jsonify({'mensagem': 'O valor para a chave ativo precisa ser do tipo boolean'}), 400
        

    chaves_esperadas = {'descricao', 'professor_id', 'ativo'}
    chaves_inseridas = set(turma_atualizada.keys())
    chaves_invalidas = chaves_inseridas - chaves_esperadas
    if chaves_invalidas:
        return jsonify({
            'mensagem': 'Chaves adicionais não necessárias, retire-as',
            'chaves_invalidas': list(chaves_invalidas)
        }), 400
        


    if 'descricao' in turma_atualizada:
        if not isinstance(turma_atualizada['descricao'], str):
            return jsonify({'mensagem': 'O novo valor para a chave descrição precisa ser uma STRING'}), 400
    

    if 'professor_id' in turma_atualizada:
        if not isinstance(turma_atualizada['professor_id'], int):
            return jsonify ({'mensagem': 'A chave professor_id precisa ser um número inteiro'}), 400
        
        
        if turma_atualizada['professor_id'] <= 0:
            return jsonify({'mensagem': 'A chave professor_id precisa ser maior que zero'}), 400
        
    for turma in users['Turmas']:
        if turma['professor_id'] == turma_atualizada['professor_id'] and id != turma['id']:
            return jsonify({'mensagem': 'Erro!!! Cada professor já está sendo responsável por uma sala, e não pode ser responsável por duas, por favor, coloque um professor livre para cuidar dessa sala'}), 400

        prof_existe = False
        for professor in users['Professores']:
            if professor['id'] == turma_atualizada['professor_id']:
                prof_existe = True
                break
        if not prof_existe:
            return jsonify({'mensagem': 'Professor Id não encontrado, tente novamente '}), 404
    

    turmas = users['Turmas']
    for index, turma in enumerate(turmas):
        if turma['id'] == id:
            turma_atualizada['id'] = turma['id']
            users['Turmas'][index] = turma_atualizada
            return jsonify({'mensagem': 'Turma atualizada com sucesso'}), 200
    return jsonify({'mensagem': 'Erro, ID de turma não encontrado'}), 404

@app.route('/turmas/<id>', methods=['DELETE'])
def deletar_turma(id):

    try:
        id = int(id)
    except ValueError:
        return jsonify({'mensagem': 'ID de turma inválido. O ID precisa ser um número inteiro para que a turma possa ser deletada.'}), 400
    
    if id <= 0:
        return jsonify({'mensagem': 'ID de turma inválido. O ID precisa ser maior que zero para que a turma possa ser deletada.'}), 400
    

    for pos, turma in enumerate(users['Turmas']):
        if turma['id'] == id:
            users['Turmas'].pop(pos)
            return jsonify({'mensagem': f'Turma {turma["descricao"]} deletada com sucesso'}), 200
    return jsonify({'mensagem': 'ID de turma não encontrado/inexistente, falha ao deletar'}), 404

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

@app.route('/alunos', methods=['POST'])
def criar_aluno():
    novo_aluno = request.json

    chaves_esperadas = {'nome', 'idade', 'turma_id', 'data_nascimento', 'nota_primeiro_semestre', 'nota_segundo_semestre', 'media_final'}

    chaves_inseridas = set(novo_aluno.keys())

    chaves_invalidas = chaves_inseridas - chaves_esperadas
    if chaves_invalidas:
        return jsonify({
            'mensagem': 'Chaves adicionais não necessárias para a criação de aluno, retire-as',
            'chaves_invalidas': list(chaves_invalidas)
        }), 400
    
    if 'nome' not in novo_aluno or 'turma_id' not in novo_aluno:
        return jsonify({'mensagem': 'Os campos nome, turma_id são OBRIGATÓRIOS'}), 400
    
    if novo_aluno['turma_id'] < 0:
        return jsonify({'mensagem': 'O valor informado para a chave turma_id é INVÁLIDO (não pode ser negativo)'}), 400

    turma_existe = False
    for turma in users['Turmas']:
        if turma['id'] == novo_aluno['turma_id']:
            turma_existe = True
            break
    if not turma_existe:
        return jsonify({'mensagem': 'Id de turma não encontrada'}), 404
    
    if not (isinstance(novo_aluno['nome'], str)):
        return jsonify({'mensagem': 'Chave nome precisa ser do tipo string'}), 400
    
    if not isinstance(novo_aluno['turma_id'], int) or not isinstance(novo_aluno['idade'], int):
        return jsonify({'mensagem': 'O valor informado para as chaves idade e turma_id precisam ser INTEIROS'}), 400
    
    if novo_aluno['idade'] <= 0:
        return jsonify({'mensagem': 'O valor informado na chave idade não pode ser negativo ou igual a zero'}),400
    
    if 'data_nascimento' in novo_aluno and not isinstance(novo_aluno.get('data_nascimento'), str):
        return jsonify({'mensagem': 'Data de Nascimento precisa ser uma string dd-mm-aaaa'}),400
    
    if not isinstance(novo_aluno['nota_primeiro_semestre'], (int, float)) or not isinstance(novo_aluno['nota_segundo_semestre'], (int, float)) or not isinstance(novo_aluno['media_final'], (int, float)):
        return jsonify({'mensagem': 'Os valores para as notas de primeiro, segundo, semestre, precisao ser do tipo INTEIRO ou FLOAT'}), 400

    if novo_aluno['nota_primeiro_semestre'] < 0 or novo_aluno['nota_segundo_semestre'] < 0 or novo_aluno['media_final'] < 0:
        return jsonify({'mensagem' : 'As notas e a media precisam receber um valor inteiro ou float'}), 400
    
    



    if 'nota_primeiro_semestre' not in novo_aluno:
        novo_aluno['nota_primeiro_semestre'] = 0.0
    if 'nota_segundo_semestre' not in novo_aluno:
        novo_aluno['nota_segundo_semestre'] = 0.0
    if 'media_final' not in novo_aluno:
        novo_aluno['media_final'] = 0.0

    id_novo = max([aluno['id'] for aluno in users['Alunos']]) + 1
    novo_aluno['id'] = id_novo
    users['Alunos'].append(novo_aluno)

    return jsonify(novo_aluno), 201

@app.route('/alunos/<id>', methods=['PUT'])
def atualizar_alunos(id):    
    try:
        id = int(id)
    except ValueError:
        return jsonify({'mensagem': 'ID de aluno informado no end point precisa ser um número inteiro'}), 400
    
    if id <= 0:
        return jsonify({'mensagem': 'ID de aluno precisa ser maior que zero'}), 400
    
    aluno_atualizado = request.json

    chaves_esperadas = {'nome', 'idade', 'turma_id', 'data_nascimento', 'nota_primeiro_semestre', 'nota_segundo_semestre', 'media_final'}
    chaves_inseridas = set(aluno_atualizado.keys())
    chaves_invalidas = chaves_inseridas - chaves_esperadas
    if chaves_invalidas:
        return jsonify({
            'mensagem': 'Chaves adicionais não necessárias, retire-as',
            'chaves_invalidas': list(chaves_invalidas)
        }), 400
        
    if 'nome' in aluno_atualizado:
        if not isinstance(aluno_atualizado['nome'], str) or not aluno_atualizado['nome'].strip():
            return jsonify({'mensagem': 'O valor para a chave aluno precisa ser uma string e não pode estar vazia'}), 400
        
    if 'turma_id' in aluno_atualizado:
        
        if not isinstance(aluno_atualizado['turma_id'], int):
            return jsonify ({'mensagem': 'A chave turma_id precisa ser um número inteiro'}), 400
        
        if aluno_atualizado['turma_id'] <= 0:
            return jsonify({'mensagem': 'A chave turma_id precisa ser maior que zero'}), 400
        
        turma_existe = False
        for turma in users['Turmas']:
            if turma['id'] == aluno_atualizado['turma_id']:
                turma_existe = True
                break
        if not turma_existe:
            return jsonify({'mensagem': 'Id de turma não encontrado'}), 404 
       
    if 'data_nascimento' in aluno_atualizado:
        if not isinstance(aluno_atualizado['data_nascimento'], str) or not aluno_atualizado['data_nascimento'].strip():
            return jsonify({'mensagem': 'A chave data_nascimento precisa ser uma string e não pode estar vazia!!'}), 400
        
    if 'idade' in aluno_atualizado:
        
        try:
           aluno_atualizado['idade']  = int(aluno_atualizado['idade'])
        except ValueError:       
            return jsonify({'mensagem': 'O valor informado para a chave idade precisa ser um número inteiro INTEIRO'}), 400
        
        if aluno_atualizado['idade'] <= 0:
            return jsonify({'mensagem': 'O valor informado na chave idade não pode ser negativo ou igual a zero'}), 400
        
    if 'nota_primeiro_semestre' in aluno_atualizado or 'nota_segundo_semestre' in aluno_atualizado or 'media_final' in aluno_atualizado:
        try:
            aluno_atualizado['nota_primeiro_semestre'] = float(aluno_atualizado['nota_primeiro_semestre'])
            aluno_atualizado['nota_segundo_semestre'] = float(aluno_atualizado['nota_segundo_semestre'])
            aluno_atualizado['media_final'] = float(aluno_atualizado['media_final'])
        except ValueError:
            return jsonify({'mensagem': 'O novo valor para as chaves das notas primeiro, segundo semestre e média_final precisam ser do tipo float'}), 400

        if aluno_atualizado['nota_primeiro_semestre'] < 0 or aluno_atualizado['nota_segundo_semestre'] < 0 or aluno_atualizado['media_final'] < 0:
            return jsonify({'mensagem': 'O novo valor para as chaves das notas primeiro, segundo semestre e média_final precisam não podem ser números negativos'}), 400 
            
        if aluno_atualizado['nota_primeiro_semestre'] > 10 or aluno_atualizado['nota_segundo_semestre'] > 10 or aluno_atualizado['media_final'] > 10:
            return jsonify({'mensagem': 'O novo valor para as chaves das notas primeiro, segundo semestre e média_final precisam não podem ser maiores que 10'}), 400
        
        
    alunos = users['Alunos']
    for index, aluno in enumerate(alunos):
        if aluno['id'] == id:
            aluno_atualizado['id'] = aluno['id']
            users['Alunos'][index] = aluno_atualizado
            return jsonify({'mensagem': 'Aluno atualizada com sucesso'}), 200
    return jsonify({'mensagem': 'Erro, Id de aluno não encontrado'}), 404
        

@app.route('/alunos/<id>', methods=['DELETE'])
def deletar_aluno(id):

    try:
        id = int(id)
    except ValueError:
        return jsonify({'mensagem': 'ID de aluno(a) inválido. O ID precisa ser um número inteiro para que o(a) aluno(a) possa ser deletado(a) com sucesso.'}), 400
    
    if id <= 0:
        return jsonify({'mensagem': 'ID de aluno(a) inválido. O ID precisa ser maior que zero para que o(a) aluno(a) possa ser deletado(a) com sucesso.'}), 400
    

    for pos, aluno in enumerate(users['Alunos']):
        if aluno['id'] == id:
            users['Alunos'].pop(pos)
            return jsonify({'mensagem': f'aluno {aluno["nome"]} deletado(a) com sucesso'}), 200
    return jsonify({'mensagem': 'ID de aluno(a) não encontrado(a), falha ao deletar'}), 404 """




if __name__ == '__main__':
    app.run(host=app.config["HOST"], port = app.config['PORT'],debug=app.config['DEBUG']) 