from flask import Blueprint, request, jsonify
from .turmas_model import listarTurmas, TurmaIdMenorQueUm, TurmaIdNaoInteiro, TurmaNaoEncontrada, listarTurmaPorId, deletarTurma

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
    