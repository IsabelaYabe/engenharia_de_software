// databaseClient.js

// Definir a URL base do servidor Flask
const baseUrl = 'http://localhost:8000'; 

// Importar a classe DatabaseManagerClient
const DatabaseManagerClient = require('./DatabaseManagerClient');

// Criar a instância única do DatabaseManagerClient
const databaseClientInstance = new DatabaseManagerClient(baseUrl);

// Exportar a instância para uso em outros arquivos
module.exports = databaseClientInstance;
