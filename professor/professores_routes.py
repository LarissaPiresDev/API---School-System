from flask import Blueprint, request, jsonify
from .professores_model import listar_professores, ProfessorIdMenorQueUm, ProfessorIdNaoInteiro, ProfessorNaoEncontrado, listar_professor_por_id

professor_blueprint = Blueprint('professores', __name__)

@professor_blueprint.route('/professores', methods=['GET'])
def get_professores():
    return jsonify(listar_professores())

@professor_blueprint.route('/professores/<id>', methods=['GET'])
def profPorId(id):
    try:
        professor = listar_professor_por_id(id)
        return jsonify(professor)
    
    except ProfessorIdNaoInteiro:
        return jsonify({'mensagem': 'ID inserido para professor precisa ser um numero inteiro'}), 400
    
    except ProfessorIdMenorQueUm:
        return jsonify({'mensagem': 'ID do professor nao pode ser menor ou igual a que zero'}), 400
    
    except ProfessorNaoEncontrado:
        return jsonify({'mensagem': 'Professor(a) nao encontrado(a)/inexistente'}), 404
