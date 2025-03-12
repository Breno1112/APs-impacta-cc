class AnalisadorLexico:
    def __init__(self, codigo_fonte):
        self.codigo_fonte = codigo_fonte
        self.linha = 0
        self.pos = 0
        self.limitadores = (' ', '\n', '\t', '\r')
        self.palavras_reservadas = ('begin', 'boolean', 'div', 'do', 'else', 'end', 'false', 'if', 'integer', 'mod', 'program', 'read', 'then', 'true', 'not', 'var', 'while', 'write', 'or', 'div', 'mod', 'and')

    def imprime_codigo_fonte(self):
        print(self.codigo_fonte)

    def proximo_char(self):
        lendo_comentario_linha = self.verifica_comentario_linha()
        lendo_comentario_bloco_tipo_a = self.verifica_comentario_tipo_a() # comentarios com {}
        lendo_comentario_bloco_tipo_b = self.verifica_comentario_tipo_b() # comentarios com (*
        while lendo_comentario_linha or lendo_comentario_bloco_tipo_a or lendo_comentario_bloco_tipo_b:
            if lendo_comentario_linha:
                self.pula_comentario_linha()
            if lendo_comentario_bloco_tipo_a:
                self.pula_comentario_tipo_a()
            if lendo_comentario_bloco_tipo_b:
                self.pula_comentario_tipo_b()
            lendo_comentario_linha = self.verifica_comentario_linha()
            lendo_comentario_bloco_tipo_a = self.verifica_comentario_tipo_a() # comentarios com {}
            lendo_comentario_bloco_tipo_b = self.verifica_comentario_tipo_b() # comentarios com (*
        if self.pos >= len(self.codigo_fonte):
            return None
        c = self.codigo_fonte[self.pos]
        self.pos += 1
        return c

    def verifica_comentario_linha(self):
        if self.pos >= len(self.codigo_fonte) -1:
            return False
        c = self.codigo_fonte[self.pos]
        carry = c + self.codigo_fonte[self.pos + 1]
        return carry == '//'

    def pula_comentario_linha(self):
        c = self.codigo_fonte[self.pos]
        while c != '\n':
            self.pos += 1
            c = self.codigo_fonte[self.pos]
        self.pos += 1
        self.linha += 1
    
    def verifica_comentario_tipo_a(self):
        if self.pos >= len(self.codigo_fonte) -1:
            return False
        c = self.codigo_fonte[self.pos]
        return c == '{'
    
    def pula_comentario_tipo_a(self):
        c = self.codigo_fonte[self.pos]
        while c != '}':
            if c == '\n':
                self.linha += 1
            self.pos += 1
            c = self.codigo_fonte[self.pos]
        self.pos += 1
    
    def verifica_comentario_tipo_b(self):
        if self.pos >= len(self.codigo_fonte) -1:
            return False
        c = self.codigo_fonte[self.pos]
        carry = c + self.codigo_fonte[self.pos + 1]
        return carry == '(*'
    
    def pula_comentario_tipo_b(self):
        c = self.codigo_fonte[self.pos]
        carry = c
        while carry != "*)":
            if c == '\n':
                self.linha += 1
            if self.pos <= len(self.codigo_fonte) - 2:
                carry = c + self.codigo_fonte[self.pos + 1]
            self.pos += 1
            c = self.codigo_fonte[self.pos]
        self.pos += 1

    def retrair(self):
        self.pos -= 1
        if self.pos < 0:
            self.pos = 0
        c = self.codigo_fonte[self.pos]
        if c == '\n':
            self.linha -= 1
    
    def verifica_identificadores(self):
        c = self.proximo_char()
        if c == '\n':
            self.linha += 1
        carry = ""
        continuar = c is not None and (c.isalpha() or c == '_') # na primeira posição do identificador é apenas letra ou underline
        while continuar:
            carry += c
            c = self.proximo_char()
            if c == '\n':
                self.linha += 1
            continuar = c is not None and (c.isalpha() or c.isnumeric() or c == '_') # se o tamanho do identificador for maior que 20, retornar erro
        if carry == "":
            return None
        if c is not None:
            self.retrair()
        return carry
    

    def verifica_palavras_reservadas(self, atomo):
        if atomo in self.palavras_reservadas:
            return atomo.upper()
        return None
    
    def tratar_excecao(self, atomo):
        # if atomo == ':':
        #     return {'linha': self.linha + 1, 'atomo': 'DOIS_PONTOS', 'lexema': atomo}
        if atomo == ':=':
            return {'linha': self.linha + 1, 'atomo': 'ATRIB', 'lexema': atomo}
        # elif atomo == ',':
        #     return {'linha': self.linha + 1, 'atomo': 'VIRGULA', 'lexema': atomo}
        elif atomo == '<':
            return {'linha': self.linha + 1, 'atomo': 'MENOR_QUE', 'lexema': atomo}
        elif atomo == '<=':
            return {'linha': self.linha + 1, 'atomo': 'MENOR_IGUAL', 'lexema': atomo}
        elif atomo == '==':
            return {'linha': self.linha + 1, 'atomo': 'COMPARACAO', 'lexema': atomo}
        elif atomo == '>':
            return {'linha': self.linha + 1, 'atomo': 'MAIOR_QUE', 'lexema': atomo}
        elif atomo == '>=':
            return {'linha': self.linha + 1, 'atomo': 'MAIOR_IGUAL', 'lexema': atomo}
        elif atomo == '<>':
            return {'linha': self.linha + 1, 'atomo': 'DIFERENTE_DE', 'lexema': atomo}
        elif atomo == '+' or atomo == 'or':
            return {'linha': self.linha + 1, 'atomo': 'SOMA', 'lexema': atomo}
        elif atomo == '-':
            return {'linha': self.linha + 1, 'atomo': 'SUBTRACAO', 'lexema': atomo}
        elif atomo == '/':
            return {'linha': self.linha + 1, 'atomo': 'DIVISAO', 'lexema': atomo}
        elif atomo == '*':
            return {'linha': self.linha + 1, 'atomo': 'MULTIPLICACAO', 'lexema': atomo}
        elif atomo == '|':
            return {'linha': self.linha + 1, 'atomo': 'MODULO', 'lexema': atomo}
        return None
    
    def tratar_numeros(self, atomo):
        if atomo.isnumeric():
            return {'linha': self.linha + 1, 'atomo': 'NUM', 'lexema': atomo}
        
    def tratar_caracter_especial(self, c):
        if c == '(':
            return {'linha': self.linha + 1, 'atomo': 'PARENTESES_ABERTO', 'lexema': c}
        elif c == ')':
            return {'linha': self.linha + 1, 'atomo': 'PARENTESES_FECHADO', 'lexema': c}
        elif c == ';':
            return {'linha': self.linha + 1, 'atomo': 'PONTO_VIRG', 'lexema': c}
        elif c == ',':
            return {'linha': self.linha + 1, 'atomo': 'VIRGULA', 'lexema': c}
        elif c == ':':
            if self.pos <= len(self.codigo_fonte) - 1 and self.codigo_fonte[self.pos] != '=':
                    return {'linha': self.linha + 1, 'atomo': 'DOIS_PONTOS', 'lexema': c}
        elif c == '=':
            return {'linha': self.linha + 1, 'atomo': 'IGUAL', 'lexema': c}
        return None

    def proximo_atomo(self):
        atomo = None
        c = self.proximo_char()
        if c is None:
            return None
        if c == '\n':
            self.linha += 1

        while atomo is None and c in self.limitadores:
            c = self.proximo_char()
            if c == '\n':
                self.linha += 1
        self.retrair()
        atomo_identificador = self.verifica_identificadores()
        if atomo_identificador is not None:
            if len(atomo_identificador) > 20:
                return {'error': 'Erro sintático na linha {}: Tamanho do identificador não pode ser maior que 20 caracteres'.format(self.linha)}
            palavra_reservada = self.verifica_palavras_reservadas(atomo_identificador)
            if palavra_reservada is not None:
                return {'linha': self.linha + 1, 'atomo': palavra_reservada, 'lexema': atomo_identificador}
            return {'linha': self.linha + 1, 'atomo': 'IDENTIF', 'lexema': atomo_identificador}
        # Verificar por identificadores
        # Verificar por palavras reservadas
        # Verificar por números
        caracter_especial_tratado = self.tratar_caracter_especial(c)
        if caracter_especial_tratado is not None:
            return caracter_especial_tratado
        continuar = c is not None and c not in self.limitadores
        while continuar:
            if atomo is None:
                atomo = c
            else:
                atomo += c
            c = self.proximo_char()
            if c == '\n':
                self.linha += 1
            continuar = c is not None and c not in self.limitadores
        atomo_numerico = self.tratar_numeros(atomo)
        if atomo_numerico is not None:
            return atomo_numerico
        excecao_tratada = self.tratar_excecao(atomo)
        if excecao_tratada is not None:
            return excecao_tratada
        return {'linha': self.linha + 1, 'atomo': 'NAO_ENCONTRADO', 'lexema': atomo}
                
    def last_line(self):
        return self.linha + 1
