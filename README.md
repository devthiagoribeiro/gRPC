# gRPC Task Manager

Sistema de gerenciamento de tarefas cliente-servidor construído com **gRPC** e **Protocol Buffers**, desenvolvido para a disciplina de Sistemas Distribuídos. O projeto demonstra comunicação remota tipada entre serviços distribuídos, com servidor e clientes rodando em containers Docker isolados, cada um com seu próprio endereço IP.

### Integrantes:
 * Guilherme Emetério Santos Lima 
 * Thiago Roberto de Lima Ribeiro
 * João Emanuel Santos do Nascimento
 * Emmanuel de Souza Silva


## Funcionalidades

- **CriarTarefa** — cria uma nova tarefa com ID único (UUID)
- **ListarTarefas** — retorna todas as tarefas cadastradas
- **AtualizarTarefa** — atualiza os dados de uma tarefa existente pelo ID
- **DeletarTarefa** — remove uma tarefa pelo ID

## Como executar

### 1. Subir o ambiente

```bash
docker compose build
docker compose up -d
```

Isso cria três containers, confirme que todos subiram corretamente:

```bash
docker compose ps
```

### 2. Usar os clientes

Cada cliente expõe um menu interativo em linha de comando. Para acessá-lo:

```bash
docker exec -it grpc_client1 python client.py
```

Em outro terminal, para o segundo cliente:

```bash
docker exec -it grpc_client2 python client.py
```

### 3. Encerrar o ambiente

```bash
docker compose down
```

## Regenerando o código a partir do `.proto`

Caso `protos/tasks.proto` seja alterado, regenere os arquivos de código antes de reconstruir as imagens:

```bash
python -m grpc_tools.protoc -I./protos --python_out=./server --grpc_python_out=./server ./protos/tasks.proto
python -m grpc_tools.protoc -I./protos --python_out=./client --grpc_python_out=./client ./protos/tasks.proto
```
