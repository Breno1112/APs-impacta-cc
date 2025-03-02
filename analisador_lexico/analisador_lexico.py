class AnalisadorLexico:
    def __init__(self, codigo_fonte):
        self.codigo_fonte = codigo_fonte
        self.linha = 0
        self.pos = 0
        self.carry = ""
        self.limitadores = (' ', '\n', '\t', '\r')
    
    def imprime_codigo_fonte(self):
        print(self.codigo_fonte)

    def proximo_char(self):
        if self.pos >= len(self.codigo_fonte):
            return None
        c = self.codigo_fonte[self.pos]
        self.pos += 1
        if c == '\n':
            self.linha += 1
        return c

    def get_linha(self):
        return self.linha + 1

    def get_coluna(self):
        return self.pos_visual + 1

    def monta_atomo(self, text):
        return {
            "lexama": text
        }
    
    def retrair(self):
        self.pos -= 1

    def proximo_atomo(self):
        c = self.proximo_char()
        if c is None:
            return None
        while c not in self.limitadores and c is not None:
            print(c.isalpha() or c.isnumeric())
            self.carry += c
            c = self.proximo_char()
        temp = self.carry
        self.carry = ""
        return temp

