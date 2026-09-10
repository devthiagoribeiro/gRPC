# gRPC Task Manager

Sistema de gerenciamento de tarefas cliente-servidor construído com **gRPC** e **Protocol Buffers**, desenvolvido para a disciplina de Sistemas Distribuídos. O projeto demonstra comunicação remota tipada entre serviços distribuídos, com servidor e clientes rodando em containers Docker isolados, cada um com seu próprio endereço IP.

## Funcionalidades

- **CriarTarefa** — cria uma nova tarefa com ID único (UUID)
- **ListarTarefas** — retorna todas as tarefas cadastradas
- **AtualizarTarefa** — atualiza os dados de uma tarefa existente pelo ID
- **DeletarTarefa** — remove uma tarefa pelo ID

## Tecnologias

- Python 3.11
- [gRPC](https://grpc.io/) / [grpcio-tools](https://pypi.org/project/grpcio-tools/)
- Protocol Buffers (proto3)
- Docker + Docker Compose

## Estrutura do projeto

```
gRPC/
├── protos/
│   └── tasks.proto          
├── server/
│   ├── server.py             
│   ├── tasks_pb2.py          
│   ├── tasks_pb2_grpc.py     
│   ├── requirements.txt
│   └── Dockerfile
├── client/
│   ├── client.py            
│   ├── tasks_pb2.py
│   ├── tasks_pb2_grpc.py
│   ├── requirements.txt
│   └── Dockerfile
├── docker-compose.yml
└── README.md
```

## Pré-requisitos

- [Docker](https://www.docker.com/products/docker-desktop/) e Docker Compose instalados e em execução
- Python 3.11+ (opcional — apenas necessário caso queira regenerar o código a partir do `.proto`)

## Como executar

### 1. Clonar o repositório

```bash
git clone https://github.com/devthiagoribeiro/gRPC.git
cd gRPC
```

### 2. Subir o ambiente

```bash
docker compose build
docker compose up -d
```

Isso cria três containers:

| Container | Papel |
|---|---|
| `grpc_server` | Servidor gRPC, escutando na porta `50051` |
| `grpc_client1` | Primeiro cliente de linha de comando |
| `grpc_client2` | Segundo cliente de linha de comando |

Confirme que todos subiram corretamente:

```bash
docker compose ps
```

### 3. Usar os clientes

Cada cliente expõe um menu interativo em linha de comando. Para acessá-lo:

```bash
docker exec -it grpc_client1 python client.py
```

Em outro terminal, para o segundo cliente:

```bash
docker exec -it grpc_client2 python client.py
```

Como os dois clientes se conectam ao mesmo servidor central, uma tarefa criada em um deles aparece imediatamente ao listar tarefas no outro.

### 4. Encerrar o ambiente

```bash
docker compose down
```

## Regenerando o código a partir do `.proto`

Caso `protos/tasks.proto` seja alterado, regenere os arquivos de código antes de reconstruir as imagens:

```bash
python -m grpc_tools.protoc -I./protos --python_out=./server --grpc_python_out=./server ./protos/tasks.proto
python -m grpc_tools.protoc -I./protos --python_out=./client --grpc_python_out=./client ./protos/tasks.proto
```

## Rede e IPs

O `docker-compose.yml` define uma rede Docker dedicada (`grpc_net`, sub-rede `172.28.0.0/16`) com IPs fixos para cada serviço, simulando servidor e clientes em máquinas distintas. Para conferir os IPs atribuídos:

```bash
docker network inspect grpc_grpc_net
```

## Solução de problemas comuns

| Sintoma | Causa provável | Solução |
|---|---|---|
| `error during connect ... dockerDesktopLinuxEngine` | Docker Desktop não está em execução | Abrir o Docker Desktop e aguardar o engine iniciar |
| `ModuleNotFoundError` ao rodar o cliente/servidor | Import com caminho incorreto | Usar import direto pelo nome do módulo (`import tasks_pb2`) |
| `requirements.txt not found` durante o build | Arquivo fora do contexto de build da pasta correspondente | Garantir que `requirements.txt` esteja dentro de `server/` e `client/` |
| Container do cliente aparece como "Exited" | Exceção não tratada ao ler uma entrada inválida do usuário | Adicionar tratamento de erro na leitura do menu; religar com `docker compose start` |
| `docker network inspect` retorna "network not found" | Nome da rede tem prefixo do nome da pasta do projeto | Rodar `docker network ls` para conferir o nome exato |

