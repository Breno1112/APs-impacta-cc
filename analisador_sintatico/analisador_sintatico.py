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


    def analisar(self):
        self.pegar_proximo_atomo()
        self.garantir_atomo_atual_especifico('PROGRAM')
        self.analisar_palavra_reservada_program()
        self.pegar_proximo_atomo()
        if self.atomo_atual['atomo'] == 'VAR':
            self.analisar_declaracao_variaveis()
            self.pegar_proximo_atomo()
        self.garantir_atomo_atual_especifico('BEGIN')
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
            self.validar_lista_identificadores()
            self.garantir_atomo_atual_especifico('PARENTESES_FECHADO')
            self.pegar_proximo_atomo()
        self.garantir_atomo_atual_especifico('PONTO_VIRG')


    def validar_lista_identificadores(self):
        self.pegar_proximo_atomo()
        while self.atomo_atual['atomo'] in ('IDENTIF', 'VIRGULA'):
            self.imprime_atomo_atual()
            self.pegar_proximo_atomo()
        if self.penultimo_atomo['atomo'] == 'VIRGULA':
            self.garantir_atomo_atual_especifico('IDENTIF')
    
    def analisar_declaracao_variaveis(self):
        self.garantir_atomo_atual_especifico('VAR')
        self.validar_lista_identificadores()

        
