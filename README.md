# Sistema Cliente-Servidor: Jogo de Par ou Ímpar

![Status](https://img.shields.io/badge/status-terminado-green)
![Linguagem](https://img.shields.io/badge/linguagem-Python-blue)

## 📖 Sobre o Projeto
Este projeto foi desenvolvido para a disciplina **Rede de Computadores** do curso de **Engenharia de Computação** na **UFMS (Universidade Federal de Mato Grosso do Sul)**.  
O objetivo é **implementar a comunicação entre um servidor e múltiplos clientes**, permitindo que os clientes joguem **Par ou Ímpar** entre si, com **gerenciamento centralizado pelo servidor**.

---

## 🚀 Funcionalidades
- **Servidor Central**
  - Gerencia múltiplos clientes conectados simultaneamente.
  - Cria partidas entre clientes disponíveis.
  - Envia resultados das partidas aos jogadores.

- **Cliente**
  - Conecta-se ao servidor via socket.
  - Permite cadastro com nome de usuário.
  - Possui menu interativo para:
    - Jogar imediatamente contra outro cliente disponível.
    - Escolher um jogador específico para desafiar.
    - Listar jogadores conectados.

---

## 📂 Estrutura do Código
server.py # Código do servidor, responsável por gerenciar conexões e partidas.
client.py # Código base do cliente.
network.py # Classe responsável pela comunicação cliente-servidor (Network).
