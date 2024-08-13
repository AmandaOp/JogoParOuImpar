import socket
import pickle

class Client:

  def __init__(self, ip, port):
    self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    self.server = ip
    self.port = port
    self.addr = (self.server, self.port)
    self.id = self.connect()

  def connect(self):
    try:
      self.client.connect(self.addr)
      return self.client.recv(2048).decode()
    except:
      print("Problema ao se conectar")
      return False

  def send(self, data):
    try:
      self.client.send(str.encode(data))
      return self.client.recv(2048).decode()
    except socket.error as e:
      print(e)

  def receiver(self):
    try:
      return self.client.recv(2048).decode()
    except socket.error as e:
      print(e)

  def send_dic(self, data):
    try:
      self.client.send(str.encode(data))
      resposta = self.client.recv(2048)
      return pickle.loads(resposta)
    except socket.error as e:
      print(e)

def menu_login(client):
  while (True):
    print("Você Deseja:")
    print("[1] Cadastrar")
    print("[2] Entrar")
    print("[3] Sair")
    res = input()
    if res == '1':
      if(cadastro(client)):
        return True
    elif res == '2':
      if (login(client)):
        return True
    elif res == '3':
      return False
    else:
      print("Opção Inválida")
      return False
  return True


def cadastro(client):
  print("Cadastro")
  name = input("Nome: ")
  user = input("Nome de usuario: ")
  password = input("Senha: ")
  client.send("register")
  client.send(name)
  client.send(user)
  client.send(password)
  print(client.receiver())
  return login(client)


def login(client):
  print("Login")
  user = input("Usuario: ")
  password = input("Senha: ")
  client.send("authentication")
  client.send(user)
  client.send(password)
  res = client.receiver()
  if res == "true":
    print("Login feito com sucesso!")
    return True
  else:
    print("Usuario ou senha incorretos! Tente Novamente.")
    return False


def desconnect(client):
  print(client.send("disconnect"))


def game_over(client):
  client.send("game_over")


def start_game(client, player2):
  client.send("start_game")
  client.send(player2)
  print(client.receiver())


def get_ip_client(client):
  return client.send("get_ip")


def get_port_client(client):
  return int(client.send("get_port"))


def list_user_on_line(client):
  return client.send_dic("list_user_on_line")


def game(connection):
  print("Jogo do Par ou Impar")
  print("Esperando escolha do oponente")
  data = connection.recv(2048)
  res = data.decode()
  print("recebeu mensagem")

  if res == "par":
    print("Você é Impar")
    connection.send(str.encode("Impar"))
  elif res == "impar":
    print("Você é Par")
    connection.send(str.encode("Par"))
  else:
    print("Erro, jogo encerrado")
    return False

  num2 = str(input("Digite um número de 0 a 5: "))
  data = connection.recv(2048)
  num1 = data.decode()
  connection.send(str.encode(num2))

  sum = int(num1) + int(num2)

  if sum % 2 == 0:
    if res == "impar":
      # jogador 2 ganhou
      print("PARABENS! Você ganhou :)")
    elif res == "par":
      # jogador 1 ganhou
      print("Não foi dessa vez :'(")
  else:
    if res == "par":
      # jogador 2 ganhou
      print("PARABENS! Você ganhou :)")
    elif res == "impar":
      # jogador 1 ganhou
      print("Não foi dessa vez :'(")

  return True


def host_game(player1):
  print("Jogo do Par ou Impar")
  print("Escolha:")
  print("[1] Impar")
  print("[2] Par")

  res = input()
  if res == 1:
    player1.send("impar")
  elif res == 2:
    player1.send("par")
  else:
    player1.send("game_over")
    # Mandar estado de game over para servidor
    return False

  num1 = str(input("Digite um número de 0 a 5: "))
  num2 = player1.send(num1)

  sum = int(num1) + int(num2)

  if sum % 2 == 0:
    if res == 2:
      # jogador 2 ganhou
      print("PARABENS! Você ganhou :)")
    elif res == 1:
      # jogador 1 ganhou
      print("Não foi dessa vez :'(")
  else:
    if res == 1:
      # jogador 2 ganhou
      print("PARABENS! Você ganhou :)")
    elif res == 2:
      # jogador 1 ganhou
      print("Não foi dessa vez :'(")


def invite(client):
  dic = list_user_on_line(client)
  print(dic)
  #for user, status, ip, port in dic.items():
  #   print(user, status, ip, port)
  user2 = input("Escolha um user para jogar: ")
  print("user escolhido: ", user2)
  ip = dic[user2][1]
  port = int(dic[user2][2]) + 1
  print("ip", ip)
  print("porta", port)

  player1 = Client(ip, port)
  print("id", player1.id)
  if player1.id:
    print("Conectou")
    res = player1.send("game_ini")
    print("Mandou game_ini")
    if res == "game_ack":
      print("recebeu ack")
      start_game(client, user2)
      print("mandou start")
      host_game(player1)
      print("passou de host_game")
      game_over(client)
    else:
      print("recebeu neg")
      print("O convite foi recusado!")
      print("Você será direcionado ao menu principal.")
  else:
    print("Impossivel conectar a esse jogador.")
    print("Você será direcionado ao menu principal.")


def wait(client):
  myIP = get_ip_client(client)
  myPort = int(get_port_client(client)) + 1
  print("ip", myIP)
  print("port", myPort)
 
  client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  try:
    client_socket.bind((myIP, myPort))
  except socket.error as e:
    str(e)
  client_socket.listen(1)

  while True:
    print("Aguardando convites...")
    connection, addr = client_socket.accept()
    print("Connected to:", addr)
    try:
      connection.send(str.encode("Connected to the server"))
      print("Entrou no try")
      sentence = connection.recv(2048).decode()
      print("recebeu solicitação")
      if sentence == "game_ini":
        print("Você recebeu um convite")
        print("[1] Aceitar")
        print("[2] Recusar")
        res = input()
        if res == '1':
          connection.sendall(str.encode("game_ack"))
          game(connection)
          connection.close()
        else:
          connection.sendall(str.encode("game_neg"))
          connection.close()
      else:
        print("Erro! Fechando conexão")
        connection.sendall(str.encode("Erro! Fechando conexão"))
        connection.close()
    except:
      connection.close()

  client_socket.close()


def menu_hall():
  print("Bem vindo ao menu principal")
  print("[1] Escolher jogador")
  print("[2] Esperar convite")
  print("[3] Sair")
  return input()


def hall(client):
  while (True):
    res = menu_hall()
    if res == '1':
      invite(client)
    elif res == '2':
      wait(client)
    elif res == '3':
      desconnect(client)
      break
    else:
      print("Opção Inválida")


ip = "172.19.0.1"
port = 5555
client = Client(ip, port)
if client.id:
  res = menu_login(client)
  if res:
    hall(client)
  else:
    desconnect(client)
