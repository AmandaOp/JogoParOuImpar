import socket
import pickle
from _thread import *
import sys
import logging

server = "172.19.0.1"
port = 5555

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
  server_socket.bind((server, port))
except socket.error as e:
  str(e)

server_socket.listen()
print("Waiting for a connection, Server Started")


def newMessage(connection):
  try:
    reply = ""
    data = connection.recv(2048)
    reply = data.decode()
    connection.sendall(str.encode(reply))
    return reply
  except:
    return None


def new_register(name, user, password):
  clients.update({user: (password, name)})
  print("novo cadastro")


def new_user(user, status, ip, port):
  print(user)
  userOnline.update({user: (status, ip, port)})
  print("nova autenticacao")


def new_game(game_id, user1, ip1, port1, user2, ip2, port2):
  userPlaying.update({game_id: ((user1, ip1, port1), (user2, ip2, port2))})
  # escreve no game.log "usuário X e Y: PLAYING"
  logger.info(f"Usuário {user1} e {user2}: PLAYING")

  userOnline.update({user1: (1, ip1, port1)})
  # escreve no game.log "usuário X tornou-se ATIVO"
  logger.info(f"Usuário {user1} tornou-se ATIVO")
  userOnline.update({user2: (1, ip2, port2)})
  # escreve no game.log "usuário Y tornou-se ATIVO"
  logger.info(f"Usuário {user2} tornou-se ATIVO")


def remove_game(game_id, user1, ip1, port1, user2, ip2, port2):
  userPlaying.pop(game_id)
  userOnline.update({user1: (0, ip1, port1)})
  # escreve no game.log "usuário X tornou-se INATIVO"
  logger.info(f"Usuário {user1} tornou-se INATIVO")
  userOnline.update({user2: (0, ip2, port2)})
  # escreve no game.log "usuário Y tornou-se INATIVO"
  logger.info(f"Usuário {user2} tornou-se INATIVO")


def threaded_client(connection, addr):
  connection.send(str.encode("Connected to the server"))
  reply = ""
  user = ""
  game_id = 0
  while True:
    try:
      data = connection.recv(2048)
      reply = data.decode()

      if not data:
        logger.info(f"Usuário {user} não responde")
        break
      else:
        print("Received: ", reply)

      if reply == "register":
        connection.sendall(str.encode("Register"))
        name = newMessage(connection)
        user = newMessage(connection)
        password = newMessage(connection)
        if user in clients:
          print("Usuário já cadastrado")
          connection.sendall(str.encode("Usuario já cadastrado"))
        else:
          new_register(name, user, password)
          connection.sendall(str.encode("Cadastro efetuado com sucesso"))
          # escreve no game.log "usuário X realizou cadastro"
          logger.info(f"Usuário {user} realizou cadastro")

      elif reply == "authentication":
        connection.sendall(str.encode("Authentication"))
        user = newMessage(connection)
        password = newMessage(connection)
        if user in clients:
          if clients[user][0] == password:
            connection.sendall(str.encode("true"))
            print("aqui")
            new_user(user, 0, addr[0], addr[1])
            # escreve no game.log "usuário X conectou-se"
            logger.info(f"Usuário {user} conectou-se")
          else:
            connection.sendall(str.encode("false"))
        else:
          connection.sendall(str.encode("false"))

      elif reply == "start_game":
        connection.sendall(str.encode("Start Game"))
        ip1 = userOnline[user][1]
        port1 = userOnline[user][2]
        user2 = newMessage(connection)
        if user2 in userOnline:
          ip2 = userOnline[user2][1]
          port2 = userOnline[user2][2]
          game_id = int(port1 + port2)
          connection.sendall(str.encode("Iniciando jogo"))
          new_game(game_id, user, ip1, port1, user2, ip2, port2)
        else:
          connection.sendall(str.encode("Usuário inválido"))

      elif reply == "game_over":
        connection.sendall(str.encode("Game over"))
        user1 = userPlaying[game_id][0][0]
        ip1 = userOnline[user1][1]
        port1 = userOnline[user1][2]
        user2 = userPlaying[game_id][1][0]
        ip2 = userOnline[user2][1]
        port2 = userOnline[user2][2]
        remove_game(game_id, user1, ip1, port1, user2, ip2, port2)
        game_id = 0

      elif reply == "list_user_on_line":
        connection.sendall(pickle.dumps(userOnline))

      elif reply == "list_user_playing":
        connection.sendall(pickle.dumps(userPlaying))

      elif reply == "get_ip":
        connection.sendall(str.encode(str(addr[0])))

      elif reply == "get_port":
        connection.sendall(str.encode(str(addr[1])))

      elif reply == "disconnect":
        connection.sendall(str.encode("Você foi desconectado do servidor"))
        # escreve no game.log "usuário X desconectou-se da rede"
        logger.info(f"Usuário {user} desconectou-se da rede")
        break
      else:
        connection.sendall(str.encode("invalid_message"))

    except:
      break

  print("Lost connection")
  connection.close()
  if game_id != 0:
    user1 = userPlaying[game_id][0][0]
    ip1 = userOnline[user1][1]
    port1 = userOnline[user1][2]
    user2 = userPlaying[game_id][1][0]
    ip2 = userOnline[user2][1]
    port2 = userOnline[user2][2]
    remove_game(game_id, user1, ip1, port1, user2, ip2, port2)
  userOnline.pop(user)


clients = {}
userOnline = {}
userPlaying = {}

while True:
  connection, addr = server_socket.accept()
  print("Connected to:", addr)
  logging.basicConfig(filename="game.log",
                      format='%(asctime)s %(message)s',
                      filemode='a')
  logger = logging.getLogger()
  logger.setLevel(logging.INFO)

  start_new_thread(threaded_client, (
      connection,
      addr,
  ))
