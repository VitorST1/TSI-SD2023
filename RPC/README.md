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

## Desenvolvimento

### Semana 1

Implementado o RPC e operações básicas.

### Semana 2

Implementados métodos para verificar se um ou mais números são primos e printar números primos em um range.
Adicionado também um método para printar números primos utilizando multiprocessamento, printando o tempo levado entre as execuções sequencial e em paralelo.

### Semana 3

Implementado cache em memória no cliente para armazenar resultados das chamadas de métodos remotos anteriormente realizadas. Desta forma, se um mesmo método for chamado várias vezes com os mesmos parâmetros, o resultado será retornado do cache localmente no cliente em vez de fazer nova requisição ao servidor.

### Semana 4

Implementada a classe Cache, para lidar com toda a lógica de cache no cliente. Agora, o cache é armazenado também em disco. Desta forma, os resultados são persistidos entre execuções do cliente.

### Semana 5

Refatoração no envio dos dados do servidor e recebimento pelo cliente. Agora os dados são transmitidos utilizando JSON.  
Implementada operação `last_news_if_barbacena` para coletar o título de um número definido de notícias do site do Campus Barbacena utilizando multithreading.
