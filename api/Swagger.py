from flask import Flask
from flask_restx import Api, Resource, fields

app = Flask(__name__)
api = Api(app, title="API Escolar", version="1.0", description="API para Professores, Alunos e Turmas")

# ====================
# MODELOS (esquemas)
# ====================
professor_model = api.model("Professor", {
    "id": fields.Integer(readonly=True),
    "nome": fields.String(required=True),
    "disciplina": fields.String(required=True)
})

aluno_model = api.model("Aluno", {
    "id": fields.Integer(readonly=True),
    "nome": fields.String(required=True),
    "idade": fields.Integer(required=True)
})

turma_model = api.model("Turma", {
    "id": fields.Integer(readonly=True),
    "nome": fields.String(required=True),
    "professor_id": fields.Integer(required=True, description="ID do professor responsável"),
    "alunos": fields.List(fields.Integer, description="IDs dos alunos da turma")
})

# ====================
# "Banco de dados" fake
# ====================
professores = []
alunos = []
turmas = []

# ====================
# NAMESPACES
# ====================
ns_prof = api.namespace("professores", description="Operações com professores")
ns_aluno = api.namespace("alunos", description="Operações com alunos")
ns_turma = api.namespace("turmas", description="Operações com turmas")

# ====================
# PROFESSORES
# ====================
@ns_prof.route("/")
class ProfessorList(Resource):
    @ns_prof.marshal_list_with(professor_model)
    def get(self):
        return professores

    @ns_prof.expect(professor_model)
    @ns_prof.marshal_with(professor_model, code=201)
    def post(self):
        novo = api.payload
        novo["id"] = len(professores) + 1
        professores.append(novo)
        return novo, 201

@ns_prof.route("/<int:id>")
class Professor(Resource):
    @ns_prof.marshal_with(professor_model)
    def get(self, id):
        for p in professores:
            if p["id"] == id:
                return p
        api.abort(404, "Professor não encontrado")

# ====================
# ALUNOS
# ====================
@ns_aluno.route("/")
class AlunoList(Resource):
    @ns_aluno.marshal_list_with(aluno_model)
    def get(self):
        return alunos

    @ns_aluno.expect(aluno_model)
    @ns_aluno.marshal_with(aluno_model, code=201)
    def post(self):
        novo = api.payload
        novo["id"] = len(alunos) + 1
        alunos.append(novo)
        return novo, 201

@ns_aluno.route("/<int:id>")
class Aluno(Resource):
    @ns_aluno.marshal_with(aluno_model)
    def get(self, id):
        for a in alunos:
            if a["id"] == id:
                return a
        api.abort(404, "Aluno não encontrado")

# ====================
# TURMAS
# ====================
@ns_turma.route("/")
class TurmaList(Resource):
    @ns_turma.marshal_list_with(turma_model)
    def get(self):
        return turmas

    @ns_turma.expect(turma_model)
    @ns_turma.marshal_with(turma_model, code=201)
    def post(self):
        nova = api.payload
        nova["id"] = len(turmas) + 1
        turmas.append(nova)
        return nova, 201

@ns_turma.route("/<int:id>")
class Turma(Resource):
    @ns_turma.marshal_with(turma_model)
    def get(self, id):
        for t in turmas:
            if t["id"] == id:
                return t
        api.abort(404, "Turma não encontrada")

# ====================
# RODA APP
# ====================
if __name__ == "__main__":
    app.run(debug=True)
