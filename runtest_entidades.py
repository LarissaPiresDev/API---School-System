import requests
import unittest


class TestStringMethods(unittest.TestCase):

        # ---------------------------------------------TURMAS------------------------------------------------ #

    def test_028_turmas_retorna_lista(self):
        resposta = requests.get('http://localhost:5003/turmas')

        
        if resposta.status_code == 404:
            self.fail("voce nao definiu a pagina /turmas no seu server")

        try:
            obj_retornado = resposta.json()
        
        except:
            self.fail("queria um json mas voce retornou outra coisa")

        self.assertEqual(type(obj_retornado),type([]))

    def test_029_id_de_turma_não_int(self):
        resposta = requests.get('http://localhost:5003/turmas/1.5')
        self.assertEqual(400, resposta.status_code)
        self.assertEqual({'mensagem': 'ID inserido para turma precisa ser um numero inteiro'}, resposta.json())

    def test_030_id_de_turma_menor_igual_que_zero(self):
        resposta = requests.get('http://localhost:5003/turmas/-1')
        self.assertEqual(400, resposta.status_code)
        self.assertEqual({'mensagem': 'ID de turma nao pode ser menor ou igual a que zero'}, resposta.json())


    def test_031_id_de_turma_inexistente(self):
        resposta = requests.get('http://localhost:5003/turmas/500')

        self.assertEqual(404, resposta.status_code)
        self.assertEqual({'mensagem': 'Turma nao encontrada/inexistente'}, resposta.json())
    
    def test_032_se_em_turma_as_chaves_professor_id_e_descricao_nao_forem_informados(self):
        nova_turma = {
            "descricao": "7 ano D",
            "ativo": True
        }

        resposta = requests.post('http://localhost:5003/turmas', json=nova_turma)
        self.assertEqual(400, resposta.status_code)
        self.assertEqual({'mensagem': 'Para criar uma nova turma, é obrigatório inserir a chave id_professor e descricao'}, resposta.json())
    
    def test_033_se_a_chave_descricao_nao_for_string_ou_esta_vazia(self):
        nova_turma = {
            "descricao": "  ",
            "ativo": True,
            "professor_id": 4
        }

        resposta = requests.post('http://localhost:5003/turmas', json=nova_turma)
        
        self.assertEqual({'mensagem': 'decricao precisa ser uma STRING e/ou não pode estar vazia'}, resposta.json())
    
    def test_034_verifica_se_chave_ativa_foi_informada_e_se_seu_tipo_e_boolean(self):
        nova_turma = {
            "descricao": "7 ano D",
            "ativo": 12,
            "professor_id": 4
        }
        resposta = requests.post('http://localhost:5003/turmas', json=nova_turma)
        self.assertEqual(400, resposta.status_code)
        self.assertEqual({'mensagem': 'a chave ativo, precisa ser de valor booleano (true ou false)'}, resposta.json())

    def test_035_caso_descricao_inserida_em_turma_ja_esteja_em_nosso_banco_de_dados(self):
        nova_turma = {
            "descricao": "7 ano A",
            "ativo": True,
            "professor_id": 4
        }
        resposta = requests.post('http://localhost:5003/turmas', json=nova_turma)
        self.assertEqual(400, resposta.status_code)
        self.assertEqual( {'mensagem': f'A turma com a descricao {nova_turma["descricao"].title()} ja existe'}, resposta.json())
        
    def test_036_caso_professor_id_inserido_ja_esteje_responsavel_por_alguma_turma(self):

        nova_turma = {
            "descricao": "7 ano D",
            "ativo": True,
            "professor_id": 2
        }
        resposta = requests.post('http://localhost:5003/turmas', json=nova_turma)
        self.assertEqual(400, resposta.status_code)
        self.assertEqual({'mensagem': 'O professor cujo id mencionado já é responsavel por uma sala, insira um id de professor que nao esta sendo responsavel por alguma turma'}, resposta.json())
    


    def test_037_caso_professor_id_nao_seja_int(self):
        nova_turma = {
            "descricao": "7 ano D",
            "ativo": True,
            "professor_id": "oito"
        }
                
        resposta = requests.post('http://localhost:5003/turmas', json=nova_turma) 
        self.assertEqual(400, resposta.status_code)
        self.assertEqual({'mensagem': 'A chave professor_id precisa ser um número INTEIRO'}, resposta.json())
        
    def test_038_se_professor_id_for_menor_igual_a_zero(self):
        nova_turma = {
            "descricao": "7 ano D",
            "ativo": True,
            "professor_id": -1
        }

        resposta = requests.post('http://localhost:5003/turmas', json=nova_turma) 
        self.assertEqual(400, resposta.status_code)
        self.assertEqual({'mensagem': 'chave professor_id Inválida!!!! O valor inserido nessa chave não pode ser menor ou igual a zero'}, resposta.json())

    def test_039_caso_tenha_chaves_invalidas(self):
        nova_turma = {
            "descricao": "7 ano D",
            "ativo": True,
            "professor_id": 4,
            "melhor_nota": 10
        }

        resposta = requests.post('http://localhost:5003/turmas', json=nova_turma)
        self.assertEqual(400, resposta.status_code)
        self.assertIn('chaves_invalidas', resposta.json())
        self.assertEqual(set(resposta.json()['chaves_invalidas']), {'melhor_nota'})

    # PUT
    
    def test_051_id_invalido_nao_inteiro_no_delete(self):
        resposta = requests.delete('http://localhost:5003/turmas/1.5')
        self.assertEqual(400, resposta.status_code)
        self.assertEqual({'mensagem': 'ID de turma inválido. O ID precisa ser um número inteiro para que a turma possa ser deletada.'}, resposta.json())

    def test_052_id_invalido_menor_igual_zero_delete(self):
        resposta = requests.delete('http://localhost:5003/turmas/0')
        self.assertEqual(400, resposta.status_code)
        self.assertEqual({'mensagem': 'ID de turma inválido. O ID precisa ser maior que zero para que a turma possa ser deletada.'}, resposta.json())
    
    def test_053_id_nao_encontrado_falha_ao_deletar(self):
        resposta = requests.delete('http://localhost:5003/turmas/9999')
        self.assertEqual(404, resposta.status_code)
        self.assertEqual({'mensagem': 'ID de turma não encontrado/inexistente, falha ao deletar'}, resposta.json())



if __name__ == '__main__':
    unittest.main()