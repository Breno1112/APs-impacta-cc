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


#teste
