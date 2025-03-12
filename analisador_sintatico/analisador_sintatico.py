from analisador_lexico import analisador_lexico

class AnalisadorSintatico:

    def __init__(self, caminho_arquivo):
        self.caminho_arquivo = caminho_arquivo
        arquivo = open(self.caminho_arquivo, 'r')
        self.analisador_lexico = analisador_lexico.AnalisadorLexico(arquivo.read())
        arquivo.close()

    def analisar(self):
        atomo = self.analisador_lexico.proximo_atomo()
        while atomo is not None:
            if atomo.get('error') is not None:
                raise RuntimeError(atomo['error'])
            print('Linha: {} - Atomo: {}    lexema: {}'.format(atomo['linha'], atomo['atomo'], atomo['lexema']))
            atomo = self.analisador_lexico.proximo_atomo()
        print('{} linhas analisadas, programa sintaticamente correto.'.format(self.analisador_lexico.last_line()))


    def begin_end(self):
    #Validar Tokens
    #A função analisar consome todos os atomos antes de begin_end ser chamada, deixando o analisador léxico sem mais atomos para processar.
        begin_count = 0
        end_count = 0
        atomo = self.analisador_lexico.proximo_atomo()
        while atomo is not None:
            if atomo['atomo'] == 'begin':
                begin_count += 1
            elif atomo['atomo'] == 'end':
                end_count += 1
            atomo = self.analisador_lexico.proximo_atomo()
        if begin_count != end_count:
            raise RuntimeError('Erro sintático: quantidade de begin e end diferentes.')
