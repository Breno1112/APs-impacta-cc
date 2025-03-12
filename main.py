from analisador_lexico import analisador_lexico

arquivo = open('programa.plite', 'r')
lex = analisador_lexico.AnalisadorLexico(arquivo.read())
arquivo.close()


atomo = lex.proximo_atomo()
while atomo is not None:
    print('Atomo: {}    lexema: {}'.format(atomo['atomo'], atomo['lexema']))
    atomo = lex.proximo_atomo()
print('fim do arquivo')