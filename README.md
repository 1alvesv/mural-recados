# Mural Coletivo de Recados

-- Descrição do Projeto --

Projeto desenvolvido para a disciplina de Redes de Computadores I. consiste em um mural de avisos que funciona pela rede.

Um programa chamado -SERVIDOR- guarda os avisos. Outro programa, o -CLIENTE-, se conecta ao servidor para ler os avisos ou escrever um aviso novo. A conexão usa -SOCKETS TCP- e o código foi desenvolvido na linguagem -PYTHON-

O mural guarda no máximo 10 avisos. Quando chega o 11º aviso, o mais antigo é apagado e cada aviso recebe um número (ID) que aumenta de 1 em 1.

- O que o projeto faz

- Mostra os avisos do mural com ID, autor e texto.
- Publica um aviso novo (de no máximo 120 caracteres).
- O cliente não deixa enviar aviso vazio ou maior que 120 caracteres.
- Vários clientes podem usar o mural ao mesmo tempo (o servidor utiliza threads).
- Bônus 1: salva os avisos no arquivo mural_avisos.txt, e eles voltam quando o servidor é reiniciado.
- Bônus 2: troca palavras da lista PALAVRAS_PROIBIDAS por *** antes de publicar o aviso.

- Pré-requisitos

- Duas máquinas virtuais com Debian 13 no VirtualBox (uma para o servidor e outra para o cliente), as duas com a rede em modo -BRIDGE- para ficarem na mesma rede.
- Python 3.
- Git (sudo apt install git).

- Como executar

1. Baixar o projeto (nas duas VMs):

git clone https://github.com/1alvesv/mural-recados.git
cd mural-recados

2. Descobrir o IP do servidor (na VM do servidor):

ip a

O IP aparece na linha -inet- da placa. Exemplo: 192.168.0.117

3. Rodar o servidor (na VM do servidor):

python3 servidor.py

O programa pergunta o IP e a porta. Digite 0.0.0.0 e 5000.

4. Rodar o cliente (na VM do cliente):

python3 cliente.py

O programa pergunta o IP do servidor, a porta (5000) e o seu nome. Depois aparece o menu:

- 1: ler os avisos do mural
- 2: escrever um novo aviso
- 0: sair

- Exemplos de execução

Servidor:

$ python3 servidor.py
Nenhum arquivo de mural encontrado, comecando vazio.
IP de escuta: 0.0.0.0
Porta: 5000
Servidor escutando em 0.0.0.0:5000

Cliente lendo o mural vazio e publicando um aviso:

$ python3 cliente.py
IP do servidor: 192.168.0.117
Porta: 5000
Seu nome: Lingard
Conectado ao servidor como Lingard!

1 - Ler avisos do mural
2 - Escrever novo aviso
0 - Sair
Escolha: 1

==================================================
MURAL DE AVISOS
==================================================
O mural esta vazio.

Escolha: 2
Digite o aviso: reuniao do grupo amanha as 14h
Aviso publicado com o ID 1.

Aviso vazio e aviso muito grande (o cliente não envia):

Escolha: 2
Digite o aviso: 
Erro: o aviso nao pode ser vazio.

Escolha: 2
Digite o aviso: Este aviso de teste foi escrito de proposito para ser muito maior que o limite ...
Erro: o aviso tem 213 caracteres, o limite e 120.

Filtro de palavras (aviso digitado: *hoje tem PIZZA e chocolate no lanche*):

ID: 3
Autor: Lingard
Aviso: hoje tem *** e *** no lanche
--------------------------------------------------

Fila circular: depois de publicar 11 avisos, o aviso de ID 1 some e ficam só os 10 mais novos (IDs de 2 a 11).

Persistência: ao ligar o servidor de novo, os avisos voltam:

$ python3 servidor.py
10 aviso(s) restaurado(s) de mural_avisos.txt

O aviso novo continua a numeração (no teste, recebeu o ID 15).

- Como o cliente e o servidor conversam

As mensagens são textos de uma linha. Para ler o mural o cliente envia LER, e o servidor responde com um aviso por linha (ID|Autor|Mensagem) e termina com FIM. Para escrever, o cliente envia ESCREVER|Autor: Mensagem, e o servidor responde OK|ID se deu certo ou ERRO|motivo se não deu.

- Arquivos
    - servidor.py: o servidor.
    - cliente.py: o cliente.
    - mural_avisos.txt: criado pelo servidor para guardar os avisos.

- Integrantes
  - Ícaro Vladimir
  - Charles William
