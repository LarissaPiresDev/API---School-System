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
        self.assertEqual(400, resposta.status_code)
        self.assertEqual({'mensagem': 'ID inserido para professor precisa ser um numero inteiro'}, resposta.json())
    
    def test_003_id_de_professor_menor_igual_que_zero(self):
        resposta = requests.get('http://localhost:5003/professores/-1')
        self.assertEqual(400, resposta.status_code)
        self.assertEqual({'mensagem': 'ID do professor nao pode ser menor ou igual a que zero'}, resposta.json())

    def test_004_id_de_professor_inexistente(self):
        resposta = requests.get('http://localhost:5003/professores/500')       
        self.assertEqual(404, resposta.status_code)
        self.assertEqual({'mensagem': 'Professor(a) nao encontrado(a)/inexistente'}, resposta.json())

    def test_005_se_nome_materia_foram_inseridos(self):
        novo_professor = {
            "nome": "",
            "idade": 45,
            "materia": "Fisica",
            "salario": 1500.00
        }

        resposta = requests.post('http://localhost:5003/professores', json=novo_professor)
        self.assertEqual(400, resposta.status_code)
        self.assertEqual({'mensagem': 'Para criar um novo professor preciso que voce me passe os parâmetros nome e materia'}, resposta.json())

    def test_006_se_idade_nao_for_inserida(self):
        novo_professor = {
            "nome": "Simas",
            "materia": "Fisica",
            "salario": 1500.00
        }

        resposta = requests.post('http://localhost:5003/professores', json=novo_professor)
        self.assertEqual(400, resposta.status_code)
        self.assertEqual({'mensagem': 'Idade e obrigatoria, por favor insira-a'}, resposta.json())
    
    def test_007_se_nome_e_materia_de_professor_nao_forem_strings(self):
        novo_professor = {
            "nome": 12345,
            "idade": 45,
            "materia": "Fisica",
            "salario": 1500.00
        }
        resposta = requests.post('http://localhost:5003/professores', json=novo_professor)
        self.assertEqual(400, resposta.status_code)
        self.assertEqual({'mensagem': 'Os parametros nome e/ou materia precisam ser do tipo STRING'}, resposta.json())
    
    def test_008_se_idade_nao_for_um_numero_inteiro(self):
        novo_professor = {
            "nome": "Simas",
            "idade": 15.0,
            "materia": "Fisica",
            "salario": 1500.00
        }

        resposta = requests.post('http://localhost:5003/professores', json=novo_professor)
        self.assertEqual(400, resposta.status_code)
        self.assertEqual({'mensagem': 'Idade precisa ser um número INTEIRO'}, resposta.json())

    def test_009_se_salario_nao_for_float_ou_int(self):
        novo_professor = {
            "nome": "Simas",
            "idade": 18,
            "materia": "Fisica",
            "salario": "mil e quinhentos"
        }

        resposta = requests.post('http://localhost:5003/professores', json=novo_professor)
        self.assertEqual(400, resposta.status_code)
        self.assertEqual({'mensagem':'O parametro de salário precisa ser um número do tipo float ou int'}, resposta.json())

    def test_010_se_idade_menor_que_18(self):
        novo_professor = {
            "nome": "Simas",
            "idade": 16,
            "materia": "Fisica",
            "salario": 1500.00
        }
        resposta = requests.post('http://localhost:5003/professores', json=novo_professor)
        self.assertEqual(400, resposta.status_code)
        self.assertEqual({'mensagem': 'Um professor precisa ter no minimo 18 anos'}, resposta.json())
    
    def test_011_se_idade_for_muito_alta(self):
        novo_professor = {
            "nome": "Simas",
            "idade": 120,
            "materia": "Fisica",
            "salario": 1500.00
        }
        resposta = requests.post('http://localhost:5003/professores', json=novo_professor)
        self.assertEqual(400, resposta.status_code)
        self.assertEqual({'mensagem': 'Esse professor não tem condiçoes de dar aula, idade muito alta'}, resposta.json())

    def test_012_se_idade_e_negativa(self):
        novo_professor = {
            "nome": "Simas",
            "idade": -1,
            "materia": "Fisica",
            "salario": -180.90
        }
        resposta = requests.post('http://localhost:5003/professores', json=novo_professor)
        self.assertEqual(400, resposta.status_code)
        self.assertEqual({'mensagem': 'Idade não pode ser negativa!!'}, resposta.json())

    def test_013_se_salario_for_negativo_ou_menor_que_1400(self):
        novo_professor = {
            "nome": "Simas",
            "idade": 18,
            "materia": "Fisica",
            "salario": -180.90
        }

        resposta = requests.post('http://localhost:5003/professores', json=novo_professor)
        self.assertEqual(400, resposta.status_code)
        self.assertEqual ({'mensagem': 'Salario precisa ser no minino a partir de R$1400.00 e nao pode ser negativo'}, resposta.json())

    def test_014_se_tem_chaves_invalidas(self):
        novo_professor = {
            "nome": "João ",
            "idade": 55,
            "materia": "Fisica",
            "endereco": "Aristoteles 1895",
            "telefone": "4002-8922"
        }
        resposta = requests.post('http://localhost:5003/professores', json=novo_professor)
        self.assertIn('chaves_invalidas', resposta.json())
        self.assertEqual(set(resposta.json()['chaves_invalidas']), {'endereco', 'telefone'})

    def test_015_se_id_nao_for_int_no_put(self):
        resposta = requests.put('http://localhost:5003/professores/1.5')
        self.assertEqual(400, resposta.status_code)
        self.assertEqual({'mensagem': 'ID IVÁLIDO, id precisa ser do tipo inteiro'}, resposta.json())
    
    def test_016_se_id_de_professor_no_put_menor_igual_que_zero(self):
        resposta = requests.put('http://localhost:5003/professores/-1')
        self.assertEqual(400, resposta.status_code)
        self.assertEqual({'mensagem': 'Valor de ID inválido, ID precisa ser MAIOR QUE ZERO'}, resposta.json())

    def test_017_se_tem_chaves_invalidas_no_put(self):
        prof_atualizado = {
            "nome": "João",
            "idade": 55,
            "materia": "Artes e Flisofia",
            "endereco": "Ser ou não ser 1040b",
            "telefone": "4002-8922"
        }
        resposta = requests.put('http://localhost:5003/professores/5', json=prof_atualizado)
        self.assertIn('chaves_invalidas', resposta.json())
        self.assertEqual(400, resposta.status_code)
        self.assertEqual(set(resposta.json()['chaves_invalidas']), {'endereco', 'telefone'})

    def test_018_se_no_put_nome_e_string_ou_esta_vazio(self):

        novo_professor = {
            "nome": 15,
            "idade": 55,
            "materia": "Artes e Flisofia",
        }
        resposta = requests.put('http://localhost:5003/professores/5', json=novo_professor)
        self.assertEqual(400, resposta.status_code)
        self.assertEqual({'mensagem': 'Para realizar atualização de professor valor para a chave nome precisa ser do tipo STRING e não pode estar vazia'}, resposta.json())

    
    def test_019_idade_nao_inteiro_no_put(self):
        professor_atualizado = {
            "nome": "João",
            "idade": "quarenta e cinco",  
            "materia": "Artes e Filosofia",
            "salario": 5800.0
        }

        resposta = requests.put('http://localhost:5003/professores/1', json=professor_atualizado)
        self.assertEqual(400, resposta.status_code)
        self.assertEqual({'mensagem': 'Essa nova idade para professor está inválida, idade tem que ser obrigatóriamente do tipo INTEIRO'}, resposta.json())

    
    def test_020_idade_maior_que_120_no_put(self):
        professor_atualizado = {
            "nome": "João",
            "idade": 121,  
            "materia": "Artes e Filosofia",
            "salario": 5800.0
        }

        resposta = requests.put('http://localhost:5003/professores/1', json=professor_atualizado)
        self.assertEqual(400, resposta.status_code)
        self.assertEqual({'mensagem': 'Essa nova idade está muito avançada para dar aulas, talvez nem esteja vivo'}, resposta.json())

    def test_021_idade_menor_que_18_no_put(self):
        professor_atualizado = {
            "nome": "João",
            "idade": 17,  
            "materia": "Artes e Filosofia",
            "salario": 5800.0
        }

        resposta = requests.put('http://localhost:5003/professores/1', json=professor_atualizado)
        self.assertEqual(400, resposta.status_code)
        self.assertEqual({'mensagem': 'Idade professor não pode ser negativa ou menor que 18 anos'}, resposta.json())

    def test_022_se_materia_nao_for_string_no_put(self):
        prof_atualizado = {
            "nome": "João",
            "idade": 55,
            "materia": 12345, 
            "salario": 1500.0
        }

        resposta = requests.put('http://localhost:5003/professores/1', json=prof_atualizado)
        self.assertEqual(400, resposta.status_code)
        self.assertEqual({'mensagem': 'O valor inserido em chave matéria precisa ser do tipo String e não pode estar vazia'}, resposta.json())

    def test_023_se_salario_nao_for_float_ou_int_no_put(self):
        prof_atualizado = {
            "nome": "João",
            "idade": 55,
            "materia": "Artes e Filosofia",
            "salario": "mil e quinhentos"
        }

        resposta = requests.put('http://localhost:5003/professores/1', json=prof_atualizado)
        self.assertEqual(400, resposta.status_code)
        self.assertEqual({'mensagem': 'O valor da chave salário precisa ser do um número com ponto flutuante (FLOAT, ex: 1400.0), ou int(1400) para que possa existir a converção'}, resposta.json())

    def test_024_se_salario_for_menor_que_1400_no_put(self):
        prof_atualizado = {
            "nome": "João",
            "idade": 55,
            "materia": "Artes e Filosofia",
            "salario": 1200.0  
        }

        resposta = requests.put('http://localhost:5003/professores/1', json=prof_atualizado)
        self.assertEqual(400, resposta.status_code)
        self.assertEqual({'mensagem': 'O novo valor para salário deve ser no mínimo 1400 e não pode ser negativo'}, resposta.json())

    def test_025_id_invalido_nao_inteiro_no_delete(self):
        resposta = requests.delete('http://localhost:5003/professores/1.5')
        self.assertEqual(400, resposta.status_code)
        self.assertEqual({'mensagem': 'ID IVÁLIDO, id precisa ser do tipo inteiro para que eu possa deletar'}, resposta.json())

    def test_026_id_invalido_menor_igual_zero_delete(self):
        resposta = requests.delete('http://localhost:5003/professores/0')
        self.assertEqual(400, resposta.status_code)
        self.assertEqual({'mensagem': 'Valor de ID inválido, ID precisa ser MAIOR QUE ZERO para que eu possa deletar'}, resposta.json())
    
    def test_027_id_nao_encontrado_falha_ao_deletar(self):
        resposta = requests.delete('http://localhost:5003/professores/9999')
        
        self.assertEqual(404, resposta.status_code)
        self.assertEqual({'mensagem': 'id de professor não encontrado, falha ao deletar'}, resposta.json())


         
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

    def test_040_se_caso_id_de_turma_nao_for_inteiro(self):
        turma_atualizada = { 
            "descricao": "7 ano E",
            "ativo": True,
            "professor_id": 4
        }
        resposta = requests.put('http://localhost:5003/turmas/abc', json=turma_atualizada)
        self.assertEqual(400, resposta.status_code)
        self.assertEqual({'mensagem': 'ID de turma informado no end point precisa ser um número inteiro'}, resposta.json())

    def test_041_csdo_id_de_turma_for_menor_igual_a_zero(self):
        turma_atualizada = { 
            "descricao": "7 ano E",
            "ativo": True,
            "professor_id": 4
        }
        resposta = requests.put('http://localhost:5003/turmas/-11', json=turma_atualizada)
        self.assertEqual(400, resposta.status_code)
        self.assertEqual({'mensagem': 'ID de turma precisa ser maior que zero'}, resposta.json())

    def test_042_se_caso_id_de_turma_nao_encontrado(self):
        turma_atualizada = { 
            "descricao": "7 ano E",
            "ativo": True,
            "professor_id": 4
        }

        resposta = requests.put('http://localhost:5003/turmas/777777', json=turma_atualizada)
        self.assertEqual(404, resposta.status_code)
        self.assertEqual({'mensagem': 'Erro, ID de turma não encontrado'}, resposta.json())

    def test_043_se_descricao_de_turma_nao_for_string(self):
        turma_atualizada = { 
            "descricao": 123456,
            "ativo": True,
            "professor_id": 4
        }

        resposta = requests.put('http://localhost:5003/turmas/11', json=turma_atualizada)
        self.assertEqual(400, resposta.status_code)
        self.assertEqual({'mensagem': 'O novo valor para a chave descrição precisa ser uma STRING'}, resposta.json())

    def test_044_caso_professor_id_nao_for_inteiro(self):
        turma_atualizada = { 
            "descricao": "7 ano E",
            "ativo": True,
            "professor_id": "quatro"
        }
        resposta = requests.put('http://localhost:5003/turmas/11', json=turma_atualizada)
        self.assertEqual(400, resposta.status_code)
        self.assertEqual({'mensagem': 'A chave professor_id precisa ser um número inteiro'}, resposta.json())

    def test_045_caso_professor_id_for_menor_que_zero(self):
        turma_atualizada = { 
            "descricao": "7 ano E",
            "ativo": True,
            "professor_id": -1
        }
        resposta = requests.put('http://localhost:5003/turmas/11', json=turma_atualizada)
        self.assertEqual(400, resposta.status_code)
        self.assertEqual({'mensagem': 'A chave professor_id precisa ser maior que zero'}, resposta.json())
    
    def test_046_caso_professor_id_ja_esteja_em_uma_sala(self):
        turma_atualizada = { 
            "descricao": "7 ano E",
            "ativo": True,
            "professor_id": 1
        }
        resposta = requests.put('http://localhost:5003/turmas/12', json=turma_atualizada)
        self.assertEqual(400, resposta.status_code)
        self.assertEqual({'mensagem': 'Erro!!! Cada professor já está sendo responsável por uma sala, e não pode ser responsável por duas, por favor, coloque um professor livre para cuidar dessa sala'}, resposta.json())
    
    def test_047_caso_professor_id_nao_encontrado(self):
        turma_atualizada = { 
            "descricao": "7 ano E",
            "ativo": True,
            "professor_id": 7777777
        }
        resposta = requests.put('http://localhost:5003/turmas/11', json=turma_atualizada)
        self.assertEqual(404, resposta.status_code)
        self.assertEqual({'mensagem': 'Professor Id não encontrado, tente novamente '}, resposta.json())

    def test_048_caso_ativo_esteje_e_nao_for_boolean(self):
        turma_atualizada = { 
            "descricao": "7 ano E",
            "ativo": "Ativada",
            "professor_id": 4 
        }
        resposta = requests.put('http://localhost:5003/turmas/11', json=turma_atualizada)
        self.assertEqual(400, resposta.status_code)
        self.assertEqual({'mensagem': 'O valor para a chave ativo precisa ser do tipo boolean'}, resposta.json())


    def test_049_chaves_invalidas_no_update(self):
        turma_atualizada = {
            "descricao": "7 ano E",
            "ativo": True,
            "professor_id": 4,
            "nota_maxima": 10
        }
        resposta = requests.put('http://localhost:5003/turmas/11', json=turma_atualizada)
        self.assertEqual(400, resposta.status_code)
        self.assertEqual('Chaves adicionais não necessárias, retire-as', resposta.json()['mensagem'])
        self.assertIn('nota_maxima', resposta.json()['chaves_invalidas'])

    def test_050_caso_de_certo_o_put_de_turma(self):
        turma_atualizada = { 
            "descricao": "7 ano E",
            "ativo": True,
            "professor_id": 4 
        }

        resposta = requests.put('http://localhost:5003/turmas/11', json=turma_atualizada)
        self.assertEqual(200, resposta.status_code)
        self.assertEqual({'mensagem': 'Turma atualizada com sucesso'}, resposta.json())

    
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


# -----------------------------------------------ALUNOS---------------------------------------------- #

    def test_054_alunos_retorna_lista(self):
        resposta = requests.get('http://localhost:5003/alunos')

        if resposta.status_code == 404:
            self.fail("voce nao definiu a pagina /alunos no seu server")
        
        try:
            obj_retornado = resposta.json()
       
        except:
            self.fail("queria um json mas voce retornou outra coisa")

        self.assertEqual(type(obj_retornado),type([]))

    def test_055_id_de_aluno_não_int(self):
        resposta = requests.get('http://localhost:5003/alunos/1.5')
        self.assertEqual(400, resposta.status_code)
        self.assertEqual ({'mensagem': 'ID inserido para aluno tem que ser um numero inteiro'}, resposta.json())

    def test_056_id_de_aluno_menor_igual_que_zero(self):
        resposta = requests.get('http://localhost:5003/alunos/-1')
        self.assertEqual(400, resposta.status_code)
        self.assertEqual({'mensagem': 'ID do aluno nao pode ser menor ou igual a que zero'}, resposta.json())


    def test_057_id_de_aluno_inexistente(self):
        resposta = requests.get('http://localhost:5003/alunos/500')

        self.assertEqual(404, resposta.status_code)
        self.assertEqual({'mensagem': 'Aluno(a) nao encontrado(a)/inexistente'}, resposta.json())


    def test_058_se_nome_e_turma_id_nao_forem_inseridos(self):
        novo_aluno = {
            "idade": 13,
            "turma_id": 4,
            "nota_primeiro_semestre": 5
        }

        resposta = requests.post('http://localhost:5003/alunos', json=novo_aluno)
        self.assertEqual({'mensagem': 'Os campos nome, turma_id são OBRIGATÓRIOS'}, resposta.json())

    def test_059_se_turma_id_for_menor_que_zero(self):
        novo_aluno = {
            "nome": "Jose Paulo",
            "idade": 13,
            "turma_id": -1,
        }
        resposta = requests.post('http://localhost:5003/alunos', json=novo_aluno)
        self.assertEqual(400, resposta.status_code)
        self.assertEqual({'mensagem': 'O valor informado para a chave turma_id é INVÁLIDO (não pode ser negativo)'}, resposta.json())
    
    def test_060_se_turma_id_não_existe(self):
        novo_aluno = {
            "nome": "Jose Paulo",
            "idade": 13,
            "turma_id": 10,
        }
        resposta = requests.post('http://localhost:5003/alunos', json=novo_aluno)
        self.assertEqual(404, resposta.status_code)
        self.assertEqual({'mensagem': 'Id de turma não encontrada'}, resposta.json())

    def test_061_se_nome_nao_for_string(self):
        novo_aluno = {
            "nome": 50,
            "idade": 13,
            "turma_id": 11,
            "nota_primeiro_semestre": 5
        }

        resposta = requests.post('http://localhost:5003/alunos', json=novo_aluno)
        self.assertEqual(400, resposta.status_code)
        self.assertEqual({'mensagem': 'Chave nome precisa ser do tipo string'}, resposta.json())


    def test_062_se_turma_id_ou_idade_nao_forem_inteiros(self):
        novo_aluno = {
            "nome": "Jose Paulo",
            "idade": "treze",
            "turma_id": 11
        }
        resposta = requests.post('http://localhost:5003/alunos', json=novo_aluno)
        self.assertEqual(400, resposta.status_code)
        self.assertEqual({'mensagem': 'O valor informado para as chaves idade e turma_id precisam ser INTEIROS'}, resposta.json())

    def test_063_se_idade_for_menor_igual_que_zero(self):
        novo_aluno = {
            "nome": "Jose Paulo",
            "idade": -1,
            "turma_id": 11
        }
        resposta = requests.post('http://localhost:5003/alunos', json=novo_aluno)
        self.assertEqual(400, resposta.status_code)
        self.assertEqual({'mensagem': 'O valor informado na chave idade não pode ser negativo ou igual a zero'}, resposta.json())

    def test_064_se_data_nascimento_nao_for_string(self):
        novo_aluno = {
            "nome": "Jose Paulo",
            "idade": 13,
            "turma_id": 11,
            "data_nascimento": 2
        }
        resposta = requests.post('http://localhost:5003/alunos', json=novo_aluno)
        self.assertEqual(400, resposta.status_code)
        self.assertEqual({'mensagem': 'Data de Nascimento precisa ser uma string dd-mm-aaaa'}, resposta.json())


    def test_065_se_as_notas_do_semestre_um_ou_2_junto_da_media_nao_forem_inteiros_ou_float(self):
        novo_aluno = {
            "nome": "Jose Paulo",
            "idade": 13,
            "turma_id": 11,
            "nota_primeiro_semestre": "oito",
            "nota_segundo_semestre": 10.0,
            "media_final": 9.0
        }

        resposta = requests.post('http://localhost:5003/alunos', json=novo_aluno)
        print(resposta.json())
        self.assertEqual(400, resposta.status_code)
        self.assertEqual({'mensagem': 'Os valores para as notas de primeiro, segundo, semestre, precisao ser do tipo INTEIRO ou FLOAT'}, resposta.json())

    
    def test_066_se_notas_ou_media_inserida_forem_negativas(self):
        novo_aluno = {
            "nome": "Jose Paulo",
            "idade": 13,
            "turma_id": 11,
            "nota_primeiro_semestre": -10,
            "nota_segundo_semestre": 10,
            "media_final": 0
        }
        resposta = requests.post('http://localhost:5003/alunos', json=novo_aluno)
        print(resposta.json())
        self.assertEqual(400, resposta.status_code)
        self.assertEqual({'mensagem' : 'As notas e a media precisam receber um valor inteiro ou float'}, resposta.json())


    def test_067_se_tem_chaves_invalidas(self):
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
        self.assertIn('chaves_invalidas', resposta.json())
        self.assertEqual(400, resposta.status_code)
        self.assertEqual(set(resposta.json()['chaves_invalidas']), {'nome_do_responsavel', 'endereço'})
        
    def test_068_se_id_do_put_nao_for_inteiro(self):
        aluno_atualizado = {
            "nome": "Wender da Silva Santos Atualizado", 
            "idade": 12, 
            "turma_id": 12, 
            "data_nascimento": "07-08-2012", 
            "nota_primeiro_semestre": 9.5, 
            "nota_segundo_semestre": 9.0, 
            "media_final": 9.25
        }

        resposta = requests.put('http://localhost:5003/alunos/centoequatro', json=aluno_atualizado)
        self.assertEqual(400, resposta.status_code)
        self.assertEqual({'mensagem': 'ID de aluno informado no end point precisa ser um número inteiro'}, resposta.json())

    def test_069_se_id_do_put_for_menor_igual_a_zero(self):
        aluno_atualizado = {
            "nome": "Wender da Silva Santos Atualizado", 
            "idade": 12, 
            "turma_id": 12, 
            "data_nascimento": "07-08-2012", 
            "nota_primeiro_semestre": 9.5, 
            "nota_segundo_semestre": 9.0,
            "media_final": 9.25
        }

        resposta = requests.put('http://localhost:5003/alunos/-1', json=aluno_atualizado)
        self.assertEqual(400, resposta.status_code)
        self.assertEqual({'mensagem': 'ID de aluno precisa ser maior que zero'}, resposta.json())
        
    
    def test_070_se_chaves_invalidas(self):
        aluno_atualizado = {
            "nome": "Wender da Silva Santos Atualizado", 
            "idade": 12, 
            "turma_id": 12, 
            "data_nascimento": "07-08-2012", 
            "nota_primeiro_semestre": 9.5, 
            "nota_segundo_semestre": 9.0,
            "media_final": 9.25,
            "nome_do_responsavel": "Jose Elis dos Santos",
            "endereço": "Casa minha, vida nossa 1930"
        }

        resposta = requests.put('http://localhost:5003/alunos/105', json=aluno_atualizado)
        self.assertIn('chaves_invalidas', resposta.json())
        self.assertEqual(400, resposta.status_code)
        self.assertEqual(set(resposta.json()['chaves_invalidas']), {'nome_do_responsavel', 'endereço'})
        
    def test_071_se_nome_esta_vazio_ou_nao_e_uma_string(self):
        aluno_atualizado = {
            "nome": "", 
            "idade": 12, 
            "turma_id": 12, 
            "data_nascimento": "07-08-2012", 
            "nota_primeiro_semestre": 9.5, 
            "nota_segundo_semestre": 9.0,
            "media_final": 9.25
        }

        resposta = requests.put('http://localhost:5003/alunos/105', json=aluno_atualizado)
        self.assertEqual(400, resposta.status_code)
        self.assertEqual({'mensagem': 'O valor para a chave aluno precisa ser uma string e não pode estar vazia'}, resposta.json())
        
    def test_072_se_turma_id_nao_for_inteiro(self):
        aluno_atualizado = {
            "nome": "Wender da Silva Santos Atualizado", 
            "idade": 12, 
            "turma_id": "doze", 
            "data_nascimento": "07-08-2012", 
            "nota_primeiro_semestre": 9.5, 
            "nota_segundo_semestre": 9.0,
            "media_final": 9.25
        }

        resposta = requests.put('http://localhost:5003/alunos/105', json=aluno_atualizado)
        self.assertEqual(400, resposta.status_code)
        self.assertEqual({'mensagem': 'A chave turma_id precisa ser um número inteiro'}, resposta.json())

    def test_073_se_turma_id_for_menor_igual_a_zero(self):
        aluno_atualizado = {
            "nome": "Wender da Silva Santos Atualizado", 
            "idade": 12, 
            "turma_id": -12, 
            "data_nascimento": "07-08-2012", 
            "nota_primeiro_semestre": 9.5, 
            "nota_segundo_semestre": 9.0,
            "media_final": 9.25
        }

        resposta = requests.put('http://localhost:5003/alunos/105', json=aluno_atualizado)
        self.assertEqual(400, resposta.status_code)
        self.assertEqual({'mensagem': 'A chave turma_id precisa ser maior que zero'}, resposta.json())
        
    def test_074_caso_id_de_turma_nao_for_encontrada(self):
        
        aluno_atualizado = {
            "nome": "Wender da Silva Santos Atualizado", 
            "idade": 12, 
            "turma_id": 7777777, 
            "data_nascimento": "07-08-2012", 
            "nota_primeiro_semestre": 9.5, 
            "nota_segundo_semestre": 9.0,
            "media_final": 9.25
        }

        resposta = requests.put('http://localhost:5003/alunos/105', json=aluno_atualizado)
        self.assertEqual(404, resposta.status_code)
        self.assertEqual({'mensagem': 'Id de turma não encontrado'}, resposta.json())
        
    def test_074_caso_data_de_nascimento_nao_for_string_ou_esteje_vazia(self):
        aluno_atualizado = {
            "nome": "Wender da Silva Santos Atualizado", 
            "idade": 12, 
            "turma_id": 12, 
            "data_nascimento": "", 
            "nota_primeiro_semestre": 9.5, 
            "nota_segundo_semestre": 9.0,
            "media_final": 9.25
        }

        resposta = requests.put('http://localhost:5003/alunos/105', json=aluno_atualizado)
        self.assertEqual(400, resposta.status_code)
        self.assertEqual({'mensagem': 'A chave data_nascimento precisa ser uma string e não pode estar vazia!!'}, resposta.json())
        
    def test_075_caso_idade_de_aluno_nao_for_um_numero_inteiro(self):
        aluno_atualizado = {
            "nome": "Wender da Silva Santos Atualizado", 
            "idade": "doze", 
            "turma_id": 12, 
            "data_nascimento": "07-08-2012", 
            "nota_primeiro_semestre": 9.5, 
            "nota_segundo_semestre": 9.0,
            "media_final": 9.25
        }

        resposta = requests.put('http://localhost:5003/alunos/105', json=aluno_atualizado)
        self.assertEqual(400, resposta.status_code)
        self.assertEqual({'mensagem': 'O valor informado para a chave idade precisa ser um número inteiro INTEIRO'}, resposta.json())
        
        
    def test_076_caso_idade_de_aluno_nao_for_um_numero_maior_que_zero(self):
        aluno_atualizado = {
            "nome": "Wender da Silva Santos Atualizado", 
            "idade": -12, 
            "turma_id": 12, 
            "data_nascimento": "07-08-2012", 
            "nota_primeiro_semestre": 9.5, 
            "nota_segundo_semestre": 9.0,
            "media_final": 9.25
        }

        resposta = requests.put('http://localhost:5003/alunos/105', json=aluno_atualizado)
        self.assertEqual(400, resposta.status_code)
        self.assertEqual({'mensagem': 'O valor informado na chave idade não pode ser negativo ou igual a zero'}, resposta.json())

    def test_077_caso_notas_primeiro_ou_segundo_semestre_ou_media_final_nao_forem_do_tipo_float(self):
        aluno_atualizado = {
            "nome": "Wender da Silva Santos Atualizado", 
            "idade": 12, 
            "turma_id": 12, 
            "data_nascimento": "07-08-2012", 
            "nota_primeiro_semestre": "nove e meio", 
            "nota_segundo_semestre": 9.0,
            "media_final": 9.25
        }     

        resposta = requests.put('http://localhost:5003/alunos/105', json=aluno_atualizado)
        self.assertEqual(400, resposta.status_code)
        self.assertEqual({'mensagem': 'O novo valor para as chaves das notas primeiro, segundo semestre e média_final precisam ser do tipo float'}, resposta.json())

    def test_078_caso_notas_primeiro_ou_segundo_semestre_ou_media_final_forem_menor_que_zero(self):
        aluno_atualizado = {
            "nome": "Wender da Silva Santos Atualizado", 
            "idade": 12, 
            "turma_id": 12, 
            "data_nascimento": "07-08-2012", 
            "nota_primeiro_semestre": -9.5, 
            "nota_segundo_semestre": 9.0,
            "media_final": 9.25
        }     

        resposta = requests.put('http://localhost:5003/alunos/105', json=aluno_atualizado)
        self.assertEqual(400, resposta.status_code)
        self.assertEqual({'mensagem': 'O novo valor para as chaves das notas primeiro, segundo semestre e média_final precisam não podem ser números negativos'}, resposta.json())
        
    def test_079_caso_notas_primeiro_ou_segundo_semestre_ou_media_final_forem_maiores_que_zero(self):
        aluno_atualizado = {
            "nome": "Wender da Silva Santos Atualizado", 
            "idade": 12, 
            "turma_id": 12, 
            "data_nascimento": "07-08-2012", 
            "nota_primeiro_semestre": 11, 
            "nota_segundo_semestre": 9.0,
            "media_final": 9.25
        }     

        resposta = requests.put('http://localhost:5003/alunos/105', json=aluno_atualizado)
        self.assertEqual(400, resposta.status_code)
        self.assertEqual({'mensagem': 'O novo valor para as chaves das notas primeiro, segundo semestre e média_final precisam não podem ser maiores que 10'}, resposta.json())

    def test_071_id_invalido_nao_inteiro_no_delete(self):
        resposta = requests.delete('http://localhost:5003/alunos/1.5')
        self.assertEqual(400, resposta.status_code)
        self.assertEqual({'mensagem': 'ID de aluno(a) inválido. O ID precisa ser um número inteiro para que o(a) aluno(a) possa ser deletado(a) com sucesso.'}, resposta.json())

    def test_072_id_invalido_menor_igual_zero_delete(self):
        resposta = requests.delete('http://localhost:5003/alunos/0')
        self.assertEqual(400, resposta.status_code)
        self.assertEqual({'mensagem': 'ID de aluno(a) inválido. O ID precisa ser maior que zero para que o(a) aluno(a) possa ser deletado(a) com sucesso.'}, resposta.json())
    
    def test_073_id_nao_encontrado_falha_ao_deletar(self):
        resposta = requests.delete('http://localhost:5003/alunos/9999')
        self.assertEqual(404, resposta.status_code)
        self.assertEqual({'mensagem': 'ID de aluno(a) não encontrado(a), falha ao deletar'}, resposta.json())
