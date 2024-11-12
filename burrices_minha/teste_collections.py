from collections import namedtuple
from typing import NamedTuple # Meta classe

class Pessoa(NamedTuple):
    nome: str = "Nome Padrão"
    sobrenome: str = "Sobrenome Padrão"
    idade: int = 38

#Pessoa = namedtuple(
#    "Pessoa", ["nome", "sobrenome", "idade"],
#    defaults=["Nome Padrão", "Sobrenome Padrão", 38]
#)

pessoa_1 = Pessoa("Yuri", "Saporito")
pessoa_2 = Pessoa("Carlos", "Ivan", 1000)
pessoa_3 = Pessoa()
pessoa_4 = Pessoa("Yuri", "Saporito")
print(pessoa_1.nome)
print(pessoa_1.sobrenome)
print(pessoa_1.idade)

print(pessoa_1)
print(pessoa_2)
print(pessoa_3)
print(pessoa_1 == pessoa_4) # Tupla é imutável, logo ele compara espaço da memória, espaço por espaço