import socket
import threading
from collections import deque

LIMITE_RECADOS = 10
LIMITE_CARACTERES = 120

mural = deque(maxlen=LIMITE_RECADOS)
proximo_id = 1
trava = threading.Lock()


def publicar(autor, texto):
    global proximo_id
    with trava:
        novo_id = proximo_id
        mural.append((novo_id, autor, texto))
        proximo_id += 1
    return novo_id


def montar_feed():
    with trava:
        recados = list(mural)
    linhas = []
    for id_recado, autor, texto in recados:
        linhas.append(f"{id_recado}|{autor}|{texto}")
    linhas.append("FIM")
    return "\n".join(linhas) + "\n"


def tratar_pedido(linha):
    if linha == "LER":
        return montar_feed()
    if linha.startswith("ESCREVER|"):
        conteudo = linha[len("ESCREVER|"):]
        if ":" not in conteudo:
            return "ERRO|Formato invalido. Use Autor: Mensagem\n"
        autor, texto = conteudo.split(":", 1)
        autor = autor.strip()
        texto = texto.strip()
        if autor == "" or texto == "":
            return "ERRO|Autor e mensagem nao podem ser vazios\n"
        if "|" in autor:
            return "ERRO|O nome do autor nao pode ter o caractere |\n"
        if len(texto) > LIMITE_CARACTERES:
            return f"ERRO|Mensagem acima de {LIMITE_CARACTERES} caracteres\n"
        novo_id = publicar(autor, texto)
        return f"OK|{novo_id}\n"
    return "ERRO|Comando desconhecido\n"


def atender_cliente(conexao, endereco):
    print(f"Cliente conectado: {endereco}")
    leitor = conexao.makefile("r", encoding="utf-8")
    try:
        for linha in leitor:
            linha = linha.strip()
            print(f"Recebido de {endereco}: {linha}")
            resposta = tratar_pedido(linha)
            conexao.sendall(resposta.encode("utf-8"))
    except (ConnectionResetError, BrokenPipeError):
        print(f"Conexao perdida com {endereco}")
    finally:
        leitor.close()
        conexao.close()
        print(f"Cliente desconectado: {endereco}")


ip = input("IP de escuta: ")
porta = int(input("Porta: "))

servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
servidor.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
servidor.bind((ip, porta))
servidor.listen()
print(f"Servidor escutando em {ip}:{porta}")

try:
    while True:
        conexao, endereco = servidor.accept()
        fio = threading.Thread(target=atender_cliente, args=(conexao, endereco), daemon=True)
        fio.start()
except KeyboardInterrupt:
    print("\nServidor encerrado.")
finally:
    servidor.close()
