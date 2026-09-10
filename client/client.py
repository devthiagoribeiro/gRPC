import grpc
import tasks_pb2
import tasks_pb2_grpc
import os

def main():
    server_address = os.environ.get('SERVER_ADDRESS', 'localhost:50051')
    channel = grpc.insecure_channel(server_address)
    stub = tasks_pb2_grpc.TaskServiceStub(channel)

    while True:
        entrada = int(input("""
1 - Criar tarefa
2 - Atualizar tarefa
3 - Excluir tarefa
4 - Listar tarefas
5 - Sair

Qual operação deseja realizar? """))

        match entrada:
                case 1:
                    title = input("Título: ")
                    description = input("Descrição: ")
                    req = tasks_pb2.CreateTaskRequest(
                        title=title, 
                        description=description
                    )
                    resp = stub.CreateTask(req)
                    print(resp)
                case 2:
                    taskId = input("ID tarefa: ")
                    title = input("Titulo: ")
                    description = input("Descrição: ")
                    req = tasks_pb2.UpdateTaskRequest(
                        uuid = taskId,
                        title=title,
                        description=description
                    )
                    resp = stub.UpdateTask(req)
                    print(resp)
        
                case 3:
                    taskId = input("ID tarefa: ")
                    req = tasks_pb2.DeleteTaskRequest(
                        uuid = taskId
                    )
                    resp = stub.DeleteTask(req)
                    print(resp)

                case 4:
                    print("==== TAREFAS ====\n")
                    tasks = stub.ListTasks(tasks_pb2.ListTasksRequest())
                    for task in tasks:
                        print(task)

                case 5:
                    print("Encerrando...")
                    break
        
                case _:
                    print("Opção inválida.")

    
if __name__ == "__main__":
    main()