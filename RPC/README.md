# Atividade - RPC

Este projeto contém uma implementação de um RPC entre Cliente e Servidor em Python, utilizando sockets TCP.

## Estrutura

O projeto contém a seguinte estrutura:

- `server.py`: Implementa o servidor
- `client.py`: Implementa o cliente
- `rpc.py`: Implementa o RPC que faz a comunicação entre o cliente e o servidor

## Cliente

O script `client.py` implementa o cliente RPC que se conecta ao servidor, chama métodos remotos e exibe os resultados.

## Servidor

O script `server.py` implementa o servidor RPC que abre uma conexão TCP na porta 5000 e aguarda requisições do cliente. Recebe chamadas de métodos, executa  e retorna o resultado ao cliente.

## RPC

O script `rpc.py` implementa as classes e métodos utilizados pelo cliente e servidor para fazer a comunicação de forma transparente.

## Execução

Para executar o projeto:

1. Execute o servidor: `python server.py`.
2. Execute o cliente: `python client.py`

O cliente irá se conectar ao servidor e chamar os métodos expostos.
O servidor ira executar os métodos e retornar os resultados.
