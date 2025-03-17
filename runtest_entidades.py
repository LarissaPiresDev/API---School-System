import requests
import unittest


class TestStringMethods(unittest.TestCase):
#--------------------------------------------PROFESSORES------------------------------------------- #

    def test_001_professores_retorna_lista(self):
        resposta = requests.get('http://localhost:5002/professores')
        
        if resposta.status_code == 404:
            self.fail("voce nao definiu a pagina /professores no seu server")

        try:
            obj_retornado = resposta.json()
        
        except:
            self.fail("queria um json mas voce retornou outra coisa")

        self.assertEqual(type(obj_retornado),type([]))

    def test_002_id_de_professor_não_int(self):
        resposta = requests.get('http://localhost:5002/professores/1.5')
        
        if resposta.status_code == 400:
            resp_retornada = resposta.json()
            assert {'mensagem': 'ID inserido para professor precisa ser um numero inteiro'} == resp_retornada
    
    def test_003_id_de_professor_menor_igual_que_zero(self):
        resposta = requests.get('http://localhost:5002/professores/-1')
        if resposta.status_code == 400:
            resp_retornada = resposta.json()                
            assert {'mensagem': 'ID do professor nao pode ser menor ou igual a que zero'} == resp_retornada

    def test_004_id_de_professor_inexistente(self):
        resposta = requests.get('http://localhost:5002/professores/500')
        if resposta.status_code == 404:
            resp_retornada = resposta.json()                
            assert {'mensagem': 'Professor(a) nao encontrado(a)/inexistente'} == resp_retornada

# ---------------------------------------------TURMAS------------------------------------------------ #

    def test_001_turmas_retorna_lista(self):
        resposta = requests.get('http://localhost:5002/turmas')

        
        if resposta.status_code == 404:
            self.fail("voce nao definiu a pagina /turmas no seu server")

        try:
            obj_retornado = resposta.json()
        
        except:
            self.fail("queria um json mas voce retornou outra coisa")

        self.assertEqual(type(obj_retornado),type([]))

    def test_002_id_de_turma_não_int(self):
        resposta = requests.get('http://localhost:5002/turmas/1.5')
        if resposta.status_code == 400:
            resp_retornada = resposta.json()
            assert {'mensagem': 'ID inserido para turma precisa ser um numero inteiro'} == resp_retornada

    def test_003_id_de_turma_menor_igual_que_zero(self):
        resposta = requests.get('http://localhost:5002/turmas/-1')
        if resposta.status_code == 400:
            resp_retornada = resposta.json()                
            assert {'mensagem': 'ID de turma nao pode ser menor ou igual a que zero'} == resp_retornada


    def test_004_id_de_turma_inexistente(self):
        resposta = requests.get('http://localhost:5002/turmas/500')
        if resposta.status_code == 404:
            resp_retornada = resposta.json()
            assert {'mensagem': 'Turma nao encontrada/inexistente'} == resp_retornada  


# -----------------------------------------------ALUNOS---------------------------------------------- #
    def test_001_alunos_retorna_lista(self):
        resposta = requests.get('http://localhost:5002/alunos')

        if resposta.status_code == 404:
            self.fail("voce nao definiu a pagina /alunos no seu server")
        
        try:
            obj_retornado = resposta.json()
       
        except:
            self.fail("queria um json mas voce retornou outra coisa")

        self.assertEqual(type(obj_retornado),type([]))


