const DataGeneratorAgent = require('./DataGeneratorAgent');

// Register agents
const { agents } = require('../server');

// Initialize and register Data Generator Agent
const dataGenerator = new DataGeneratorAgent();
agents.set('generateSupplyChainData', dataGenerator);

console.log('Agents registered:', Array.from(agents.keys()));

module.exports = {
  DataGeneratorAgent
};