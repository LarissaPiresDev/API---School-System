from flask import Blueprint, request, jsonify
from .alunos_model import AlunoNaoEncontrado, listar_alunos, aluno_por_id, TurmaNaoEncontrada, achar_turma, criar_aluno, atualizar_aluno

alunos_blueprint = Blueprint('alunos', __name__)

@alunos_blueprint.route('/alunos', methods=['GET'])
def get_alunos():
    return jsonify(listar_alunos())

@alunos_blueprint.route('/alunos/<id>', methods=['GET'])
def alunoPorId(id):
    try:
        try:
            id = int(id)
        except ValueError:
            return jsonify({'mensagem': 'ID inserido para aluno tem que ser um numero inteiro'}), 400
        
        if id <=0:
            return jsonify({'mensagem': 'ID do aluno nao pode ser menor ou igual a que zero'}), 400
        
        aluno = aluno_por_id(id)
        return jsonify(aluno)
    
    except AlunoNaoEncontrado:
        return jsonify({'mensagem': 'Aluno(a) nao encontrado(a)/inexistente'}), 404
    


@alunos_blueprint.route('/alunos', methods=['POST'])
def create_aluno():
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
    
    if not isinstance(novo_aluno['turma_id'], int) or not isinstance(novo_aluno['idade'], int):
        return jsonify({'mensagem': 'O valor informado para as chaves idade e turma_id precisam ser INTEIROS'}), 400
    
    if novo_aluno['turma_id'] < 0:
        return jsonify({'mensagem': 'O valor informado para a chave turma_id é INVÁLIDO (não pode ser negativo)'}), 400


    try:
        turmaexiste = achar_turma(novo_aluno['turma_id'])
    except TurmaNaoEncontrada:
        return jsonify({'mensagem': 'Id de turma não encontrada'}), 404
    
    if not (isinstance(novo_aluno['nome'], str)):
        return jsonify({'mensagem': 'Chave nome precisa ser do tipo string'}), 400
    
    if novo_aluno['idade'] <= 0:
        return jsonify({'mensagem': 'O valor informado na chave idade não pode ser negativo ou igual a zero'}),400
    
    if 'data_nascimento' in novo_aluno:
        if not isinstance(novo_aluno['data_nascimento'], str) or not novo_aluno['data_nascimento'].strip():
            return jsonify({'mensagem': 'Data de Nascimento precisa ser uma string dd-mm-aaaa e não pode estar vazia'}), 400

    
    if 'nota_primeiro_semestre' in novo_aluno or 'nota_segundo_semestre' in novo_aluno or 'media_final' in novo_aluno:
        
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
    
    
    novo_aluno_criado = criar_aluno(novo_aluno)

    return jsonify(novo_aluno_criado), 201


@alunos_blueprint.route('/alunos/<id>', methods=['PUT'])
def update_aluno(id):    
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
        
        try:
            turmaexiste = achar_turma(aluno_atualizado['turma_id'])
        except TurmaNaoEncontrada:
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
        
        
    try:
        
        aluno = atualizar_aluno(id, aluno_atualizado)
        return jsonify({'mensagem': 'Aluno atualizada com sucesso'}), 200
    
    except AlunoNaoEncontrado:
        return jsonify({'mensagem': 'Erro, Id de aluno não encontrado'}), 404