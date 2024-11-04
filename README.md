# Sobre o Projeto

Este projeto faz parte da criação de um aplicativo de compras em Vending Machines gerenciado por uma universidade.

# Requisitos Atendidos

Durante a Sprint, foram implementados e entregues os seguintes requisitos funcionais (RF) e não funcionais (NR):

- **RF7 - Comentar sobre Produto**: Foi implementada a funcionalidade para os usuários escreverem comentários sobre produtos.
- **RF10 - Visualizar Estoque**: Gestores podem visualizar o estoque de produtos nas vending machines, auxiliando na tomada de decisões.
- **RF14 - Perfil da Vending Machine**: Os usuários podem visualizar as vending machines, indicados os produtos delas.
- **RF33 - Reportar Problemas**: Usuários podem reportar problemas direcionados a cending machines ou ao sistema. Gestores podem vsualizar o que foi reportado.
- **RFNA - Visualizar Profuto**: Usuários podem visualizar informações do produto. 
Outros requisitos foram parcialmente implementados, mas não constam na main do projeto.

# Organização dos Arquivos

# Requisitos Para a Execução


## Instruções para Instalação do MySQL

Para instalar o MySQL em diferentes sistemas operacionais, siga as instruções específicas para seu sistema.

## 1. Instalação no Ubuntu/Debian (Linux)

### Passo 1: Atualize o sistema
Abra um terminal e execute os seguintes comandos para garantir que o sistema esteja atualizado:

```bash
sudo apt update
sudo apt upgrade
```

### Passo 2: Instale o MySQL
Instale o MySQL com o seguinte comando:

```bash
sudo apt install mysql-server
```

### Passo 3: Verifique o serviço MySQL
Após a instalação, o serviço MySQL deve ser iniciado automaticamente. Verifique o status do serviço:

```bash
sudo systemctl status mysql
```

### Passo 4: Executar o script de segurança do MySQL
Este script ajudará a configurar a segurança do seu servidor MySQL, permitindo definir uma senha para o usuário root, remover usuários anônimos, desabilitar o login remoto do root e remover o banco de dados de teste:

```bash
sudo mysql_secure_installation
```

### Passo 5: Acessar o MySQL
Para acessar o console do MySQL, use:

```bash
sudo mysql
```

Você agora está pronto para utilizar o MySQL no Ubuntu/Debian!

---

## 2. Instalação no Windows

### Passo 1: Baixe o MySQL Installer
Baixe o MySQL Installer para Windows do site oficial:
[Download MySQL Installer](https://dev.mysql.com/downloads/installer/)

### Passo 2: Execute o MySQL Installer
Abra o instalador e siga as instruções na tela. Escolha o tipo de instalação "Developer Default" para ter uma configuração completa com todos os componentes essenciais, ou "Server only" para instalar apenas o servidor.

### Passo 3: Configure o Servidor MySQL
Durante a instalação, você será solicitado a configurar o servidor MySQL:

- Defina uma senha de root.
- Escolha o tipo de servidor (Standalone MySQL Server).
- Selecione a porta padrão (3306).

### Passo 4: Complete a Instalação
Após a instalação, você poderá iniciar o MySQL Workbench ou acessar o MySQL via linha de comando.

---

## 3. Instalação no macOS

### Passo 1: Instalar via Homebrew
Se você tem o Homebrew instalado, pode facilmente instalar o MySQL com o comando:

```bash
brew install mysql
```

### Passo 2: Iniciar o serviço MySQL
Depois da instalação, inicie o MySQL com o comando:

```bash
brew services start mysql
```

### Passo 3: Configurar e Acessar o MySQL
Após a instalação, você pode configurar a senha de root e acessar o MySQL:

```bash
mysql_secure_installation
mysql -u root -p
```

---

## 4. Conectar-se ao MySQL

Você pode usar clientes MySQL como o **MySQL Workbench** ou **phpMyAdmin** para gerenciar seu banco de dados visualmente, ou utilizar o terminal para executar comandos SQL.

### Exemplo de conexão via terminal:

```bash
mysql -u root -p
```
Em seguida, insira a senha Alacazumba123* quando solicitado.

## 5. Instalar dependências do projeto

```bash
pip install -r requirements.txt
```

## 6. Crie o banco de dados

```bash
python3 src/init_database.py
```



## 7. Como executar o código

```bash
python3 src/app.py
```

No prompt, será indicada a inicialização do servidor flask, e constará uma porta.

Acesse a porta para visualizar uma página navegável que permite ver o estoque, comentários, reclamações e as vending machines.

## 8. Testes

```bash
python3 test/test_comment_profile.py
python3 test/test_complaints.py
python3 test/test_comment_profile.py
python3 test/test_stock_profile.py
```


## 9. Disposição dos arquivos

Na pasta test temos os arquivos de teste.
Na pasta src temos arquivos python para inicializar a base de dados padrão e rodar a aplicação.
Na subpasta src/templates temos o html base para cada página da aplicação.
Na subpasta src/profiles temos os arquivos python para as classes de acesso à base de dados.
Na subpasta src/static/js temos os arquivos js que permitem a interação do usuário com as páginas.
Na pasta schemas temos os diagramas usados na modelagem.
Na pasta reports temos os relatórios de cada etapa do trabalho.


---

## 9. Recursos Adicionais

- [Documentação Oficial do MySQL](https://dev.mysql.com/doc/)
- [MySQL Workbench](https://www.mysql.com/products/workbench/)