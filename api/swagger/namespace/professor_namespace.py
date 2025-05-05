from flask_restx import Namespace, Resource, fields
from professor.professores_model import listar_professores, listar_professor_por_id, criar_professor, atualizar_professor, deletar_professor
from config import db

professor_ns = Namespace("professor", description="Operações relacionadas ao professor")

professor_model = professor_ns.model("professor", {
    "nome": fields.String(required=True, description="Nome do professor"),
    "idade": fields.Integer(required=True, description="Idade"),
    "materia": fields.String(required=True, description="Matéria que leciona"),
    "salario": fields.Float(required=True, description="Observações"),
})

professor_output_model = professor_ns.model("professorOutput", {
    "id": fields.Integer(description="ID do professor"),
    "nome": fields.String(description="Nome do professor"),
    "idade": fields.Integer(description="Idade do professor"),
    "materia": fields.String(description="Matéria que ao qual dão Aula"),
    "salario": fields.Float(description="Salario do Professor"),
})

@professor_ns.route("/")
class professorResource(Resource):
    @professor_ns.marshal_list_with(professor_output_model)
    def get(self):
        """Lista os dados de todos os professores"""
        return listar_professores()
    

@professor_ns.route("/<int:idProfessor>")
class professorIdResource(Resource):
    @professor_ns.marshal_with(professor_output_model)
    def get(self, idProfessor):
        """Mostra os dados de um professor pelo ID"""
        return listar_professor_por_id(idProfessor)

    @professor_ns.expect(professor_model)
    def post(self):
        """Cria um novo professor"""
        data = professor_ns.payload
        response, status_code = criar_professor(data)
        return response, status_code

    @professor_ns.expect(professor_model)
    def put(self, idProfessor):
        """Atualiza um professor pelo ID"""
        data = professor_ns.payload
        atualizar_professor(idProfessor, data)
        return data, 200

    def delete(self, idProfessor):
        """"Atualiza os dados de um professor pelo seu ID"""
        deletar_professor(idProfessor)
        return {"message": "professor excluído com sucesso"}, 200