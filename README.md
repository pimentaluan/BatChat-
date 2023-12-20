● Título do projeto: BatChat;

● Autores: Luan Pimenta Fernandes - luan.pimenta@academico.ifpb.edu.br
           Pedro Arthur de Holanda Nery - arthur.nery@academico.ifpb.edu.br
           Jonata Nascimento Barbosa - jonata.barbosa@academico.ifpb.edu.br;
           
● Disciplinas: Protocolos e Interconexão de Redes de Computadores - Leonidas Francisco de Lima Junior;

● Descrição do problema: O nosso programa é um chat feito com a API de sockets em python, no qual o cliente ao se conectar ao servidor, consegue criar um usuário, fazer login em um usuário, listar os usuários online, mandar um chat e sair;

● Arquivos do Projeto: 
servidor.py: Este arquivo contém o código do servidor para o chat BatChat. Ele é responsável por aceitar conexões de clientes, processar comandos enviados pelos clientes e encaminhar mensagens entre os clientes. O servidor mantém um registro de todos os usuários ativos e suas respectivas conexões de soquete. Ele usa threads para lidar com múltiplos clientes simultaneamente.

cliente.py: Este arquivo contém o código do cliente para o chat BatChat. Ele é responsável por conectar-se ao servidor, enviar comandos ao servidor e receber respostas. O cliente pode enviar comandos para criar um usuário, fazer login, listar usuários online, enviar uma mensagem e sair. As respostas do servidor são exibidas para o usuário.;

● Pré-requisitos para execução: 
Python 3.x: Linguagem de programação usada para desenvolver o projeto. Pode ser instalado a partir do site oficial do Python.
Biblioteca socket: Biblioteca padrão do Python para criar conexões de rede. Não requer instalação adicional.
Biblioteca threading: Biblioteca padrão do Python para suporte a threads. É usada para permitir que o servidor lide com múltiplos clientes simultaneamente. Não requer instalação adicional.
Biblioteca sys: Biblioteca padrão do Python para acessar algumas variáveis usadas ou mantidas pelo interpretador Python. É usada para acessar argumentos da linha de comando. Não requer instalação adicional.;

● Protocolo da Aplicação: 
O protocolo da aplicação consiste em uma série de comandos que o cliente pode enviar ao servidor, como NOVO para criar um usuário, ENTRAR para fazer login, LISTA para listar usuários online, CHAT para enviar uma mensagem e SAIR para desconectar.;

● Instruções para execução: 
Execute o arquivo servidor.py para iniciar o servidor.
Em um terminal separado, execute o arquivo cliente.py para iniciar o cliente.
Comandos disponíveis:

* NOVO <username> <password>: Registra um novo usuário.
    Argumentos:
        username: O nome de usuário do novo usuário.
        password: A senha do novo usuário.

* ENTRAR <username> <password>: Loga um usuário existente.
    Argumentos:
        username: O nome de usuário do usuário existente.
        password: A senha do usuário existente.

* LISTA: Lista todos os usuários registrados.

* CHAT <username> <mensagem>: Inicia um chat com o usuário especificado, enviando mensagem.
    Argumentos:
        username: O nome de usuário do usuário com quem você deseja conversar.
        mensagem: A mensagem que o usuário deseja enviar

* SAIR: Encerra a conexão com o servidor.;
