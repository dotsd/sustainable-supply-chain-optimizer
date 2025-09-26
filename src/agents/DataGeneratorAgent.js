const { v4: uuidv4 } = require('uuid');
const BaseAgent = require('./BaseAgent');

class DataGeneratorAgent extends BaseAgent {
  constructor() {
    super('DataGeneratorAgent');
  }

  async process(parameters = {}) {
    const { suppliers = 20, routes = 30, products = 15 } = parameters;
    
    return {
      suppliers: this.generateSuppliers(suppliers),
      routes: this.generateRoutes(routes),
      products: this.generateProducts(products),
      timestamp: new Date().toISOString()
    };
  }

  generateSuppliers(count) {
    const companies = ['GreenTech', 'EcoSupply', 'SustainCorp', 'CleanSource', 'BioMaterials', 'RenewCo', 'EarthFirst', 'GreenLogistics', 'EcoFriendly', 'SolarSupply'];
    const locations = ['USA', 'Germany', 'Japan', 'Canada', 'Sweden', 'Netherlands', 'Denmark', 'Norway', 'Switzerland', 'Finland'];
    
    return Array.from({ length: count }, (_, i) => ({
      id: uuidv4(),
      name: `${companies[i % companies.length]} ${Math.floor(i / companies.length) + 1}`,
      location: locations[i % locations.length],
      sustainabilityScore: Math.floor(Math.random() * 40) + 60, // 60-100
      cost: Math.floor(Math.random() * 50) + 25, // $25-75
      certifications: this.getRandomCertifications(),
      carbonFootprint: Math.floor(Math.random() * 500) + 100 // 100-600 kg CO2
    }));
  }

  generateRoutes(count) {
    const modes = ['truck', 'rail', 'ship', 'air'];
    const cities = ['New York', 'Los Angeles', 'Chicago', 'Houston', 'Phoenix', 'Philadelphia', 'San Antonio', 'San Diego', 'Dallas', 'San Jose'];
    
    return Array.from({ length: count }, () => ({
      id: uuidv4(),
      origin: cities[Math.floor(Math.random() * cities.length)],
      destination: cities[Math.floor(Math.random() * cities.length)],
      mode: modes[Math.floor(Math.random() * modes.length)],
      distance: Math.floor(Math.random() * 2000) + 100, // 100-2100 miles
      emissionsPerMile: this.getEmissionsByMode(modes[Math.floor(Math.random() * modes.length)]),
      cost: Math.floor(Math.random() * 1000) + 200 // $200-1200
    }));
  }

  generateProducts(count) {
    const categories = ['Electronics', 'Textiles', 'Food', 'Chemicals', 'Automotive', 'Furniture', 'Packaging', 'Medical'];
    
    return Array.from({ length: count }, (_, i) => ({
      id: uuidv4(),
      name: `Product ${i + 1}`,
      category: categories[i % categories.length],
      currentStock: Math.floor(Math.random() * 1000) + 100,
      reorderPoint: Math.floor(Math.random() * 200) + 50,
      wasteRate: Math.random() * 0.1, // 0-10%
      holdingCost: Math.floor(Math.random() * 20) + 5 // $5-25 per unit
    }));
  }

  getRandomCertifications() {
    const certs = ['ISO 14001', 'LEED', 'Energy Star', 'Fair Trade', 'Organic'];
    const count = Math.floor(Math.random() * 3) + 1;
    return Array.from({ length: count }, () => certs[Math.floor(Math.random() * certs.length)]);
  }

  getEmissionsByMode(mode) {
    const emissions = {
      truck: 0.4, // kg CO2 per mile
      rail: 0.1,
      ship: 0.05,
      air: 1.2
    };
    return emissions[mode] || 0.4;
  }
}

module.exports = DataGeneratorAgent;