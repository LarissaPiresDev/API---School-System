from flask import Blueprint, request, jsonify
from .alunos_model import AlunoNaoEncontrado, listar_alunos, aluno_por_id

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