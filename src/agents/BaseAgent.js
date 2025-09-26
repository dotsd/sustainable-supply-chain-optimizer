class BaseAgent {
  constructor(name) {
    this.name = name;
    this.context = {};
  }

  async execute(parameters, sharedContext = {}) {
    this.context = { ...this.context, ...sharedContext };
    return await this.process(parameters);
  }

  async process(parameters) {
    throw new Error('Process method must be implemented by subclass');
  }

  log(message) {
    console.log(`[${this.name}] ${message}`);
  }
}

module.exports = BaseAgent;