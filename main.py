import grpc
from concurrent import futures

# Importa os módulos gerados pela compilação do dto.proto
import msf.schema.dto_pb2
import msf.schema.dto_pb2_grpc

# Importa os schemas Pydantic criados no arquivo dto.py
from msf.dto.dto import RequestDTO, ResponseDTO
from msf.validator import Validator
from service import Service

class MagmaServicer(msf.schema.dto_pb2_grpc.MagmaServiceServicer):

    def __init__(self):
        self.validator = Validator()
        self.service = Service()

    def ProcessAction(self, request, context):
        try:
            # Valida os dados vindos do gRPC transformando-os no schema RequestDTO do Pydantic
            valid_request = RequestDTO(
                request=request.request,
                transaction=request.transaction,
                action=request.action,
                payload=request.payload
            )
            
            # Valida a requisição usando o validator e obtém a spec instanciada e validada
            spec = self.validator.validate(valid_request)

            # Executa a ação usando o service, repassando o request e a spec validada
            self.service.execute(valid_request, spec=spec)
            
            # Caso tudo corra bem, cria a resposta de sucesso validada no schema
            valid_response = ResponseDTO(
                request=valid_request.request,
                transaction=valid_request.transaction,
                status="success",
                message="[Core/Runner] Action processed successfully."
            )
            
        except Exception as e:
            # Em caso de qualquer erro (inclusive de validação), constrói o ResponseDTO com erro
            valid_response = ResponseDTO(
                request=request.request,
                transaction=request.transaction,
                status="error",
                message=f"[Core/Runner] Error processing action: {str(e)}"
            )

        # Converte o Pydantic ResponseDTO de volta para a mensagem do Protobuf ResponseDTO e retorna
        return msf.schema.dto_pb2.ResponseDTO(
            request=valid_response.request,
            transaction=valid_response.transaction,
            status=valid_response.status,
            message=valid_response.message
        )

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    msf.schema.dto_pb2_grpc.add_MagmaServiceServicer_to_server(MagmaServicer(), server)
    server.add_insecure_port('[::]:50051')
    print("[Core/Runner] Magma gRPC server is running on port 50051...")
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    serve()