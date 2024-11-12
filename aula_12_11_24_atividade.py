class Pessoa():
    def __init__(self, nome, sobrenome, idade):
        self.nome = nome
        self.sobrenome = sobrenome
        self.idade = idade

    def __str__(self):
        return f"{self.name} {self.sobrenome} {self.idade}"

    def __repr__(self):
        return 

    def __eq__(self):
        return