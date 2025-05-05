from flask_restx import Namespace, Resource, fields
from turma.turmas_model import listarTurmas, listarTurmaPorId, criarturma, atualizar_turma, deletarTurma 

turma_ns = Namespace("turma", description="Operações relacionadas as turmas")

turma_model = turma_ns.model("turma", {
    "descricao": fields.String(required=True, description="Descrição da turma (nome dela)"),
    "professor_id": fields.Integer(required=True, description="ID do professor coordenador da turma"),
    "ativo": fields.Boolean(required=True, description="Situação da turma (se a turma esta ativada ou não)"),
})

turma_output_model = turma_ns.model("turmaOutput", {
    "id": fields.Integer(description="ID da turma"),
    "descricao": fields.String(description="Descrição da turma"),
    "professor_id": fields.Integer(description="ID do professor"),
    "ativo": fields.Boolean(description="Situação da turma"),
})

@turma_ns.route("/")
class turmaResource(Resource):
    @turma_ns.marshal_list_with(turma_output_model)
    def get(self):
        """Lista os dados de todas as turmas presentes no banco de dados"""
        return listarTurmas()

@turma_ns.route("/<int:idTurma>")
class turmaIdResource(Resource):
    @turma_ns.marshal_with(turma_output_model)
    def get(self, idTurma):
        """Mostra os dados de um turma pelo seu ID"""
        return listarTurmaPorId(idTurma)


    @turma_ns.expect(turma_model)
    def post(self):
        """Cria uma nova turma"""
        data = turma_ns.payload
        response, status_code = criarturma(data)
        return response, status_code

    @turma_ns.expect(turma_model)
    def put(self, idTurma):
        """Atualiza os dados de uma turma pelo seu ID"""
        data = turma_ns.payload
        atualizar_turma(idTurma, data)
        return data, 200

    def delete(self, idTurma):
        """Exclui uma turma pelo seu ID"""
        deletarTurma(idTurma)
        return {"message": "turma excluído com sucesso"}, 200