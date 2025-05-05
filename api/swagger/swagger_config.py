from . import api
from swagger.namespace.professor_namespace import professor_ns
from swagger.namespace.turma_namespace import turma_ns
from swagger.namespace.aluno_namespace import alunos_ns


def configure_swagger(app):
    api.init_app(app)
    api.add_namespace(professor_ns, path="/professor")
    api.add_namespace(turma_ns, path="/turma")
    api.add_namespace(alunos_ns, path="/alunos")
    api.mask_swagger = False