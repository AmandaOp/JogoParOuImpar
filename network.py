import socket

class Network:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = "172.19.0.1"
        self.port = 5555
        self.addr = (self.server, self.port)
        self.id = self.connect()
        #print(self.id)

    def connect(self):
        try:
            self.client.connect(self.addr)
            return self.client.recv(2048).decode()
        except:
            pass

    def send(self, data):
        try:
            self.client.send(str.encode(data))
            return self.client.recv(2048).decode()
        except socket.error as e:
            return None

def menu():
    print("Menu:")
    print("[0] Para sair")
    print("[1] Jogar agora")
    print("[2] Escolher jogador")
    

n = Network()
num = -1
if n.id == None:
    print("O servidor esta fora do ar")
    num = 0
else:
    print("Jogo do par ou impar")
    name = str(input("Informe nome do usuario: "))
    print(n.send(name))
    print("Aqui")
    print(n.send(name))

while(num!=0):
    menu()
    num = int(input())
    if num == 1:
        print("Voce sera encaminhado para uma partida")
        res = n.send(str(num+10))
        if res == None:
            num = 0
            print("Impossivel obter resposta do servidor")
        else:
            print(res)
    elif num == 2:
        print("Lista de Jogadores")
        res = n.send(str(num+10))
        if res == None:
            num = 0
            print("Impossivel obter resposta do servidor")
        else:
            print(res)