from flask import Blueprint, request, jsonify
from .professores_model import listar_professores

professor_blueprint = Blueprint('professores', __name__)

@professor_blueprint.route('/professores', methods=['GET'])
def get_professores():
    return jsonify(listar_professores())