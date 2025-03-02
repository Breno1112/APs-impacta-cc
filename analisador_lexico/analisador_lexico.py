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

    def monta_atomo(self, text):
        return {
            "lexama": text
        }
    
    def retrair(self):
        c = self.codigo_fonte[self.pos]
        if c == '\n':
            self.linha -= 1
        self.pos -= 1

    def proximo_atomo(self):
        was_using_alpha = False
        was_using_numeric = False
        c = self.proximo_char()
        if c is None:
            return None
        while c not in self.limitadores and c is not None:
            if c.isalpha():
                was_using_alpha = True
            elif c.isnumeric():
                was_using_numeric = True
            if (not c.isalpha() and not c.isnumeric()) and (was_using_alpha or was_using_numeric):
                self.retrair()
                c = None
            else:
                self.carry += c
                c = self.proximo_char()
        temp = self.carry
        self.carry = ""
        return temp

