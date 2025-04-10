from flask import Blueprint, request, jsonify
from .turmas_model import listarTurmas

turma_blueprint = Blueprint('turmas', __name__)

@turma_blueprint.route('/turmas', methods=['GET'])

def getTurma ():
    return jsonify(listarTurmas())
