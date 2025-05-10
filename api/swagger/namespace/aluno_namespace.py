from flask_restx import Namespace, Resource, fields
from alunos.alunos_model import listar_alunos, aluno_por_id, criar_aluno, atualizar_aluno, deletar_aluno

alunos_ns = Namespace("alunos", description="Operações relacionadas aos alunos")

aluno_model = alunos_ns.model("Aluno", {
    "nome": fields.String(required=True, description="Nome do aluno"),
    "data_nascimento": fields.String(required=True, description="Data de nascimento (YYYY-MM-DD)"),
    "nota_primeiro_semestre": fields.Float(required=True, description="Nota do primeiro semestre"),
    "nota_segundo_semestre": fields.Float(required=True, description="Nota do segundo semestre"),
    "turma_id": fields.Integer(required=True, description="ID da turma em que o aluno está estudando"),
})

aluno_output_model = alunos_ns.model("AlunoOutput", {
    "id": fields.Integer(description="ID do aluno"),
    "nome": fields.String(description="Nome do aluno"),
    "idade": fields.Integer(description="Idade do aluno"),
    "data_nascimento": fields.String(description="Data de nascimento (YYYY-MM-DD)"),
    "nota_primeiro_semestre": fields.Float(description="Nota do primeiro semestre"),
    "nota_segundo_semestre": fields.Float(description="Nota do segundo semestre"),
    "media_final": fields.Float(description="Média final do aluno de acordo com as suas notas do primeiro e segundo semestre"),
    "turma_id": fields.Integer(description="ID da turma em que o aluno está estudando"),
})

@alunos_ns.route("/")
class AlunosResource(Resource):
    @alunos_ns.marshal_list_with(aluno_output_model)
    def get(self):
        """Lista todos os alunos do nosso banco de dados"""
        return listar_alunos()
    
    @alunos_ns.expect(aluno_model)
    def post(self):
        """Cria um novo aluno no banco de dados"""
        data = alunos_ns.payload
        response, status_code = criar_aluno(data)
        return response, status_code
    
@alunos_ns.route("/<int:id_aluno>")
class AlunoIdResource(Resource):
    @alunos_ns.marshal_with(aluno_output_model)
    def get(self, id_aluno):
        """Mostra os dados de um aluno pelo seu ID"""
        return aluno_por_id(id_aluno)

    @alunos_ns.expect(aluno_model)
    def put(self, id_aluno):
        """Atualiza os Dados de um aluno pelo seu ID"""
        data = alunos_ns.payload
        atualizar_aluno(id_aluno, data)
        return data, 200

    def delete(self, id_aluno):
        """Deleta o aluno pelo seu ID"""
        deletar_aluno(id_aluno)