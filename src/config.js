module.exports = {
  server: {
    port: process.env.PORT || 3000,
    host: process.env.HOST || 'localhost'
  },
  agents: {
    timeout: 30000, // 30 seconds
    maxRetries: 3
  },
  data: {
    defaultSuppliers: 20,
    defaultRoutes: 30,
    defaultProducts: 15
  },
  sustainability: {
    minScore: 60,
    maxScore: 100,
    targetScore: 80
  }
};