const DataGeneratorAgent = require('./agents/DataGeneratorAgent');

async function testDataGeneration() {
  console.log('Testing Data Generator Agent...\n');
  
  const agent = new DataGeneratorAgent();
  const result = await agent.execute({
    suppliers: 20,
    routes: 30,
    products: 15
  });

  console.log('Generated Data Summary:');
  console.log(`- Suppliers: ${result.suppliers.length}`);
  console.log(`- Routes: ${result.routes.length}`);
  console.log(`- Products: ${result.products.length}`);
  
  console.log('\nSample Supplier:');
  console.log(JSON.stringify(result.suppliers[0], null, 2));
  
  console.log('\nSample Route:');
  console.log(JSON.stringify(result.routes[0], null, 2));
  
  console.log('\nSample Product:');
  console.log(JSON.stringify(result.products[0], null, 2));

  // Validate data quality
  const avgSustainability = result.suppliers.reduce((sum, s) => sum + s.sustainabilityScore, 0) / result.suppliers.length;
  console.log(`\nData Quality Check:`);
  console.log(`- Average Sustainability Score: ${avgSustainability.toFixed(1)}`);
  console.log(`- All suppliers have certifications: ${result.suppliers.every(s => s.certifications.length > 0)}`);
  console.log(`- All routes have valid emissions: ${result.routes.every(r => r.emissionsPerMile > 0)}`);
}

testDataGeneration().catch(console.error);