
def aaaa(cls):
    original_init = cls.__init__
    def new_init(self, *args, **kwargs):
        original_init(self, *args, **kwargs)
        def new_method(self):
            return f"Olha estou aqui {self.name}"
        self.new_method = new_method.__get__(self)
    cls.__init__ = new_init
    return cls


@aaaa
class MinhaClasse:
    def __init__(self, nome):
        self.name = nome

# Testando o método específico da instância
obj = MinhaClasse("Objeto 1")
print(obj.new_method())

# Elabore a Classe Pessoa, com os atributos nome, sobrenome e idade. 
# Elabore os métodos str, repr e eq.