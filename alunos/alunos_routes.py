from flask import Blueprint, request, jsonify
from .alunos_model import AlunoNaoEncontrado, listar_alunos

alunos_blueprint = Blueprint('alunos', __name__)

@alunos_blueprint.route('/alunos', methods=['GET'])
def get_alunos():
    return jsonify(listar_alunos())