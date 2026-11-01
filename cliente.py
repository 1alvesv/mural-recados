import socket

LIMITE_CARACTERES = 120


def ler_avisos(cliente, leitor):
    cliente.sendall("LER\n".encode("utf-8"))
    print()
    print("=" * 50)
    print("MURAL DE AVISOS")
    print("=" * 50)
    quantidade = 0
    while True:
        linha = leitor.readline()
        if linha == "":
            print("Conexao encerrada pelo servidor.")
            return False
        linha = linha.strip()
        if linha == "FIM":
            break
        id_recado, autor, texto = linha.split("|", 2)
        print(f"ID: {id_recado}")
        print(f"Autor: {autor}")
        print(f"Aviso: {texto}")
        print("-" * 50)
        quantidade += 1
    if quantidade == 0:
        print("O mural esta vazio.")
    return True


def escrever_aviso(cliente, leitor, autor):
    texto = input("Digite o aviso: ").strip()
    if texto == "":
        print("Erro: o aviso nao pode ser vazio.")
        return True
    if len(texto) > LIMITE_CARACTERES:
        print(f"Erro: o aviso tem {len(texto)} caracteres, o limite e {LIMITE_CARACTERES}.")
        return True
    cliente.sendall(f"ESCREVER|{autor}: {texto}\n".encode("utf-8"))
    resposta = leitor.readline()
    if resposta == "":
        print("Conexao encerrada pelo servidor.")
        return False
    resposta = resposta.strip()
    if resposta.startswith("OK|"):
        print(f"Aviso publicado com o ID {resposta.split('|')[1]}.")
    else:
        print("O servidor recusou o aviso:", resposta.split("|", 1)[1])
    return True


ip = input("IP do servidor: ")
porta = int(input("Porta: "))
autor = input("Seu nome: ").strip()
while autor == "" or "|" in autor or ":" in autor:
    print("Nome invalido: nao pode ser vazio nem ter | ou :")
    autor = input("Seu nome: ").strip()

cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
cliente.connect((ip, porta))
leitor = cliente.makefile("r", encoding="utf-8")
print(f"Conectado ao servidor como {autor}!")

ativo = True
while ativo:
    print()
    print("1 - Ler avisos do mural")
    print("2 - Escrever novo aviso")
    print("0 - Sair")
    opcao = input("Escolha: ").strip()
    if opcao == "1":
        ativo = ler_avisos(cliente, leitor)
    elif opcao == "2":
        ativo = escrever_aviso(cliente, leitor, autor)
    elif opcao == "0":
        ativo = False
    else:
        print("Opcao invalida.")

leitor.close()
cliente.close()
print("Ate logo!")
