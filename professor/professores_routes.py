from flask import Blueprint, request, jsonify
from .professores_model import listar_professores, ProfessorIdMenorQueUm, ProfessorIdNaoInteiro, ProfessorNaoEncontrado, listar_professor_por_id, criar_professor

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
    
    
@professor_blueprint.route('/professores', methods=['POST'])
def create_professor():
    novo_professor = request.json

    chaves_esperadas = {'nome', 'idade', 'materia', 'salario'}
    chaves_inseridas = set(novo_professor.keys())

    chaves_invalidas = chaves_inseridas - chaves_esperadas
    if chaves_invalidas:
        return jsonify({
            'mensagem': 'Chaves adicionais não necessárias, retire-as',
            'chaves_invalidas': list(chaves_invalidas)
        }), 400
    if not novo_professor.get('nome') or not novo_professor.get('materia'):
        return jsonify({'mensagem': 'Para criar um novo professor preciso que voce me passe os parâmetros nome e materia'}), 400
    
    if 'idade' not in novo_professor:
        return jsonify({'mensagem': 'Idade e obrigatoria, por favor insira-a'}), 400
    
    if not isinstance(novo_professor['nome'], str) or not isinstance(novo_professor['materia'], str):
        return jsonify({'mensagem': 'Os parametros nome e/ou materia precisam ser do tipo STRING'}), 400
    
    if not isinstance(novo_professor['idade'], int):
        return jsonify({'mensagem': 'Idade precisa ser um número INTEIRO'}), 400
    
    if not isinstance(novo_professor['salario'], (int, float)):
        return jsonify({'mensagem':'O parametro de salário precisa ser um número do tipo float ou int'}), 400
    
    if novo_professor['idade'] >= 0 and novo_professor['idade'] < 18:
        return jsonify({'mensagem': 'Um professor precisa ter no minimo 18 anos'}), 400

    if novo_professor['idade'] >= 120:
        return jsonify({'mensagem': 'Esse professor não tem condiçoes de dar aula, idade muito alta'}), 400

    if novo_professor['idade'] < 0:
        return jsonify({'mensagem': 'Idade não pode ser negativa!!'}), 400

    if novo_professor['salario'] < 1400.00:
        return jsonify({'mensagem': 'Salario precisa ser no minino a partir de R$1400.00 e nao pode ser negativo'}), 400
    

    novo_professor_criado = criar_professor(novo_professor)

    return jsonify(novo_professor_criado), 201
