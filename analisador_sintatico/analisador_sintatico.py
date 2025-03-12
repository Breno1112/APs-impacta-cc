from analisador_lexico import analisador_lexico

class AnalisadorSintatico:

    def __init__(self, caminho_arquivo):
        self.caminho_arquivo = caminho_arquivo
        arquivo = open(self.caminho_arquivo, 'r')
        self.analisador_lexico = analisador_lexico.AnalisadorLexico(arquivo.read())
        arquivo.close()

        self.quantidade_begins = 0
        self.quantidade_ends = 0
        self.quantidade_programs = 0
        self.atomo_atual = None
        self.penultimo_atomo = None
        self.tipos = ('INTEGER', 'BOOLEAN')


    def analisar(self):
        self.pegar_proximo_atomo()
        self.garantir_atomo_atual_especifico('PROGRAM')
        self.analisar_palavra_reservada_program()
        self.pegar_proximo_atomo()
        if self.atomo_atual['atomo'] == 'VAR':
            self.analisar_declaracao_variaveis()
        self.analisar_comando_composto()
        # while self.atomo_atual is not None:
        #     self.imprime_atomo_atual()
        #     self.pegar_proximo_atomo()
        print('{} linhas analisadas, programa sintaticamente correto.'.format(self.analisador_lexico.last_line()))
    
    def imprime_atomo_atual(self):
        print('Linha: {} - Atomo: {}    lexema: {}'.format(self.atomo_atual['linha'], self.atomo_atual['atomo'], self.atomo_atual['lexema']))
    
    def pegar_proximo_atomo(self):
        self.penultimo_atomo = self.atomo_atual
        self.atomo_atual = self.analisador_lexico.proximo_atomo()

    def verificar_e_direcionar_e_validar_proximo_atomo(self, proximo_atomo_esperado):
        self.pegar_proximo_atomo()
        if self.atomo_atual['atomo'] != proximo_atomo_esperado:
            raise RuntimeError('Erro sintático: Esperado [{}] encontrado [{}] na linha {}'.format(proximo_atomo_esperado, self.atomo_atual['atomo'], self.atomo_atual['linha']))
        self.imprime_atomo_atual()

    def garantir_atomo_atual_especifico(self, atomo_esperado):
        if self.atomo_atual['atomo'] != atomo_esperado:
            raise RuntimeError('Erro sintático: Esperado [{}] encontrado [{}] na linha {}'.format(atomo_esperado, self.atomo_atual['atomo'], self.atomo_atual['linha']))
        self.imprime_atomo_atual()

    def analisar_palavra_reservada_program(self):
        if self.quantidade_programs > 0:
            raise RuntimeError('Erro sintático: Encontrado [{}] na linha {}. O programa só pode ter um identificador'.format(self.atomo_atual['atomo'], self.atomo_atual['linha']))
        self.quantidade_programs += 1
        self.verificar_e_direcionar_e_validar_proximo_atomo('IDENTIF')
        self.pegar_proximo_atomo()

        if self.atomo_atual['atomo'] == 'PARENTESES_ABERTO':
            self.imprime_atomo_atual()
            self.pegar_proximo_atomo()
            self.validar_lista_identificadores()
            self.garantir_atomo_atual_especifico('PARENTESES_FECHADO')
            self.pegar_proximo_atomo()
        self.garantir_atomo_atual_especifico('PONTO_VIRG')


    def validar_lista_identificadores(self):
        while self.atomo_atual['atomo'] in ('IDENTIF', 'VIRGULA'):
            self.imprime_atomo_atual()
            self.pegar_proximo_atomo()
        if self.penultimo_atomo['atomo'] == 'VIRGULA':
            self.garantir_atomo_atual_especifico('IDENTIF')
    
    def analisar_declaracao_variaveis(self):
        self.garantir_atomo_atual_especifico('VAR')
        self.pegar_proximo_atomo()
        continuar = True
        while continuar:
            self.analisar_declaracao()
            self.verificar_e_direcionar_e_validar_proximo_atomo('PONTO_VIRG')
            self.pegar_proximo_atomo()
            continuar = self.atomo_atual['atomo'] == 'IDENTIF'

    
    def analisar_declaracao(self):
        self.validar_lista_identificadores()
        self.garantir_atomo_atual_especifico('DOIS_PONTOS')
        self.garantir_tipo()


    def garantir_tipo(self):
        self.pegar_proximo_atomo()
        if self.atomo_atual['atomo'] not in self.tipos:
            raise RuntimeError('Erro sintático: Esperado [INTEGER] ou [BOOLEAN] encontrado [{}] na linha {}'.format(self.atomo_atual['atomo'], self.atomo_atual['linha']))
        self.imprime_atomo_atual()

    def analisar_comando(self):
        if self.atomo_atual['atomo'] == 'IDENTIF':
            self.imprime_atomo_atual()
            self.pegar_proximo_atomo()
            if self.atomo_atual['atomo'] == 'ATRIB':
                self.imprime_atomo_atual()
                self.analisar_expressao()
        elif self.atomo_atual['atomo'] == 'IF':
            self.analisar_comando_if()
        elif self.atomo_atual['atomo'] == 'READ':
            self.analisar_comando_de_entrada()
            


    def analisar_comando_de_entrada(self):
        self.garantir_atomo_atual_especifico('READ')
        self.verificar_e_direcionar_e_validar_proximo_atomo('PARENTESES_ABERTO')
        self.pegar_proximo_atomo()
        self.validar_lista_identificadores()
        self.garantir_atomo_atual_especifico('PARENTESES_FECHADO')

    def analisar_comando_de_saida(self):
        pass

    def analisar_comando_if(self):
        self.garantir_atomo_atual_especifico('IF')
        self.pegar_proximo_atomo()
        self.analisar_expressao()
        self.garantir_atomo_atual_especifico('THEN')
        self.pegar_proximo_atomo()
        self.analisar_comando()
        if self.atomo_atual['atomo'] == 'ELSE':
            self.garantir_atomo_atual_especifico('THEN')
            self.pegar_proximo_atomo()
            self.analisar_comando()


    def analisar_comando_while(self):
        pass

    def analisar_comando_composto(self):
        self.garantir_atomo_atual_especifico('BEGIN')
        self.pegar_proximo_atomo()
        self.analisar_comando()
        self.pegar_proximo_atomo()
        while self.atomo_atual['atomo'] == 'PONTO_VIRG':
            self.garantir_atomo_atual_especifico('PONTO_VIRG')
            self.pegar_proximo_atomo()
            self.analisar_comando()
            self.pegar_proximo_atomo()
        self.garantir_atomo_atual_especifico('END')
        pass

    def analisar_expressao(self):
        self.analisar_expressao_simples()

    def analisar_operador_relacional(self):
        if self.atomo_atual['atomo'] not in ('MENOR_QUE', 'MENOR_IGUAL', 'IGUAL', 'DIFERENTE_DE', 'MAIOR_QUE', 'MAIOR_IGUAL'):
            raise RuntimeError('Erro sintático: Esperado [MENOR_QUE] ou [MENOR_IGUAL] ou [IGUAL] ou [DIFERENTE_DE] ou [MAIOR_QUE] ou [MAIOR_IGUAL] encontrado [{}] na linha {}'.format(self.atomo_atual['atomo'], self.atomo_atual['linha']))
        self.imprime_atomo_atual()

    def analisar_operador_adicao(self):
        if not self.is_operador_adicao():
            raise RuntimeError('Erro sintático: Esperado [ADICAO] ou [SUBTRACAO] ou [OR] encontrado [{}] na linha {}'.format(self.atomo_atual['atomo'], self.atomo_atual['linha']))
        self.imprime_atomo_atual()
    
    def is_operador_adicao(self):
        return self.atomo_atual['atomo'] in ('ADICAO', 'SUBTRACAO', 'OR')

    def analisar_expressao_simples(self):
        if self.atomo_atual['atomo'] in ('SOMA', 'SUBTRACAO'):
            self.imprime_atomo_atual()
            self.pegar_proximo_atomo()
        self.analisar_termo()
        while self.is_operador_adicao():
            self.analisar_operador_adicao()
            self.analisar_termo()

    def analisar_termo(self):
        self.analisar_fator()
        while self.is_operador_multiplicacao():
            self.analisar_operador_multiplicacao()
            self.pegar_proximo_atomo()
            self.analisar_fator()

    def is_operador_multiplicacao(self):
        return self.atomo_atual['atomo'] in ('MULTIPLICACAO', 'DIVISAO', 'DIV', 'MOD', 'AND')

    def analisar_operador_multiplicacao(self):
        if not self.is_operador_multiplicacao():
            raise RuntimeError('Erro sintático: Esperado [MULTIPLICACAO] ou [DIVISAO] ou [DIV] ou [MOD] ou [AND] encontrado [{}] na linha {}'.format(self.atomo_atual['atomo'], self.atomo_atual['linha']))
        self.imprime_atomo_atual()

    def analisar_fator(self):
        pass

        
