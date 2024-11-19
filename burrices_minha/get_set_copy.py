class Alarme:
    def __init__(self, estado):
        self.__estado = estado

    @property
    def estado(self):
        return self.__estado
    
    @estado.setter
    def estado(self, valor):
        self.__estado = valor
        
alarme = Alarme(False)
print(f"Alarme inicializado com estado: {alarme.estado}")  

alarme_get = alarme.estado
print(f"alarme.estado atribuído à variável alarme_get: {alarme_get}")

alarme_get = True
print(f"Alterando o valor da variável alarme_get: {alarme_get}")
print(f"Verificando o estado do objeto alarme: {alarme.estado}")

alarme.estado = True  
print(f"Alterando o estado do objeto alarme com setter: {alarme.estado}")
