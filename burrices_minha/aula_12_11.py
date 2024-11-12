from dataclasses import dataclass, asdict, astuple, field, fields

@dataclass #(order=True) #(init=False)
class Pessoa:
    nome: str
    sobrenome: str
    idade: int 
    dependentes: list[str] = field(default_factory=list) #Voce sempre precisa usar uma factory quando instancia um objeto mutável

    #def __post_init__(self):
    #    print("Eu acabei de executar o Post Init")
    
pessoa_1 = Pessoa("Yuri", "Saporito", 38)
print(fields(pessoa_1))
print(asdict(pessoa_1))
print(asdict(pessoa_1).keys())
print(asdict(pessoa_1).values())
print(asdict(pessoa_1).items())
print(astuple(pessoa_1))
print(astuple(pessoa_1)[0])

#pessoa_2 = Pessoa("Carlos", "Ivan", 1000)
#pessoa_3 = Pessoa("Homem", "de Meia-idade")
#
#print(pessoa_1)
#print(pessoa_2)
#print(pessoa_3)
#print(pessoa_1==pessoa_2)
#
##exemplo de order=True
#lista_de_herois = []
#lista_de_herois.append(pessoa_1)
#lista_de_herois.append(pessoa_2)
#lista_de_herois.append(pessoa_3)
#print(lista_de_herois)
#print(sorted(lista_de_herois))