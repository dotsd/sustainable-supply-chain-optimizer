# Sustainable Supply Chain Optimizer

Phase 1 Foundation - Python MCP Server with AWS Bedrock Integration

## Quick Start

```bash
pip install -r requirements.txt
python mcp_server.py
```

## Test Data Generation

```bash
python test_mcp.py
```

## MCP Tools

- `generate_supply_chain_data` - Generate realistic supply chain data
- `analyze_suppliers` - Analyze supplier sustainability metrics

## AWS Integration

- **Bedrock Runtime**: Powers AI agents with Claude/Titan models
- **S3**: Data storage and retrieval
- **IAM**: Secure access management

## Phase 1 Complete ✅

- [x] MCP Server Structure
- [x] Agent Communication Protocol  
- [x] Data Generator Agent
- [x] Test with 20 suppliers, 30 routes, 15 products
- [x] Data quality validation

## Next: Phase 2 - Core Agents Implementation
# 🌱 Sustainable Supply Chain Optimizer

An AI-powered solution leveraging AWS Bedrock Agents to analyze and optimize supply chain sustainability across sourcing, logistics, inventory, and carbon accounting.

## 🎯 Overview

This solution provides comprehensive sustainability analysis through four specialized AI agents:
- **Sourcing Agent**: Analyzes supplier sustainability profiles and certifications
- **Logistics Agent**: Optimizes transportation routes for emission reduction  
- **Inventory Agent**: Generates waste reduction recommendations
- **Carbon Accounting Agent**: Calculates overall carbon footprint and benchmarking

## 🏗️ Architecture

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Bedrock       │    │   Lambda         │    │   Agent Core    │
│   Agent         │───▶│   Orchestrator   │───▶│   Coordinator   │
└─────────────────┘    └──────────────────┘    └─────────────────┘
                                                         │
                       ┌─────────────────────────────────┼─────────────────────────────────┐
                       │                                 │                                 │
                       ▼                                 ▼                                 ▼
              ┌─────────────────┐              ┌─────────────────┐              ┌─────────────────┐
              │ Sourcing Agent  │              │ Logistics Agent │              │ Inventory Agent │
              │ - Supplier      │              │ - Route         │              │ - Waste         │
              │   Analysis      │              │   Optimization  │              │   Reduction     │
              │ - Sustainability│              │ - Emission      │              │ - Stock         │
              │   Scoring       │              │   Calculation   │              │   Optimization  │
              └─────────────────┘              └─────────────────┘              └─────────────────┘
                       │                                 │                                 │
                       └─────────────────────────────────┼─────────────────────────────────┘
                                                         ▼
                                              ┌─────────────────┐
                                              │ Carbon          │
                                              │ Accounting      │
                                              │ Agent           │
                                              │ - Footprint     │
                                              │ - Benchmarking  │
                                              └─────────────────┘
```

## 🚀 Quick Start

### Prerequisites
- Python 3.9+
- AWS Account with Bedrock access
- AWS CLI configured

### Installation

1. **Clone and Setup**
```bash
cd sustainable-supply-chain-optimizer
pip install -r requirements.txt
```

2. **Deploy to AWS Bedrock**
```bash
# Update account details in deploy_agents_to_bedrock.py
python deploy_agents_to_bedrock.py
```

3. **Run Local API Server**
```bash
python api_endpoint.py
```

4. **Test the Solution**
```bash
python test_api.py
```

## 📋 Sample Usage

### Via Bedrock Agent (Natural Language)
```
"Analyze the sustainability of my supply chain with 5 suppliers, 
10 transportation routes, and 20 inventory items. Focus on carbon 
footprint reduction and waste minimization."
```

### Via API Endpoint
```bash
curl -X POST http://localhost:5000/api/sustainability/analyze \
  -H "Content-Type: application/json" \
  -d '{
    "supply_chain_data": {
      "suppliers": [...],
      "routes": [...], 
      "inventory": [...]
    }
  }'
```

## 🧪 Sample Test Prompts

### For Bedrock Agent Testing:

1. **Basic Analysis**
   ```
   "Please analyze my supply chain sustainability. I have 3 suppliers: 
   EcoTech (carbon footprint: 30 tons, ISO14001 certified), 
   GreenSupply (carbon footprint: 45 tons, no certifications), 
   and SustainableCorp (carbon footprint: 20 tons, FSC + ISO14001 certified)."
   ```

2. **Route Optimization**
   ```
   "Optimize my transportation routes for emissions. I have a 200km truck route 
   from Factory A to Warehouse B, and an 800km truck route from Supplier C to Factory A. 
   What are the best alternatives?"
   ```

3. **Inventory Waste Analysis**
   ```
   "Help reduce waste in my inventory. I have Widget A (500 units, 100/month demand, 
   180 days shelf life) and Component B (1200 units, 150/month demand, 365 days shelf life)."
   ```

4. **Complete Analysis**
   ```
   "Run a complete sustainability analysis on my supply chain including 
   supplier assessment, route optimization, inventory waste reduction, 
   and overall carbon footprint calculation."
   ```

## 📊 Output Examples

### Sustainability Score Breakdown
```json
{
  "overall_sustainability_score": 78.5,
  "sustainability_grade": "B",
  "total_carbon_footprint": 245.8,
  "footprint_breakdown": {
    "sourcing": 180.2,
    "logistics": 45.6, 
    "inventory_waste": 8.5,
    "operations": 11.5
  }
}
```

### Top Recommendations
```json
{
  "top_recommendations": [
    "Switch to rail transport for routes over 500km",
    "Implement supplier sustainability training program",
    "Reduce order quantity for Widget A by 30%",
    "Request carbon reduction plan from high-footprint suppliers"
  ]
}
```

## 🔧 Configuration

### AWS Resources Required
- **Bedrock Agent**: `sustainability-supply-chain-optimizer`
- **Lambda Function**: `sustainability-agents-orchestrator`
- **IAM Roles**: Bedrock execution role with Lambda invoke permissions

### Environment Variables
```bash
AWS_REGION=us-east-1
AWS_ACCOUNT_ID=your-account-id
BEDROCK_AGENT_ID=your-agent-id
```

## 📈 Key Features

### ✅ Sourcing Agent
- Supplier sustainability scoring (0-100)
- Certification tracking (ISO14001, FSC, etc.)
- Risk assessment (Low/Medium/High)
- Renewable energy usage analysis

### ✅ Logistics Agent  
- Multi-modal transport optimization
- Emission factor calculations
- Route consolidation recommendations
- Distance-based mode selection

### ✅ Inventory Agent
- Waste percentage calculation
- Expiry risk assessment
- Overstock identification
- FIFO implementation guidance

### ✅ Carbon Accounting Agent
- Complete footprint aggregation
- Category-wise breakdown
- Industry benchmarking
- Reduction opportunity identification

### ✅ Enhanced Orchestration (Phase 2 Step 2)
- **Agent Communication Flow**: Sequential execution with context sharing
- **Context Management**: Shared data store for cross-agent insights
- **Error Handling & Retry**: Resilient execution with automatic recovery
- **Result Validation**: Data flow integrity checks and validation
- **Execution Monitoring**: Detailed timing and performance metrics

## 🧪 Testing

### Run All Tests
```bash
# Test individual agents
python test_agents.py

# Test enhanced orchestration (Phase 2 Step 2)
python test_orchestration.py

# Test API endpoints
python test_api.py

# Test Bedrock integration
python deploy_agents_to_bedrock.py
```

### Phase 2 Step 2: Agent Orchestration Features
- **Context Passing**: Agents share results and context between executions
- **Error Handling**: Graceful failure handling with fallback mechanisms
- **Retry Logic**: Automatic retry for failed agent executions
- **Flow Control**: Sequential execution with dependency management
- **Result Aggregation**: Comprehensive result compilation with metadata

### API Endpoints
- `GET /health` - Health check
- `GET /api/sustainability/test` - Test with sample data
- `POST /api/sustainability/analyze` - Full analysis

## 📝 Data Format

### Input Schema
```json
{
  "suppliers": [
    {
      "id": "SUP001",
      "name": "Supplier Name", 
      "carbon_footprint": 25,
      "certifications": ["ISO14001"],
      "renewable_energy_percent": 60
    }
  ],
  "routes": [
    {
      "id": "RT001",
      "origin": "Location A",
      "destination": "Location B", 
      "distance_km": 250,
      "transport_mode": "truck"
    }
  ],
  "inventory": [
    {
      "id": "PRD001",
      "name": "Product Name",
      "current_stock": 500,
      "monthly_demand": 100,
      "shelf_life_days": 180
    }
  ]
}
```

## 🎯 Business Impact

- **30-40%** potential emission reduction through route optimization
- **20-60%** waste reduction through inventory optimization  
- **15-25%** supplier sustainability score improvement
- **Real-time** carbon footprint tracking and benchmarking

## 🔮 Future Enhancements

- Real-time data integration with ERP systems
- Machine learning for demand forecasting
- Blockchain for supply chain transparency
- IoT sensor integration for real-time monitoring
- Advanced visualization dashboard

## 📞 Support

For questions or issues:
1. Check the test files for usage examples
2. Review AWS Bedrock Agent logs
3. Validate input data format
4. Ensure proper AWS permissions

---

**Built for AI Hackathon - Sustainable Supply Chain Optimization**