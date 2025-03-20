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
            self.assertEqual({'mensagem': 'ID inserido para professor precisa ser um numero inteiro'}, resp_retornada)
    
    def test_003_id_de_professor_menor_igual_que_zero(self):
        resposta = requests.get('http://localhost:5003/professores/-1')
        if resposta.status_code == 400:
            resp_retornada = resposta.json()                
            self.assertEqual({'mensagem': 'ID do professor nao pode ser menor ou igual a que zero'}, resp_retornada)

    def test_004_id_de_professor_inexistente(self):
        resposta = requests.get('http://localhost:5003/professores/500')
        if resposta.status_code == 404:
            resp_retornada = resposta.json()                
            self.assertEqual({'mensagem': 'Professor(a) nao encontrado(a)/inexistente'}, resp_retornada)

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
            self.assertEqual({'mensagem': 'Para criar um novo professor preciso que voce me passe os parâmetros nome e materia'}, resp_retornada)

    def test_006_se_idade_nao_for_inserida(self):
        novo_professor = {
            "nome": "Simas",
            "materia": "Fisica",
            "salario": 1500.00
        }

        resposta = requests.post('http://localhost:5003/professores', json=novo_professor)
        if 'id' not in novo_professor:
            resp_retornada = resposta.json()
            self.assertEqual({'mensagem': 'Idade e obrigatoria, por favor insira-a'}, resp_retornada)
    
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
            self.assertEqual({'mensagem': 'Os parametros nome e/ou materia precisam ser do tipo STRING'}, resp_retornada)
    
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
            self.assertEqual({'mensagem': 'Idade precisa ser um número INTEIRO'}, resp_retornada)

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
            self.assertEqual({'mensagem':'O parametro de salário precisa ser um número do tipo float ou int'}, resp_retornada)

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
            self.assertEqual({'mensagem': 'Um professor precisa ter no minimo 18 anos'}, resp_retornada)
    
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
            self.assertEqual({'mensagem': 'Esse professor não tem condiçoes de dar aula, idade muito alta'}, resp_retornada)

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
            self.assertEqual({'mensagem': 'Idade não pode ser negativa!!'}, resp_retornada)

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
            self.assertEqual ({'mensagem': 'Salario precisa ser no minino a partir de R$1400.00 e nao pode ser negativo'}, resp_retornada)

    def test_014_se_tem_chaves_invalidas(self):
        novo_professor = {
            "nome": "João ",
            "idade": 55,
            "materia": "Fisica",
            "endereco": "Aristoteles 1895",
            "telefone": "4002-8922"
        }
        resposta = requests.post('http://localhost:5003/professores', json=novo_professor)
        resp_retornada = resposta.json()
        self.assertIn('chaves_invalidas', resp_retornada)
        self.assertEqual(set(resp_retornada['chaves_invalidas']), {'endereco', 'telefone'})

    def test_015_se_id_nao_for_int_no_put(self):
        resposta = requests.put('http://localhost:5003/professores/1.5')
        
        if resposta.status_code == 404:
            resp_retornada = resposta.json()
            self.assertEqual({'mensagem': 'ID IVÁLIDO, id precisa ser do tipo inteiro'}, resp_retornada)
    
    def test_016_se_id_de_professor_no_put_menor_igual_que_zero(self):
        resposta = requests.put('http://localhost:5003/professores/-1')
        if resposta.status_code == 404:
            resp_retornada = resposta.json()

            self.assertEqual({'mensagem': 'Valor de ID inválido, ID precisa ser MAIOR QUE ZERO'}, resp_retornada)

    def test_017_se_tem_chaves_invalidas_no_put(self):
        prof_atualizado = {
            "nome": "João",
            "idade": 55,
            "materia": "Artes e Flisofia",
            "endereco": "Ser ou não ser 1040b",
            "telefone": "4002-8922"
        }
        resposta = requests.put('http://localhost:5003/professores/5', json=prof_atualizado)
        resp_retornada = resposta.json()
        self.assertIn('chaves_invalidas', resp_retornada)
        self.assertEqual(set(resp_retornada['chaves_invalidas']), {'endereco', 'telefone'})

    def test_018_se_no_put_nome_e_string_ou_esta_vazio(self):

        novo_professor = {
            "nome": 15,
            "idade": 55,
            "materia": "Artes e Flisofia",
        }
        resposta = requests.put('http://localhost:5003/professores/5', json=novo_professor)
        resp_retornada = resposta.json()
        self.assertEqual({'mensagem': 'Para realizar atualização de professor valor para a chave nome precisa ser do tipo STRING e não pode estar vazia'}, resp_retornada)

    
    def test_019_idade_nao_inteiro_no_put(self):
        professor_atualizado = {
            "nome": "João",
            "idade": "quarenta e cinco",  
            "materia": "Artes e Filosofia",
            "salario": 5800.0
        }

        resposta = requests.put('http://localhost:5003/professores/1', json=professor_atualizado)
        resp_retornada = resposta.json()
        self.assertEqual({'mensagem': 'Essa nova idade para professor está inválida, idade tem que ser obrigatóriamente do tipo INTEIRO'}, resp_retornada)

    
    def test_020_idade_maior_que_120_no_put(self):
        professor_atualizado = {
            "nome": "João",
            "idade": 121,  
            "materia": "Artes e Filosofia",
            "salario": 5800.0
        }

        resposta = requests.put('http://localhost:5003/professores/1', json=professor_atualizado)
        resp_retornada = resposta.json()
        self.assertEqual({'mensagem': 'Essa nova idade está muito avançada para dar aulas, talvez nem esteja vivo'}, resp_retornada)

    def test_021_idade_menor_que_18_no_put(self):
        professor_atualizado = {
            "nome": "João",
            "idade": 17,  
            "materia": "Artes e Filosofia",
            "salario": 5800.0
        }

        resposta = requests.put('http://localhost:5003/professores/1', json=professor_atualizado)
        resp_retornada = resposta.json()
        self.assertEqual({'mensagem': 'Idade professor não pode ser negativa ou menor que 18 anos'}, resp_retornada)

    def test_022_se_materia_nao_for_string_no_put(self):
        prof_atualizado = {
            "nome": "João",
            "idade": 55,
            "materia": 12345, 
            "salario": 1500.0
        }

        resposta = requests.put('http://localhost:5003/professores/1', json=prof_atualizado)
        resp_retornada = resposta.json()
        self.assertEqual({'mensagem': 'O valor inserido em chave matéria precisa ser do tipo String e não pode estar vazia'}, resp_retornada)

    def test_023_se_salario_nao_for_float_ou_int_no_put(self):
        prof_atualizado = {
            "nome": "João",
            "idade": 55,
            "materia": "Artes e Filosofia",
            "salario": "mil e quinhentos"
        }

        resposta = requests.put('http://localhost:5003/professores/1', json=prof_atualizado)
        resp_retornada = resposta.json()
        self.assertEqual({'mensagem': 'O valor da chave salário precisa ser do um número com ponto flutuante (FLOAT, ex: 1400.0), ou int(1400) para que possa existir a converção'}, resp_retornada)

    def test_024_se_salario_for_menor_que_1400_no_put(self):
        prof_atualizado = {
            "nome": "João",
            "idade": 55,
            "materia": "Artes e Filosofia",
            "salario": 1200.0  
        }

        resposta = requests.put('http://localhost:5003/professores/1', json=prof_atualizado)
        resp_retornada = resposta.json()
        self.assertEqual({'mensagem': 'O novo valor para salário deve ser no mínimo 1400 e não pode ser negativo'}, resp_retornada)

    def test_025_id_invalido_nao_inteiro_no_delete(self):
        resposta = requests.delete('http://localhost:5003/professores/1.5')
        
        if resposta.status_code == 404:
            resp_retornada = resposta.json()
            self.assertEqual({'mensagem': 'ID IVÁLIDO, id precisa ser do tipo inteiro para que eu possa deletar'}, resp_retornada)

    def test_026_id_invalido_menor_igual_zero_delete(self):
        resposta = requests.delete('http://localhost:5003/professores/0')
        
        if resposta.status_code == 404:
            resp_retornada = resposta.json()
            self.assertEqual({'mensagem': 'Valor de ID inválido, ID precisa ser MAIOR QUE ZERO para que eu possa deletar'}, resp_retornada)
    
    def test_027_id_nao_encontrado_falha_ao_deletar(self):
        resposta = requests.delete('http://localhost:5003/professores/9999')
        
        if resposta.status_code == 404:
            resp_retornada = resposta.json()
            self.assertEqual({'mensagem': 'id de professor não encontrado, falha ao deletar'}, resp_retornada)


         
        # ---------------------------------------------TURMAS------------------------------------------------ #

    def test_022_turmas_retorna_lista(self):
        resposta = requests.get('http://localhost:5003/turmas')

        
        if resposta.status_code == 404:
            self.fail("voce nao definiu a pagina /turmas no seu server")

        try:
            obj_retornado = resposta.json()
        
        except:
            self.fail("queria um json mas voce retornou outra coisa")

        self.assertEqual(type(obj_retornado),type([]))

    def test_016_id_de_turma_não_int(self):
        resposta = requests.get('http://localhost:5003/turmas/1.5')
        if resposta.status_code == 400:
            resp_retornada = resposta.json()
            self.assertEqual({'mensagem': 'ID inserido para turma precisa ser um numero inteiro'}, resp_retornada)

    def test_017_id_de_turma_menor_igual_que_zero(self):
        resposta = requests.get('http://localhost:5003/turmas/-1')
        if resposta.status_code == 400:
            resp_retornada = resposta.json()                
            self.assertEqual({'mensagem': 'ID de turma nao pode ser menor ou igual a que zero'}, resp_retornada)


    def test_018_id_de_turma_inexistente(self):
        resposta = requests.get('http://localhost:5003/turmas/500')
        if resposta.status_code == 404:
            resp_retornada = resposta.json()
            self.assertEqual({'mensagem': 'Turma nao encontrada/inexistente'}, resp_retornada)
    
    def test_019_se_em_turma_as_chaves_professor_id_e_descricao_nao_forem_informados(self):
        nova_turma = {
            "descricao": "7 ano D",
            "ativo": True
        }

        resposta = requests.post('http://localhost:5003/turmas', json=nova_turma)
        resp_retornada = resposta.json()
        self.assertEqual({'mensagem': 'Para criar uma nova turma, é obrigatório inserir a chave id_professor e descricao'}, resp_retornada)
    
    def test_020_se_a_chave_descricao_nao_for_string_ou_esta_vazia(self):
        nova_turma = {
            "descricao": "  ",
            "ativo": True,
            "professor_id": 4
        }

        resposta = requests.post('http://localhost:5003/turmas', json=nova_turma)
        resp_retornada = resposta.json()
        self.assertEqual({'mensagem': 'decricao precisa ser uma STRING e/ou não pode estar vazia'}, resp_retornada)
    
    def test_021_verifica_se_chave_ativa_foi_informada_e_se_seu_tipo_e_boolean(self):
        nova_turma = {
            "descricao": "7 ano D",
            "ativo": 12,
            "professor_id": 4
        }
        resposta = requests.post('http://localhost:5003/turmas', json=nova_turma)
        resp_retornada = resposta.json()
        self.assertEqual({'mensagem': 'a chave ativo, precisa ser de valor booleano (true ou false)'}, resp_retornada)

    def test_022_caso_descricao_inserida_em_turma_ja_esteja_em_nosso_banco_de_dados(self):
        nova_turma = {
            "descricao": "7 ano A",
            "ativo": True,
            "professor_id": 4
        }
        resposta = requests.post('http://localhost:5003/turmas', json=nova_turma)
        resp_retornada = resposta.json()
        self.assertEqual( {'mensagem': f'A turma com a descricao {nova_turma["descricao"].title()} ja existe'}, resp_retornada)
    def test_023_caso_professor_id_inserido_ja_esteje_responsavel_por_alguma_turma(self):

        nova_turma = {
            "descricao": "7 ano D",
            "ativo": True,
            "professor_id": 2
        }
        resposta = requests.post('http://localhost:5003/turmas', json=nova_turma)
        resp_retornada = resposta.json()
        self.assertEqual({'mensagem': 'O professor cujo id mencionado já é responsavel por uma sala, insira um id de professor que nao esta sendo responsavel por alguma turma'}, resp_retornada)
    


    def test_024_caso_professor_id_nao_seja_int(self):
        nova_turma = {
            "descricao": "7 ano D",
            "ativo": True,
            "professor_id": "oito"
        }
                
        resposta = requests.post('http://localhost:5003/turmas', json=nova_turma)
        resp_retornada = resposta.json() 
        self.assertEqual({'mensagem': 'A chave professor_id precisa ser um número INTEIRO'}, resp_retornada)
    def test_025_se_professor_id_for_menor_igual_a_zero(self):
        nova_turma = {
            "descricao": "7 ano D",
            "ativo": True,
            "professor_id": -1
        }

        resposta = requests.post('http://localhost:5003/turmas', json=nova_turma)
        resp_retornada = resposta.json() 
        self.assertEqual({'mensagem': 'chave professor_id Inválida!!!! O valor inserido nessa chave não pode ser menor ou igual a zero'}, resp_retornada)

    def test_026_caso_tenha_chaves_invalidas(self):
        nova_turma = {
            "descricao": "7 ano D",
            "ativo": True,
            "professor_id": 4,
            "melhor_nota": 10
        }

        resposta = requests.post('http://localhost:5003/turmas', json=nova_turma)
        resp_retornada = resposta.json()
        assert 'chaves_invalidas' in resp_retornada
        assert set(resp_retornada['chaves_invalidas']) == {'melhor_nota'}

    def test_027_id_invalido_nao_inteiro_no_delete(self):
        resposta = requests.delete('http://localhost:5003/turmas/1.5')
        resp_retornada = resposta.json()
        self.assertEqual({'mensagem': 'ID de turma inválido. O ID precisa ser um número inteiro para que a turma possa ser deletada.'}, resp_retornada)

    def test_028_id_invalido_menor_igual_zero_delete(self):
        resposta = requests.delete('http://localhost:5003/turmas/0')
        resp_retornada = resposta.json()
        self.assertEqual({'mensagem': 'ID de turma inválido. O ID precisa ser maior que zero para que a turma possa ser deletada.'}, resp_retornada)
    
    def test_029_id_nao_encontrado_falha_ao_deletar(self):
        resposta = requests.delete('http://localhost:5003/turmas/9999')
        resp_retornada = resposta.json()
        self.assertEqual({'mensagem': 'ID de turma não encontrado/inexistente, falha ao deletar'}, resp_retornada)
    


# -----------------------------------------------ALUNOS---------------------------------------------- #

    def test_027_alunos_retorna_lista(self):
        resposta = requests.get('http://localhost:5003/alunos')

        if resposta.status_code == 404:
            self.fail("voce nao definiu a pagina /alunos no seu server")
        
        try:
            obj_retornado = resposta.json()
       
        except:
            self.fail("queria um json mas voce retornou outra coisa")

        self.assertEqual(type(obj_retornado),type([]))

    def test_028_id_de_aluno_não_int(self):
        resposta = requests.get('http://localhost:5003/alunos/1.5')
        if resposta.status_code == 400:
            resp_retornada = resposta.json()
            self.assertEqual ({'mensagem': 'ID inserido para aluno tem que ser um numero inteiro'}, resp_retornada)

    def test_029_id_de_aluno_menor_igual_que_zero(self):
        resposta = requests.get('http://localhost:5003/alunos/-1')
        if resposta.status_code == 400:
            resp_retornada = resposta.json()  
            self.assertEqual({'mensagem': 'ID do aluno nao pode ser menor ou igual a que zero'}, resp_retornada)


    def test_030_id_de_aluno_inexistente(self):
        resposta = requests.get('http://localhost:5003/alunos/500')
        if resposta.status_code == 404:
            resp_retornada = resposta.json()
            self.assertEqual({'mensagem': 'Aluno(a) nao encontrado(a)/inexistente'}, resp_retornada)


    def test_031_se_nome_e_turma_id_nao_forem_inseridos(self):
        novo_aluno = {
            "idade": 13,
            "turma_id": 4,
            "nota_primeiro_semestre": 5
        }

        resposta = requests.post('http://localhost:5003/alunos', json=novo_aluno)
        resp_retornada = resposta.json()
        self.assertEqual({'mensagem': 'Os campos nome, turma_id são OBRIGATÓRIOS'}, resp_retornada)

    def test_032_se_turma_id_for_menor_que_zero(self):
        novo_aluno = {
            "nome": "Jose Paulo",
            "idade": 13,
            "turma_id": -1,
        }
        resposta = requests.post('http://localhost:5003/alunos', json=novo_aluno)
        resp_retornada = resposta.json()
        self.assertEqual({'mensagem': 'O valor informado para a chave turma_id é INVÁLIDO (não pode ser negativo)'}, resp_retornada)
    
    def test_033_se_turma_id_não_existe(self):
        novo_aluno = {
            "nome": "Jose Paulo",
            "idade": 13,
            "turma_id": 10,
        }
        resposta = requests.post('http://localhost:5003/alunos', json=novo_aluno)
        resp_retornada = resposta.json()
        self.assertEqual({'mensagem': 'Chave turma_id Inválida ou não essa turma não existe'}, resp_retornada)

    def test_034_se_nome_nao_for_string(self):
        novo_aluno = {
            "nome": 50,
            "idade": 13,
            "turma_id": 11,
            "nota_primeiro_semestre": 5
        }

        resposta = requests.post('http://localhost:5003/alunos', json=novo_aluno)
        resp_retornada = resposta.json()
        self.assertEqual({'mensagem': 'Chave nome precisa ser do tipo string'}, resp_retornada)


    def test_035_se_turma_id_ou_idade_nao_forem_inteiros(self):
        novo_aluno = {
            "nome": "Jose Paulo",
            "idade": "treze",
            "turma_id": 11
        }
        resposta = requests.post('http://localhost:5003/alunos', json=novo_aluno)
        resp_retornada = resposta.json()
        self.assertEqual({'mensagem': 'O valor informado para as chaves idade e turma_id precisam ser INTEIROS'}, resp_retornada)

    def test_036_se_idade_for_menor_igual_que_zero(self):
        novo_aluno = {
            "nome": "Jose Paulo",
            "idade": -1,
            "turma_id": 11
        }
        resposta = requests.post('http://localhost:5003/alunos', json=novo_aluno)
        resp_retornada = resposta.json()
        self.assertEqual({'mensagem': 'O valor informado na chave idade não pode ser negativo ou igual a zero'}, resp_retornada)

    def test_037_se_data_nascimento_nao_for_string(self):
        novo_aluno = {
            "nome": "Jose Paulo",
            "idade": 13,
            "turma_id": 11,
            "data_nascimento": 2
        }
        resposta = requests.post('http://localhost:5003/alunos', json=novo_aluno)
        resp_retornada = resposta.json()
        self.assertEqual({'mensagem': 'Data de Nascimento precisa ser uma string dd-mm-aaaa'}, resp_retornada)


    def test_038_se_as_notas_do_semestre_um_ou_2_junto_da_media_nao_forem_inteiros_ou_float(self):
        novo_aluno = {
            "nome": "Jose Paulo",
            "idade": 13,
            "turma_id": 11,
            "nota_primeiro_semestre": "oito",
            "nota_segundo_semestre": 10.0,
            "media_final": 9.0
        }

        resposta = requests.post('http://localhost:5003/alunos', json=novo_aluno)
        resp_retornada = resposta.json()
        print(resp_retornada)
        self.assertEqual({'mensagem': 'Os valores para as notas de primeiro, segundo, semestre, precisao ser do tipo INTEIRO ou FLOAT'}, resp_retornada)

    
    def test_039_se_notas_ou_media_inserida_forem_negativas(self):
        novo_aluno = {
            "nome": "Jose Paulo",
            "idade": 13,
            "turma_id": 11,
            "nota_primeiro_semestre": -10,
            "nota_segundo_semestre": 10,
            "media_final": 0
        }
        resposta = requests.post('http://localhost:5003/alunos', json=novo_aluno)
        resp_retornada = resposta.json()
        print(resp_retornada)
        self.assertEqual({'mensagem' : 'As notas e a media precisam receber um valor inteiro ou float'}, resp_retornada)


    def test_040_se_tem_chaves_invalidas(self):
        novo_aluno = {
            "nome": "Jose Paulo",
            "idade": 13,
            "turma_id": 11,
            "data_nascimento": "12-10-2011",
            "nota_primeiro_semestre": 10,
            "nota_segundo_semestre": 10,
            "media_final": 10,
            "nome_do_responsavel": "Josiane de Paula",
            "endereço": "Cid. Tiradentes SP, 404- ZL"
        }

        resposta = requests.post('http://localhost:5003/alunos', json=novo_aluno)
        resp_retornada = resposta.json()
        self.assertIn('chaves_invalidas', resp_retornada)
        self.assertEqual(set(resp_retornada['chaves_invalidas']), {'nome_do_responsavel', 'endereço'})