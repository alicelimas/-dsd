const soap = require('soap');
const readline = require('readline');

const rl = readline.createInterface({
    input: process.stdin,
    output: process.stdout
});

const url = 'http://10.3.5.12:5002/?wsdl';

soap.createClient(url, (err, client) => {
    if (err) throw err;

    console.log('Bem-vindo ao Calculador de Calorias!');
    console.log('Digite os dados da atividade ou "sair" para encerrar.\n');

    let totalCalorias = 0; // Variável pra acumular o total de calorias

    function perguntarDados() {
        rl.question('Tipo de atividade (ex.: corrida, musculacao, natacao, futebol, caminhada): ', (tipo) => {
            if (tipo.toLowerCase() === 'sair') {
                console.log(`\nTotal de calorias gastas: ${totalCalorias.toFixed(2)} kcal`);
                rl.close();
                return;
            }

            rl.question('Duração (minutos): ', (duracao) => {
                rl.question('Intensidade (leve, moderada, alta): ', (intensidade) => {
                    client.calcular_calorias({
                        tipo: tipo,
                        duracao: parseInt(duracao),
                        intensidade: intensidade
                    }, (err, result) => {
                        if (err) {
                            console.log('Erro:', err.message);
                        } else {
                            const calorias = result.calcular_caloriasResult;
                            totalCalorias += calorias; 
                            console.log(`\nCalorias gastas: ${calorias.toFixed(2)} kcal`);
                            
                        }
                        perguntarDados(); 
                    });
                });
            });
        });
    }

    perguntarDados();
});

rl.on('close', () => {
    console.log('Calculador encerrado.');
    process.exit(0);
});