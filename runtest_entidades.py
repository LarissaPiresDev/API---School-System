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




