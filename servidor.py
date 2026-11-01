
import socket 

ip = input("IP de escuta: ") 
porta = int(input("Porta: "))

servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
servidor.setsockopt(socket.SQL_SOCKET, socket.SO_REUSEADDR, 1)
servidor.bind((ip, porta))
servidor.listen()
  print(f"Servidor escutando em {ip}:{porta}")


  conexao, endereco = servidor.accept()
  print(f"Cliente conectando: {endereco}")


  dados = conexao.recv(1024)
  print("Recebido:", dados.decode("utf-8"))
  conexao.sendall("Ola, cliente! Mensagem recebida.\n".encode("utf-8))


  conexao.close()
  servidor.close()



