import uuid
import random
from datetime import datetime
from typing import Dict, Any, List
from .base_agent import BaseAgent

class DataGeneratorAgent(BaseAgent):
    def __init__(self):
        super().__init__("DataGeneratorAgent")
    
    async def process(self, parameters: Dict[str, Any]) -> Dict[str, Any]:
        suppliers = parameters.get('suppliers', 20)
        routes = parameters.get('routes', 30)
        products = parameters.get('products', 15)
        
        return {
            'suppliers': self.generate_suppliers(suppliers),
            'routes': self.generate_routes(routes),
            'products': self.generate_products(products),
            'timestamp': datetime.now().isoformat()
        }
    
    def generate_suppliers(self, count: int) -> List[Dict[str, Any]]:
        companies = ['GreenTech', 'EcoSupply', 'SustainCorp', 'CleanSource', 'BioMaterials']
        locations = ['USA', 'Germany', 'Japan', 'Canada', 'Sweden']
        
        return [{
            'id': str(uuid.uuid4()),
            'name': f"{companies[i % len(companies)]} {i // len(companies) + 1}",
            'location': locations[i % len(locations)],
            'sustainability_score': random.randint(60, 100),
            'cost': random.randint(25, 75),
            'certifications': self.get_random_certifications(),
            'carbon_footprint': random.randint(100, 600)
        } for i in range(count)]
    
    def generate_routes(self, count: int) -> List[Dict[str, Any]]:
        modes = ['truck', 'rail', 'ship', 'air']
        cities = ['New York', 'Los Angeles', 'Chicago', 'Houston', 'Phoenix']
        
        return [{
            'id': str(uuid.uuid4()),
            'origin': random.choice(cities),
            'destination': random.choice(cities),
            'mode': random.choice(modes),
            'distance': random.randint(100, 2100),
            'emissions_per_mile': self.get_emissions_by_mode(random.choice(modes)),
            'cost': random.randint(200, 1200)
        } for _ in range(count)]
    
    def generate_products(self, count: int) -> List[Dict[str, Any]]:
        categories = ['Electronics', 'Textiles', 'Food', 'Chemicals', 'Automotive']
        
        return [{
            'id': str(uuid.uuid4()),
            'name': f"Product {i + 1}",
            'category': categories[i % len(categories)],
            'current_stock': random.randint(100, 1000),
            'reorder_point': random.randint(50, 250),
            'waste_rate': random.uniform(0, 0.1),
            'holding_cost': random.randint(5, 25)
        } for i in range(count)]
    
    def get_random_certifications(self) -> List[str]:
        certs = ['ISO 14001', 'LEED', 'Energy Star', 'Fair Trade', 'Organic']
        return random.sample(certs, random.randint(1, 3))
    
    def get_emissions_by_mode(self, mode: str) -> float:
        emissions = {'truck': 0.4, 'rail': 0.1, 'ship': 0.05, 'air': 1.2}
        return emissions.get(mode, 0.4)