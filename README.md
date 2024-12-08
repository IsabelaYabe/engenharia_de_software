# Sobre o Projeto

Este projeto faz parte da criação de um aplicativo de compras em Vending Machines gerenciado por uma universidade.

Para maiores detalhes sobre a implementação e características do programa, consulte o relatório presente no repositório.

A seguir, são dadas instruções para rodar o aplicativo sobre uma base de dados local.

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
Em seguida, insira a senha Alacazumba123* quando solicitado. Alem da senha, as outras credenciais seguem como padrões.

As credenciais esperadas pelo aplicativo são:
    "host": "localhost",
    "user": "root",
    "password": "Alacazumba123*",
    "database": "my_database"

## 5. Instalar dependências do projeto

```bash
pip install -r requirements.txt
```

## 6. Crie o banco de dados

O arquivo de inicialização monta as tabelas no banco de dados e as popula com alguns registros para fins didáticos.

Ele também realiza algumas operações que verificam a consistência do banco.

```bash
python3 src/init_database.py
```

## 7. Como executar o código

```bash
python3 src/app.py
```

No prompt, será indicada a inicialização do servidor flask, e constará uma porta.

Acesse a porta para visualizar uma página navegável que permite ver a página de login.

## 8. Navegação do aplicativo

No app, a página inicial possui um formulário para registrar um novo usuário; e um formulário de login, com opção para logar como user ou owner. O sistema por trás realiza a verificação de validade e, se tudo certo, passa para a página de Menu.

No Menu, botões para diferentes funcionalidades se dispõem: user e owner tem acesso a diferentes funcionalidades.

Ambos podem ver informações do seu perfil.

Ambos podem ver as máquinas existentes, mas somente user podem comentar ou reclamar de uma delas, selecionando a máquina correspondente e preenchendo o formulário. Os comentários e reclamações já feitos são dispostos na tela para que saibamos o que todos pensam do serviço.

A partir dessa tela, é possível acessar a página específica de cada máquina de vendas, onde encontram-se dispostos seus produtos, com todas as informações relevantes e com opção de compra.

Ao comprar, o sistema verifica a viabilidade, dado o preço e estoque do produto, e executa as deduções necessárias, que podem ser visualizadas na sua página de perfil.

Retornando ao Menu, o owner tem acesso a mais duas páginas. Na página de estoque, um owner possui dispostas as informações de todos os seus produtos em todas as suas tabelas. Essa página é só para visualização dos negócios.

A última página é de my machines, onde um owner pode observar com facilidade suas máquinas e sacar delas o montante resultante das compras. Observa-se que numa compra o dinheiro se destina à máquina e é necessário que seu owner saque a quantia, para que ela se apresente no seu perfil.

## 9. Como logar

Para permitir a fácil navegação do professor, criamos um único login que permite acessar as informações tanto de user como de owner.

Usename: 'Al1ce'
Password: 'alqqq'

Caso deseje observar somente como user ou owner, pode registrar o novo login e usar a partir daí.


## 10. Disposição dos arquivos

Na pasta test temos os arquivos de teste.
Na pasta src temos arquivos python para inicializar a base de dados padrão e rodar a aplicação.
Na subpasta src/templates temos o html base para cada página da aplicação.
Na subpasta src/static/js temos os arquivos js que permitem a interação do usuário com as páginas.
Na pasta schemas temos os diagramas usados na modelagem.
Na pasta reports temos os relatórios de cada etapa do trabalho.


---

## 11. Recursos Adicionais

- [Documentação Oficial do MySQL](https://dev.mysql.com/doc/)
- [MySQL Workbench](https://www.mysql.com/products/workbench/)