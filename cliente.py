
import socket

ip = input("IP do servidor: ")
porta = int(input("Porta: "))

cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
cliente.connect((ip, porta))
print("Conectado ao servidor!")

cliente.sendall("Ola, servidor!\n".encode("utf-8"))
resposta = cliente.recv(1024)
print("Resposta:", resposta.decode("utf-8"))

cliente.close()


