import requests
import unittest


class TestStringMethods(unittest.TestCase):
#--------------------------------------------PROFESSORES------------------------------------------- #

    def test_001_professores_retorna_lista(self):
        resposta = requests.get('http://localhost:5003/professores')
        
        if resposta.status_code == 404:
            self.fail("voce nao definiu a pagina /professores no seu server")

        try:
            obj_retornado = resposta.json()
        
        except:
            self.fail("queria um json mas voce retornou outra coisa")

        self.assertEqual(type(obj_retornado),type([]))

    def test_002_id_de_professor_não_int(self):
        resposta = requests.get('http://localhost:5003/professores/1.5')
        
        if resposta.status_code == 400:
            resp_retornada = resposta.json()
            assert {'mensagem': 'ID inserido para professor precisa ser um numero inteiro'} == resp_retornada
    
    def test_003_id_de_professor_menor_igual_que_zero(self):
        resposta = requests.get('http://localhost:5003/professores/-1')
        if resposta.status_code == 400:
            resp_retornada = resposta.json()                
            assert {'mensagem': 'ID do professor nao pode ser menor ou igual a que zero'} == resp_retornada

    def test_004_id_de_professor_inexistente(self):
        resposta = requests.get('http://localhost:5003/professores/500')
        if resposta.status_code == 404:
            resp_retornada = resposta.json()                
            assert {'mensagem': 'Professor(a) nao encontrado(a)/inexistente'} == resp_retornada

    def test_005_se_nome_materia_foram_inseridos(self):
        novo_professor = {
            "nome": "",
            "idade": 45,
            "materia": "Fisica",
            "salario": 1500.00
        }

        resposta = requests.post('http://localhost:5003/professores', json=novo_professor)
        if not novo_professor['nome'] or not novo_professor['materia']:
            resp_retornada = resposta.json()
            assert {'mensagem': 'Para criar um novo professor preciso que voce me passe os parâmetros nome e materia'} == resp_retornada    

    def test_006_se_idade_nao_for_inserida(self):
        novo_professor = {
            "nome": "Simas",
            "materia": "Fisica",
            "salario": 1500.00
        }

        resposta = requests.post('http://localhost:5003/professores', json=novo_professor)
        if 'id' not in novo_professor:
            resp_retornada = resposta.json()
            assert {'mensagem': 'Idade e obrigatoria, por favor insira-a'} == resp_retornada
    
    def test_007_se_nome_e_materia_de_professor_nao_forem_strings(self):
        novo_professor = {
            "nome": 12345,
            "idade": 45,
            "materia": "Fisica",
            "salario": 1500.00
        }
        resposta = requests.post('http://localhost:5003/professores', json=novo_professor)
        if not isinstance(novo_professor["nome"], str) or not isinstance(novo_professor["materia"], str):
            resp_retornada = resposta.json()
            assert {'mensagem': 'Os parametros nome e/ou materia precisam ser do tipo STRING'} == resp_retornada
    
    def test_008_se_idade_nao_for_um_numero_inteiro(self):
        novo_professor = {
            "nome": "Simas",
            "idade": 15.0,
            "materia": "Fisica",
            "salario": 1500.00
        }

        resposta = requests.post('http://localhost:5003/professores', json=novo_professor)
        if not isinstance(novo_professor['idade'], int):
            resp_retornada = resposta.json()
            assert {'mensagem': 'Idade precisa ser um número INTEIRO'} == resp_retornada

    def test_009_se_salario_nao_for_float_ou_int(self):
        novo_professor = {
            "nome": "Simas",
            "idade": 18,
            "materia": "Fisica",
            "salario": "mil e quinhentos"
        }

        resposta = requests.post('http://localhost:5003/professores', json=novo_professor)
        if not isinstance(novo_professor['salario'], (float, int)):
            resp_retornada = resposta.json()
            assert {'mensagem':'O parametro de salário precisa ser um número do tipo float ou int'} == resp_retornada

    def test_010_se_idade_menor_que_18(self):
        novo_professor = {
            "nome": "Simas",
            "idade": 16,
            "materia": "Fisica",
            "salario": 1500.00
        }
        resposta = requests.post('http://localhost:5003/professores', json=novo_professor)
        if novo_professor['idade'] >= 0 and novo_professor['idade'] < 18:
            resp_retornada = resposta.json()
            assert {'mensagem': 'Um professor precisa ter no minimo 18 anos'} == resp_retornada
    
    def test_011_se_idade_for_muito_alta(self):
        novo_professor = {
            "nome": "Simas",
            "idade": 120,
            "materia": "Fisica",
            "salario": 1500.00
        }
        resposta = requests.post('http://localhost:5003/professores', json=novo_professor)
        if novo_professor['idade'] > 18 and novo_professor['idade'] >= 120:
            resp_retornada = resposta.json()
            assert {'mensagem': 'Esse professor não tem condiçoes de dar aula, idade muito alta'} == resp_retornada

    def test_012_se_idade_e_negativa(self):
        novo_professor = {
            "nome": "Simas",
            "idade": -1,
            "materia": "Fisica",
            "salario": -180.90
        }
        resposta = requests.post('http://localhost:5003/professores', json=novo_professor)
        if novo_professor['idade'] < 0:
            resp_retornada = resposta.json()
            assert {'mensagem': 'Idade não pode ser negativa!!'} == resp_retornada

    def test_013_se_salario_for_negativo_ou_menor_que_1400(self):
        novo_professor = {
            "nome": "Simas",
            "idade": 18,
            "materia": "Fisica",
            "salario": -180.90
        }

        resposta = requests.post('http://localhost:5003/professores', json=novo_professor)
        if novo_professor['salario'] <= 1400.00:
            resp_retornada = resposta.json()
            assert {'mensagem': 'Salario precisa ser no minino a partir de R$1400.00 e nao pode ser negativo'} == resp_retornada

    def test_014_se_tem_chaves_invalidas(self):
        novo_professor = {
            "nome": "Simas",
            "idade": 45,
            "materia": "Fisica",
            "endereco": "Rua dos Fisicos e Quimicos 1895",
            "telefone": "4002-8922"
        }
        resposta = requests.post('http://localhost:5003/professores', json=novo_professor)
        resp_retornada = resposta.json()
        assert 'chaves_invalidas' in resp_retornada
        assert set(resp_retornada['chaves_invalidas']) == {'endereco', 'telefone'}
        # ---------------------------------------------TURMAS------------------------------------------------ #

    def test_001_turmas_retorna_lista(self):
        resposta = requests.get('http://localhost:5003/turmas')

        
        if resposta.status_code == 404:
            self.fail("voce nao definiu a pagina /turmas no seu server")

        try:
            obj_retornado = resposta.json()
        
        except:
            self.fail("queria um json mas voce retornou outra coisa")

        self.assertEqual(type(obj_retornado),type([]))

    def test_002_id_de_turma_não_int(self):
        resposta = requests.get('http://localhost:5003/turmas/1.5')
        if resposta.status_code == 400:
            resp_retornada = resposta.json()
            assert {'mensagem': 'ID inserido para turma precisa ser um numero inteiro'} == resp_retornada

    def test_003_id_de_turma_menor_igual_que_zero(self):
        resposta = requests.get('http://localhost:5003/turmas/-1')
        if resposta.status_code == 400:
            resp_retornada = resposta.json()                
            assert {'mensagem': 'ID de turma nao pode ser menor ou igual a que zero'} == resp_retornada


    def test_004_id_de_turma_inexistente(self):
        resposta = requests.get('http://localhost:5003/turmas/500')
        if resposta.status_code == 404:
            resp_retornada = resposta.json()
            assert {'mensagem': 'Turma nao encontrada/inexistente'} == resp_retornada
    
    def test_005_se_em_turma_as_chaves_professor_id_e_descricao_nao_forem_informados(self):
        nova_turma = {
            "descricao": "7 ano D",
            "ativo": True
        }

        resposta = requests.post('http://localhost:5003/turmas', json=nova_turma)
        resp_retornada = resposta.json()
        assert {'mensagem': 'Para criar uma nova turma, é obrigatório inserir a chave id_professor e descricao'}
    
    def test_006_se_a_chave_descricao_nao_for_string_ou_esta_vazia(self):
        nova_turma = {
            "descricao": "  ",
            "ativo": True,
            "professor_id": 4
        }

        resposta = requests.post('http://localhost:5003/turmas', json=nova_turma)
        resp_retornada = resposta.json()
        assert {'mensagem': 'decricao precisa ser uma STRING e/ou não pode estar vazia'} == resp_retornada
    
    def test_007_verifica_se_chave_ativa_foi_informada_e_se_seu_tipo_e_boolean(self):
        nova_turma = {
            "descricao": "7 ano D",
            "ativo": 12,
            "professor_id": 4
        }
        resposta = requests.post('http://localhost:5003/turmas', json=nova_turma)
        resp_retornada = resposta.json()
        assert {'mensagem': 'a chave ativo, precisa ser de valor booleano (true ou false)'} == resp_retornada

    def test_008_caso_descricao_inserida_em_turma_ja_esteja_em_nosso_banco_de_dados(self):
        nova_turma = {
            "descricao": "7 ano A",
            "ativo": True,
            "professor_id": 4
        }
        resposta = requests.post('http://localhost:5003/turmas', json=nova_turma)
        resp_retornada = resposta.json()
        assert {'mensagem': f'A turma com a descricao {nova_turma["descricao"].title()} ja existe'} == resp_retornada
    
    

# -----------------------------------------------ALUNOS---------------------------------------------- #

    def test_001_alunos_retorna_lista(self):
        resposta = requests.get('http://localhost:5003/alunos')

        if resposta.status_code == 404:
            self.fail("voce nao definiu a pagina /alunos no seu server")
        
        try:
            obj_retornado = resposta.json()
       
        except:
            self.fail("queria um json mas voce retornou outra coisa")

        self.assertEqual(type(obj_retornado),type([]))

    def test_002_id_de_aluno_não_int(self):
        resposta = requests.get('http://localhost:5003/alunos/1.5')
        if resposta.status_code == 400:
            resp_retornada = resposta.json()
            assert {'mensagem': 'ID inserido para aluno tem que ser um numero inteiro'} == resp_retornada

    def test_003_id_de_aluno_menor_igual_que_zero(self):
        resposta = requests.get('http://localhost:5003/alunos/-1')
        if resposta.status_code == 400:
            resp_retornada = resposta.json()  
            assert {'mensagem': 'ID do aluno nao pode ser menor ou igual a que zero'} == resp_retornada


    def test_004_id_de_aluno_inexistente(self):
        resposta = requests.get('http://localhost:5003/alunos/500')
        if resposta.status_code == 404:
            resp_retornada = resposta.json()
            assert {'mensagem': 'Aluno(a) nao encontrado(a)/inexistente'} == resp_retornada


