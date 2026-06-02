import grpc
import msf.schema.dto_pb2 as dto_pb2
import msf.schema.dto_pb2_grpc as dto_pb2_grpc

class GrpcClient:
    
    def __init__(self, port="50051"):
        self.port = port

    def send(self, message, url):
        # Se a url informada não contiver porta, adicionamos a porta fixa
        target_url = url if ":" in url else f"{url}:{self.port}"
        
        # Cria um canal de comunicação não seguro com o servidor gRPC alvo
        with grpc.insecure_channel(target_url) as channel:
            # Instancia o cliente (stub) do serviço MagmaService
            stub = dto_pb2_grpc.MagmaServiceStub(channel)
            
            # Prepara a requisição convertendo para a mensagem Protobuf RequestDTO esperada
            if isinstance(message, dict):
                grpc_request = dto_pb2.RequestDTO(**message)
            elif isinstance(message, dto_pb2.RequestDTO):
                grpc_request = message
            else:
                # Tenta extrair os atributos, caso seja um objeto Pydantic ou similar
                grpc_request = dto_pb2.RequestDTO(
                    request=getattr(message, 'request', ''),
                    transaction=getattr(message, 'transaction', ''),
                    action=getattr(message, 'action', ''),
                    payload=getattr(message, 'payload', '')
                )
                
            # Envia a requisição e retorna o ResponseDTO do protobuf
            return stub.ProcessAction(grpc_request)