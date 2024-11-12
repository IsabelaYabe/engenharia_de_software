from database_manager_central import DatabaseManagerCentral
from relationship_manager_central import RelationshipManagerCentral
#incluir num pacote
#criar um pacote colocar um arquivo __init__.py 
#organizar meu código em pacotes
#
database_manager_central = DatabaseManagerCentral("host", "user", "password", "database")
relationship_manager_central = RelationshipManagerCentral("host", "user", "password", "database")