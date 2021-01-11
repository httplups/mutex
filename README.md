# Relógio de Lamport

Implementação que simula um algoritmo centralizado de exclusão mútua, na comunicação entre 1 coordenador e 2 processos. 
Note que nesta implementação, quando um processo pede permissão a um arquivo para o coordenador, este não especifica o nome do arquivo.
Isso foi feito assumindo que todos os processos querem acessar o mesmo arquivo, da qual o coordenador cuida, para simplificação da implementação. 
No entanto, o conceito de troca de mensagens para obter permissão é o mesmo. Note ainda que no caso ideal, deveria ter uma fila associada a cada arquivo. 
Como estamos falando de um em específico, existe apenas uma única fila. Não há na verdade a modificação de um arquivo na máquina do coordenador pelo processo. 
O que é feito é uma simulação, com um arquivo de log.txt mostrando quem modificou o arquivo. 

## Pré-requisitos
Python3

## Uso
Coloquei um IP e porta da instância servidor da AWS previamente configuradas no grupo de segurança. Para testar com outra máquina, deve-se substituir. 
Se quiser testar localmente, o ip_publico deve ser 127.0.0.1.
O teste que fiz no vídeo foi executar o coordenador primeiro, que é como se fosse um servidor de permissões. 
Depois um processo 1 que pede a permissão do arquivo por X segundos (variavel time). 
Depois um processo 2 que pede a permissão do arquivo por Y segundos (variavel time).

* fiz com que X fosse suficientemente grande para dar tempo de chamar a execução de P2.
* o processo 1 e 2 tem a mesma base de codígo, arquivo p1.py

1. Executar o coordenador
```bash
   python3 coord.py
```

2. Executar o 1º cliente
```bash
   python3 p1.py ip_publico time
```
3. Executar o 2º cliente
```bash
   python3 p1.py ip_publico time
```
No teste do vídeo, rodamos os processos como:
```bash
   python3 p1.py 54.145.129.76 15
```
3. Executar o 2º cliente
```bash
   python3 p1.py 54.145.129.76 5
```   

Obtivemos a seguinte saída:

Servidor:
```bash
    Coordinator started!
    Waiting for requests...
    Queue:
    [('3.83.25.185', 35798)]
    Queue:
    [('3.83.25.185', 35798), ('18.212.33.91', 59324)]
    Queue:
    [('18.212.33.91', 59324)]
    Queue:
    []
    ^CBye bye...
```

Processo 1:
```bash
    This IP address is:  3.83.25.185
    Trying to get permission...
    Allowed
    I am doing something with the file...
    Terminou
```

Cliente 2:
```bash
    This IP address is:  18.212.33.91
    Trying to get permission...
    Allowed
    I am doing something with the file...
    Terminou
```
