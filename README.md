# BatChat 🦇💬

O BatChat é um chat simples desenvolvido em Python utilizando a API de sockets. Este projeto tem como objetivo permitir a comunicação entre clientes em um ambiente de chat, com funcionalidades básicas como criação de usuário, login, listagem de usuários online e envio de mensagens.


## Tecnologias Usadas

<div style="display:flex">
  <img aling="center" alt="python" src="https://img.shields.io/badge/Python-14354C?style=for-the-badge&logo=python&logoColor=white">
</div>

## Funcionalidades Principais 📝🔍

- **Cadastro de Usuário:** Permite criar um novo usuário com nome de usuário e senha.
- **Login de Usuário:** Permite que um usuário existente faça login no sistema.
- **Listagem de Usuários Online:** Mostra a lista de todos os usuários que estão atualmente online.
- **Envio de Mensagens:** Permite enviar mensagens para outros usuários registrados.
- **Desconexão:** Permite que um usuário encerre sua conexão com o servidor.

## Instalação e Configuração ⚙️🔧

1. **Clone o repositório:**
    ```
    https://github.com/pimentaluan/BatChat-.git
    ```

2. **Certifique-se de ter o Python 3.x instalado:** A biblioteca padrão do Python já inclui `socket`, `threading` e `sys`, então não são necessárias instalações adicionais.

3. **Execute o servidor:**
    Navegue até o diretório onde o `servidor.py` está localizado e execute:
    ```
    python servidor.py
    ```

4. **Execute o cliente:**
    Em um terminal separado, navegue até o diretório onde o `cliente.py` está localizado e execute:
    ```
    python cliente.py
    ```

## Comandos Disponíveis

- **NOVO <username> <password>:** Registra um novo usuário.
    - **Argumentos:**
        - `username`: O nome de usuário do novo usuário.
        - `password`: A senha do novo usuário.

- **ENTRAR <username> <password>:** Loga um usuário existente.
    - **Argumentos:**
        - `username`: O nome de usuário do usuário existente.
        - `password`: A senha do usuário existente.

- **LISTA:** Lista todos os usuários registrados.

- **CHAT <username> <mensagem>:** Inicia um chat com o usuário especificado, enviando a mensagem.
    - **Argumentos:**
        - `username`: O nome de usuário do destinatário.
        - `mensagem`: A mensagem a ser enviada.

- **SAIR:** Encerra a conexão com o servidor.
