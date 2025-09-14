import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))
import grpc
from concurrent import futures
import matrix_pb2
import matrix_pb2_grpc
from Utils import Utils



class MatrixServiceServicer(matrix_pb2_grpc.MatrixServiceServicer):
    def Multiply(self, request, context):
        try:
            peer = context.peer()
            print(f"Received request from: {peer}")

            line = list(request.line)
            column = list(request.column)

            if len(line) != len(column):
                return matrix_pb2.Result(status="error", message="incompatible sizes between line and column")
            
            result = Utils.scalarMultiply(line, column)
            return matrix_pb2.Result(status="ok", value=result)

        except Exception as e:
            return matrix_pb2.Result(status="error", message=str(e))
    
def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    matrix_pb2_grpc.add_MatrixServiceServicer_to_server(MatrixServiceServicer(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    print("gRPC server started on port 50051")
    server.wait_for_termination()


if __name__ == '__main__':
    serve()
