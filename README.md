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