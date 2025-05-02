from flask import Blueprint, request, jsonify
from .alunos_model import AlunoNaoEncontrado, AlunoIdNaoInteiro, AlunoIdMenorQueUm, listar_alunos, aluno_por_id, TurmaNaoEncontrada, achar_turma, criar_aluno, atualizar_aluno, deletar_aluno
from datetime import datetime
from turma.turmas_model import Turma, listarTurmas
from config import db

alunos_blueprint = Blueprint('alunos', __name__)

@alunos_blueprint.route('/alunos', methods=['GET'])
def get_alunos():
    return jsonify(listar_alunos())

@alunos_blueprint.route('/alunos/<id>', methods=['GET'])
def alunoPorId(id):
    try:
        aluno = aluno_por_id(id)
        return jsonify(aluno)
    
    except AlunoIdNaoInteiro:
        return jsonify({'mensagem': 'ID inserido para aluno tem que ser um numero inteiro'}), 400
    except AlunoIdMenorQueUm:
        
        return jsonify({'mensagem': 'ID do aluno nao pode ser menor ou igual a que zero'}), 400
    except AlunoNaoEncontrado:
        return jsonify({'mensagem': 'Aluno(a) nao encontrado(a)/inexistente'}), 404
    
    


@alunos_blueprint.route('/alunos', methods=['POST'])
def create_aluno():
    novo_aluno = request.json

    chaves_esperadas = {'nome','turma_id', 'data_nascimento', 'nota_primeiro_semestre', 'nota_segundo_semestre'}

    chaves_inseridas = set(novo_aluno.keys())

    chaves_invalidas = chaves_inseridas - chaves_esperadas
    if chaves_invalidas:
        return jsonify({
            'mensagem': 'Chaves adicionais não necessárias para a criação de aluno, retire-as',
            'chaves_invalidas': list(chaves_invalidas)
        }), 400
    
    if 'nome' not in novo_aluno or 'turma_id' not in novo_aluno:
        return jsonify({'mensagem': 'Os campos nome, turma_id são OBRIGATÓRIOS'}), 400
    
    if not isinstance(novo_aluno['turma_id'], int):
        return jsonify({'mensagem': 'O valor informado para a chave turma_id precisa ser INTEIROS'}), 400
    
    if novo_aluno['turma_id'] <= 0:
        return jsonify({'mensagem': 'O valor informado para a chave turma_id é INVÁLIDO (não pode ser negativo)'}), 400



    turma = Turma.query.get(novo_aluno['turma_id'])
    if not turma:
        return jsonify({'mensagem': 'Id de turma não encontrada'}), 404
    
    if not (isinstance(novo_aluno['nome'], str)) or not novo_aluno['nome'].strip():
        return jsonify({'mensagem': 'Chave nome precisa ser do tipo string e não pode estar vazia'}), 400
    
    try:
        novo_aluno['data_nascimento'] = datetime.strptime(novo_aluno['data_nascimento'], "%Y-%m-%d").date()
    except (ValueError, TypeError):
            return jsonify({'mensagem': 'Data de Nascimento precisa ser uma string dd-mm-aaaa e não pode estar vazia'}), 400

    
    if 'nota_primeiro_semestre' in novo_aluno or 'nota_segundo_semestre' in novo_aluno:
        
        if not isinstance(novo_aluno['nota_primeiro_semestre'], (int, float)) or not isinstance(novo_aluno['nota_segundo_semestre'], (int, float)):
            return jsonify({'mensagem': 'Os valores para as notas de primeiro e segundo semestre, precisao ser do tipo INTEIRO ou FLOAT'}), 400

        if novo_aluno['nota_primeiro_semestre'] < 0 or novo_aluno['nota_segundo_semestre'] < 0:
            return jsonify({'mensagem' : 'As notas e a media precisam receber um valor inteiro ou float'}), 400
    
    



    if 'nota_primeiro_semestre' not in novo_aluno:
        novo_aluno['nota_primeiro_semestre'] = 0.0
    if 'nota_segundo_semestre' not in novo_aluno:
        novo_aluno['nota_segundo_semestre'] = 0.0
        
    novo_aluno_criado = criar_aluno(novo_aluno)

    return jsonify(novo_aluno_criado), 201


@alunos_blueprint.route('/alunos/<id>', methods=['PUT'])
def update_aluno(id):    
    aluno_atualizado = request.json

    chaves_esperadas = {'nome','turma_id', 'data_nascimento', 'nota_primeiro_semestre', 'nota_segundo_semestre'}
    chaves_inseridas = set(aluno_atualizado.keys())
    chaves_invalidas = chaves_inseridas - chaves_esperadas
    if chaves_invalidas:
        return jsonify({
            'mensagem': 'Chaves adicionais não necessárias, retire-as',
            'chaves_invalidas': list(chaves_invalidas)
        }), 400
        
    if 'nome' in aluno_atualizado:
        if not isinstance(aluno_atualizado['nome'], str) or not aluno_atualizado['nome'].strip():
            return jsonify({'mensagem': 'O valor para a chave nome precisa ser uma string e não pode estar vazia'}), 400
        
    if 'turma_id' in aluno_atualizado:
        
        if not isinstance(aluno_atualizado['turma_id'], int):
            return jsonify ({'mensagem': 'A chave turma_id precisa ser um número inteiro'}), 400
        
        if aluno_atualizado['turma_id'] <= 0:
            return jsonify({'mensagem': 'A chave turma_id precisa ser maior que zero'}), 400
        
        turma = Turma.query.get(aluno_atualizado['turma_id'])
        if not turma:
            return jsonify({'mensagem': 'Id de turma não encontrado'}), 404
    if 'data_nascimento' in aluno_atualizado:
        try:
            aluno_atualizado['data_nascimento'] = datetime.strptime(aluno_atualizado['data_nascimento'], "%Y-%m-%d").date()
        except (ValueError, TypeError):
                return jsonify({'mensagem': 'A chave data_nascimento precisa ser uma string no formato YYYY-MM-DD e não pode estar vazia'}), 400
        
    if 'nota_primeiro_semestre' in aluno_atualizado or 'nota_segundo_semestre' in aluno_atualizado:
        try:
            aluno_atualizado['nota_primeiro_semestre'] = float(aluno_atualizado['nota_primeiro_semestre'])
            aluno_atualizado['nota_segundo_semestre'] = float(aluno_atualizado['nota_segundo_semestre'])
        except ValueError:
            return jsonify({'mensagem': 'O novo valor para as chaves das notas primeiro e segundo semestre precisam ser do tipo float'}), 400

        if aluno_atualizado['nota_primeiro_semestre'] < 0 or aluno_atualizado['nota_segundo_semestre'] < 0:
            return jsonify({'mensagem': 'O novo valor para as chaves das notas não podem ser números negativos'}), 400 
            
        if aluno_atualizado['nota_primeiro_semestre'] > 10 or aluno_atualizado['nota_segundo_semestre'] > 10:
            return jsonify({'mensagem': 'O novo valor para as chaves das notas primeiro e segundo semestre  não podem ser maiores que 10'}), 400
        
        
    try:
        aluno = atualizar_aluno(id, aluno_atualizado)
        return jsonify({'mensagem': 'Aluno atualizada com sucesso'}), 200
    
    except AlunoIdNaoInteiro:
        return jsonify({'mensagem': 'ID de aluno informado no end point precisa ser um número inteiro'}), 400
    
    except AlunoIdMenorQueUm:
        return jsonify({'mensagem': 'ID de aluno precisa ser maior que zero'}), 400
    
    except AlunoNaoEncontrado:
        return jsonify({'mensagem': 'Erro, Id de aluno não encontrado'}), 404
    
@alunos_blueprint.route('/alunos/<id>', methods=['DELETE'])
def delete_aluno(id):
    try:
        aluno = deletar_aluno(id)
        return jsonify({'mensagem': f'aluno deletado(a) com sucesso'}), 200
    
    except AlunoIdNaoInteiro:
        return jsonify({'mensagem': 'ID de aluno(a) inválido. O ID precisa ser um número inteiro para que o(a) aluno(a) possa ser deletado(a) com sucesso.'}), 400
    
    except AlunoIdMenorQueUm:
        return jsonify({'mensagem': 'ID de aluno(a) inválido. O ID precisa ser maior que zero para que o(a) aluno(a) possa ser deletado(a) com sucesso.'}), 400
    
    except AlunoNaoEncontrado:
        return jsonify({'mensagem': 'ID de aluno(a) não encontrado(a), falha ao deletar'}), 404