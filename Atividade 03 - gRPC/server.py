import grpc
from concurrent import futures
import voting_pb2
import voting_pb2_grpc

class VotingService(voting_pb2_grpc.VotingServiceServicer):
    def __init__(self):
        # Dicionário para armazenar os votos por candidato
        self.votes = {1: 0, 2: 0, 3: 0}  

        self.candidates = {
            1: "Maria Freitas", 
            2: "Pedro Motta ", 
            3: "José Barros"
        }

    def Vote(self, request, context):
        if request.candidate_id in self.votes:
            self.votes[request.candidate_id] += 1
            return voting_pb2.VoteResponse(message="Voto registrado com sucesso!")
        else:
            return voting_pb2.VoteResponse(message="ID do candidato inválido. Tente novamente.")

    def GetResults(self, request, context):
        results = [
            voting_pb2.CandidateResult(candidate_id=cid, votes=vote_count, name=self.candidates.get(cid, "Desconhecido"))
            for cid, vote_count in self.votes.items()
        ]
        return voting_pb2.ResultsResponse(results=results)
    
    def GetCandidates(self, request, context):
        # Retorna os candidatos disponíveis para o cliente
        candidates = [
            voting_pb2.Candidate(id=cid, name=name) 
            for cid, name in self.candidates.items()
        ]
        return voting_pb2.CandidateList(candidates=candidates)

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    voting_pb2_grpc.add_VotingServiceServicer_to_server(VotingService(), server)
    server.add_insecure_port('10.3.5.12:50051')
    server.start()
    print("Servidor gRPC iniciado na porta 50051.")
    server.wait_for_termination()

if __name__ == "__main__":
    serve()
