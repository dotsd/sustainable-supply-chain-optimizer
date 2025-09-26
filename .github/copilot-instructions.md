# AI Coding Agent Instructions - Sustainable Supply Chain Optimizer

## Project Overview
This is a **Sustainable Supply Chain Optimizer** built for the AWS Agentic AI Hackathon. The system uses multiple AI agents to help businesses optimize their supply chains for sustainability while maintaining operational efficiency. The goal is to analyze supply chain data, identify carbon hotspots, and suggest actionable optimizations.

## Architecture & Components
Multi-agent system with orchestrated AI agents powered by AWS Strands and AgentCore:

```
                      ┌───────────────────┐
                      │   AgentCore       │
                      │  Orchestrator     │
                      └─────────┬─────────┘
                                │
           ┌──────────┬─────────┼─────────┬──────────┐
           ▼          ▼         ▼         ▼          ▼
┌───────────────┐ ┌─────────┐ ┌───────┐ ┌───────┐ ┌───────────────┐
│Sourcing Agent │ │Logistics│ │Invent-│ │Carbon │ │Recommendation │
│               │ │ Agent   │ │ory    │ │Account│ │     Agent     │
│               │ │         │ │Agent  │ │Agent  │ │               │
└───────────────┘ └─────────┘ └───────┘ └───────┘ └───────────────┘
```

### Core Agents
- **Sourcing Agent**: Evaluates suppliers based on environmental metrics and sustainability scores
- **Logistics Agent**: Optimizes transportation routes to minimize emissions and costs
- **Inventory Agent**: Predicts optimal inventory levels to reduce waste
- **Carbon Accounting Agent**: Calculates environmental impact across supply chain
- **Recommendation Agent**: Synthesizes insights into actionable business recommendations

## Development Workflows

### 3-Hour Hackathon Sprint Plan so the plan
**Hour 1: Setup & Data Preparation**
- Initialize project structure with agent directories
- Create mock datasets: supplier data, transportation routes, inventory levels
- Define agent prompts and interaction patterns

**Hour 2: Agent Implementation**
- Implement individual agents using AWS Strands
- Configure AgentCore for agent orchestration
- Build basic web dashboard interface

**Hour 3: Integration & Demo**
- Connect all agents through orchestrator
- Deploy solution with QR code demo access
- Prepare business impact pitch

### Key Commands
- Agent deployment: Use AWS Strands CLI for agent registration
- Dashboard: Simple web interface for hackathon demo
- Mock data: JSON files simulating real supply chain data

## Project-Specific Conventions

### Code Organization
```
/agents/              # Individual agent implementations
  /sourcing/         # Supplier evaluation agent
  /logistics/        # Route optimization agent
  /inventory/        # Inventory management agent
  /carbon/           # Carbon accounting agent
  /recommendation/   # Synthesis and recommendations
/orchestrator/        # AgentCore configuration
/dashboard/          # Web interface
/data/              # Mock datasets
  suppliers.json
  routes.json
  inventory.json
```

### Agent Naming Conventions
- Agent classes: `SourcingAgent`, `LogisticsAgent`, etc.
- Agent prompts: `agent_prompt_sourcing.txt`
- Data models: `SupplierData`, `RouteOptimization`, `CarbonImpact`

### Mock Data Structure
- **Suppliers**: sustainability scores, locations, costs, certifications
- **Transportation**: routes, emissions per mile, transportation modes
- **Inventory**: current levels, waste metrics, holding costs
- **Carbon**: emission factors, baseline measurements, reduction targets

## Integration Points

### AWS Services
- **AWS Strands**: Powers individual specialized agents
- **AgentCore**: Orchestrates communication between agents
- **Amazon Q Developer**: Assists with dashboard and analytics development

### Agent Communication Patterns
- Agents communicate through AgentCore orchestrator
- Data flows: Raw data → Individual agents → Orchestrator → Recommendations
- Each agent produces structured outputs for the next stage

## Key Files & Directories
*To be updated as project structure develops*

## Domain-Specific Patterns

### Supply Chain Concepts
- **Inventory Management**: Track stock levels, reorder points, safety stock
- **Demand Forecasting**: Implement predictive models for demand planning
- **Route Optimization**: Optimize transportation and logistics routes
- **Supplier Management**: Handle supplier relationships and performance metrics
- **Cost Optimization**: Balance service levels with operational costs

### Optimization Algorithms
- Document algorithm choices and their trade-offs
- Include performance benchmarks for optimization runs
- Maintain clear separation between heuristic and exact optimization methods

## Security Considerations
- Protect sensitive supply chain data (pricing, supplier contracts)
- Implement proper authentication for API access
- Follow AWS security best practices

---
*This file will be updated as the project evolves. Please contribute improvements based on implemented patterns and workflows.*