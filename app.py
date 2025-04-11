import os
from config import app
from alunos.alunos_routes import alunos_blueprint
from professor.professores_routes import professor_blueprint
from turma.turmas_routes import turma_blueprint

app.register_blueprint(alunos_blueprint)
app.register_blueprint(professor_blueprint)
app.register_blueprint(turma_blueprint)

if __name__ == '__main__':
    app.run(host=app.config["HOST"], port = app.config['PORT'],debug=app.config['DEBUG']) 