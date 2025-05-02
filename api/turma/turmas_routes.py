from flask import Blueprint, request, jsonify
from .turmas_model import listarTurmas, TurmaIdMenorQueUm, TurmaIdNaoInteiro, TurmaNaoEncontrada, listarTurmaPorId, deletarTurma, criarturma, ProfessorNaoEncontrado, achar_professor, turmaDescricaoJaExiste, ProfessorJaEstaEmUmaSala, atualizar_turma

turma_blueprint = Blueprint('turmas', __name__)

@turma_blueprint.route('/turmas', methods=['GET'])

def getTurma ():
    return jsonify(listarTurmas())

@turma_blueprint.route('/turmas/<id>', methods=['GET'])
def getTurmaPorId(id):
    try:
        turma = listarTurmaPorId(id)
        return jsonify(turma)
    except TurmaIdNaoInteiro:
        return jsonify({'mensagem': 'ID inserido para turma precisa ser um numero inteiro'}), 400
    except TurmaIdMenorQueUm:
        return jsonify({'mensagem': 'ID de turma nao pode ser menor ou igual a que zero'}), 400
    except TurmaNaoEncontrada:
        return jsonify({'mensagem': 'Turma nao encontrada/inexistente'}), 404
    
@turma_blueprint.route('/turmas/<id>', methods=['DELETE'])
def DeleteTurma(id):
    try:
        turma = deletarTurma(id)
        return jsonify({'mensagem': f'Turma deletada com sucesso'}), 200
    except TurmaIdNaoInteiro:
       return jsonify({'mensagem': 'ID de turma inválido. O ID precisa ser um número inteiro para que a turma possa ser deletada.'}), 400
    except TurmaIdMenorQueUm:
        return jsonify({'mensagem': 'ID de turma inválido. O ID precisa ser maior que zero para que a turma possa ser deletada.'}), 400
    except TurmaNaoEncontrada:
        return jsonify({'mensagem': 'ID de turma não encontrado/inexistente, falha ao deletar'}), 404
    

@turma_blueprint.route('/turmas', methods=['POST'])
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
    

    try:
        professor_existe = achar_professor(nova_turma['professor_id'])
    except ProfessorNaoEncontrado:
        return jsonify({'mensagem':'Id de Professor não encontrado'}), 400
        
        
    
    if 'ativo' not in nova_turma:
        nova_turma['ativo'] = False
    try:
        nova_turma_criada = criarturma(nova_turma)
        return jsonify(nova_turma_criada), 201
    
    except turmaDescricaoJaExiste: 
        return jsonify({'mensagem': f'A turma com a descricao {nova_turma["descricao"].title()} ja existe'}), 400
    except ProfessorJaEstaEmUmaSala:
         return jsonify({'mensagem': 'O professor cujo id mencionado já é responsavel por uma sala, insira um id de professor que nao esta sendo responsavel por alguma turma'}), 400
        


@turma_blueprint.route('/turmas/<id>', methods=['PUT'])
def update_turma(id):
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
        
        try:
            professor_existe = achar_professor(turma_atualizada['professor_id'])
        
        except professorNaoEncontrado:
            return jsonify({'mensagem': 'Professor Id não encontrado, tente novamente '}), 404   



    try:
        turma = atualizar_turma(id, turma_atualizada)
        return jsonify({'mensagem': 'Turma atualizada com sucesso'}), 200
        
    except TurmaIdNaoInteiro:
        return jsonify({'mensagem': 'ID de turma informado no end point precisa ser um número inteiro'}), 400
        
    except TurmaIdMenorQueUm:
        return jsonify({'mensagem': 'ID de turma precisa ser maior que zero'}), 400
        
    except TurmaNaoEncontrada:
        return jsonify({'mensagem': 'Erro, ID de turma não encontrado'}), 404
    
    except ProfessorJaEstaEmUmaSala:
        return jsonify({'mensagem': 'Erro!!! Cada professor já está sendo responsável por uma sala, e não pode ser responsável por duas, por favor, coloque um professor livre para cuidar dessa sala'}), 400
        
        




    