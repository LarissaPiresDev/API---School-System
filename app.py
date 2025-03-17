from flask import Flask, jsonify
import users

app = Flask(__name__)
dados = users.users

@app.route('/professores/', methods=['GET'])
@app.route('/professores', methods=['GET'])
def get_professores():
    professores = dados['Professores']
    return jsonify(professores)


@app.route('/alunos/', methods=['GET'])
@app.route('/alunos', methods=['GET'])
def get_alunos():
    alunos = dados['Alunos']
    return jsonify(alunos)


if __name__ == '__main__':
    app.run(host='localhost', port = 5002,debug=True)



