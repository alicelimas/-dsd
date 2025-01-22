const grpc = require("@grpc/grpc-js");
const protoLoader = require("@grpc/proto-loader");

// Carregar o arquivo .proto
const PROTO_PATH = "./voting.proto";
const packageDefinition = protoLoader.loadSync(PROTO_PATH, {});
const votingProto = grpc.loadPackageDefinition(packageDefinition).VotingService;

// Criar cliente
const client = new votingProto("10.3.5.12:50051", grpc.credentials.createInsecure());

function vote(candidateId) {
  client.Vote({ candidateId: candidateId }, (error, response) => {
    if (error) {
      console.error("Erro ao votar:", error.message);
      return;
    }
    console.log(response.message);

    menu();
  });
}

function getResults() {
  client.GetResults({}, (error, response) => {
    if (error) {
      console.error("Erro ao obter resultados:", error.message);
      return;
    }
    
    console.log("Resultados:");
    response.results.forEach((result) => {
        console.log(`Candidato(a) ${result.name} - ${result.candidateId}: ${result.votes !== undefined ? result.votes : 0} votos`);
    });

    menu();
  });
}

function showCandidates() {
    client.GetCandidates({}, (error, response) => {
      if (error) {
        console.error("Erro ao obter candidatos:", error.message);
        return;
      }
  
      console.log("\nCandidatos disponíveis:");
      response.candidates.forEach((candidate) => {
        console.log(`${candidate.id}: ${candidate.name}`);
      });
  
      readline.question("Digite o ID do candidato para votar: ", (id) => { // usuário informa o candidato votado
        const candidateId = parseInt(id, 10);
        if (isNaN(candidateId) || candidateId <= 0) {
          console.log("Por favor, insira um ID de candidato válido.");
          menu();  // Reexibe o menu em caso de erro
          return;
        }
        vote(candidateId);
      });
    });
  }

const readline = require("readline").createInterface({
  input: process.stdin,
  output: process.stdout,
});

function menu() {
  console.log("\n1. Votar em um candidato");
  console.log("2. Ver resultados");
  console.log("3. Sair");
  readline.question("Escolha uma opção: ", (option) => {
    switch (option) {
      case "1":
          showCandidates();
          break;
      case "2":
        getResults();
        break;
      case "3":
        console.log("Encerrando cliente...");
        readline.close();
        break;
      default:
        console.log("Opção inválida.");
        menu();
    }
  });
}

menu();
