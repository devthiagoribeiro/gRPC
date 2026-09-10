from concurrent import futures
import grpc

import tasks_pb2
import tasks_pb2_grpc
import uuid

tasksMemory = []

class TaskService(tasks_pb2_grpc.TaskServiceServicer):

    def CreateTask(self, request, context):

        newTask = {
                    "uuid": str(uuid.uuid4()),
                    "title": request.title,
                    "description": request.description,
                    "status": 1
                }
                
        tasksMemory.append(newTask)
        return tasks_pb2.CreateTaskResponse(task=tasks_pb2.Task(**newTask))
    
    def ListTasks(self, request, context):
        for task in tasksMemory:
            yield tasks_pb2.ListTasksResponse(task=tasks_pb2.Task(
                uuid=task['uuid'],
                title=task["title"],
                description=task["description"],
                status=task["status"]
            ))
    
    def UpdateTask(self, request, context):
        for task in tasksMemory:
            if task['uuid'] == request.uuid:
                target = task
                target['title'] = request.title
                target['description'] = request.description
                target['status'] = request.status
                return tasks_pb2.UpdateTaskResponse(task=tasks_pb2.Task(**target))
                
        return tasks_pb2.UpdateTaskResponse(task=None)

    def DeleteTask(self, request, context):
        for i, task in enumerate(tasksMemory):
            if task['uuid'] == request.uuid:
                tasksMemory.pop(i)
        return tasks_pb2.DeleteTaskResponse()


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    tasks_pb2_grpc.add_TaskServiceServicer_to_server(
        TaskService(), server
    )
    server.add_insecure_port("[::]:50051")
    server.start()
    server.wait_for_termination()

if __name__ == "__main__":
    serve()