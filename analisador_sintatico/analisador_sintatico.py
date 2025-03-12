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


    def analisar(self):
        self.pegar_proximo_atomo()
        while self.atomo_atual is not None:
            if self.atomo_atual.get('error') is not None:
                raise RuntimeError(self.atomo_atual['error'])
            self.verificar_e_direcionar_atomo()
            self.pegar_proximo_atomo()
        print('{} linhas analisadas, programa sintaticamente correto.'.format(self.analisador_lexico.last_line()))
    
    def imprime_atomo_atual(self):
        print('Linha: {} - Atomo: {}    lexema: {}'.format(self.atomo_atual['linha'], self.atomo_atual['atomo'], self.atomo_atual['lexema']))
    
    def verificar_e_direcionar_atomo(self):
        if self.atomo_atual['atomo'] == 'PROGRAM':
            self.analisar_palavra_reservada_program()
        else:
            self.imprime_atomo_atual()
    
    def pegar_proximo_atomo(self):
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
        self.imprime_atomo_atual()
        self.quantidade_programs += 1
        self.verificar_e_direcionar_e_validar_proximo_atomo('IDENTIF')
        # Agora preciso validar se após o primeiro identificador nós temos parênteses e mais identificadores
        # pega o próximo átomo
        # se for parênteses aberto
        # enquanto não chegar no parênteses fechado, 
        # garantir que o átomo seguinte é IDENTIF
        # pegar o próximo
        # se o próximo não for PARENTESES_FECHADO
        # garantir que é virgula
        # pegar o próximo
        self.pegar_proximo_atomo()
        if self.atomo_atual['atomo'] == 'PARENTESES_ABERTO':
            self.imprime_atomo_atual()
            while self.atomo_atual['atomo'] != 'PARENTESES_FECHADO':
                self.verificar_e_direcionar_e_validar_proximo_atomo('IDENTIF')
                self.pegar_proximo_atomo()
                if self.atomo_atual['atomo'] != 'VIRGULA':
                    self.garantir_atomo_atual_especifico('PARENTESES_FECHADO')
            self.imprime_atomo_atual()
            self.pegar_proximo_atomo()
        self.garantir_atomo_atual_especifico('PONTO_VIRG')
        
