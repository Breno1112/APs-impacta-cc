from analisador_lexico import analisador_lexico

arquivo = open('programa.plite', 'r')
lex = analisador_lexico.AnalisadorLexico(arquivo.read())
arquivo.close()

lex.imprime_codigo_fonte()
atomo = lex.proximo_atomo()
while atomo is not None:
    print(f'Atomo: {atomo}')
    atomo = lex.proximo_atomo()
print('fim do arquivo')