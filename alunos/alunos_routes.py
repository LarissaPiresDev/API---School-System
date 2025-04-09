from flask import Blueprint, request, jsonify
from .alunos_model import AlunoNaoEncontrado, listar_alunos, aluno_por_id, TurmaNaoEncontrada, achar_turma, criar_aluno

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