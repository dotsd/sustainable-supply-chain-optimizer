# 🏗️ Complete System Architecture

## Architecture Overview

The Sustainable Supply Chain Optimizer follows a layered architecture pattern with clear separation of concerns:

```
┌─────────────────────────────────────────────────────────────────┐
│                    User Interface Layer                         │
│  ┌─────────────────┐    ┌─────────────────────────────────────┐ │
│  │  Web Dashboard  │───▶│      QR Code Demo Access           │ │
│  └─────────────────┘    └─────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────┘
                                    │
┌─────────────────────────────────────────────────────────────────┐
│                    API Gateway Layer                            │
│  ┌─────────────────┐    ┌─────────────────────────────────────┐ │
│  │ Flask API Server│───▶│     MCP Server Interface           │ │
│  └─────────────────┘    └─────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────┘
                                    │
┌─────────────────────────────────────────────────────────────────┐
│                     MCP Server Layer                            │
│  ┌─────────────────┐  ┌─────────────┐  ┌─────────────────────┐  │
│  │Data Generation  │  │Agent Orch.  │  │  Analysis Tool      │  │
│  │     Tool        │  │    Tool     │  │                     │  │
│  └─────────────────┘  └─────────────┘  └─────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
                                    │
┌─────────────────────────────────────────────────────────────────┐
│              Agent Network (Strands/AgentCore)                  │
│  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐ ┌─────────────┐ │
│  │   Data      │ │  Sourcing   │ │ Logistics   │ │ Inventory   │ │
│  │ Generator   │ │   Agent     │ │   Agent     │ │   Agent     │ │
│  └─────────────┘ └─────────────┘ └─────────────┘ └─────────────┘ │
│                  ┌─────────────┐                                 │
│                  │   Carbon    │                                 │
│                  │ Accounting  │                                 │
│                  │   Agent     │                                 │
│                  └─────────────┘                                 │
└─────────────────────────────────────────────────────────────────┘
                                    │
┌─────────────────────────────────────────────────────────────────┐
│                      AWS Services                               │
│  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐ ┌─────────────┐ │
│  │   Strands   │ │ AgentCore   │ │Amazon Q Dev │ │    Kiro     │ │
│  │   Agents    │ │             │ │             │ │             │ │
│  └─────────────┘ └─────────────┘ └─────────────┘ └─────────────┘ │
└─────────────────────────────────────────────────────────────────┘
```

## Layer Responsibilities

### 1. User Interface Layer
- **Web Dashboard**: Interactive sustainability metrics and charts
- **QR Code Access**: Mobile-friendly demo access for presentations

### 2. API Gateway Layer  
- **Flask API Server**: RESTful endpoints for dashboard integration
- **MCP Server Interface**: Model Context Protocol compliance

### 3. MCP Server Layer
- **Data Generation Tool**: Creates realistic supply chain datasets
- **Agent Orchestration Tool**: Coordinates multi-agent workflows
- **Analysis Tool**: Processes and validates results

### 4. Agent Network
- **Data Generator Agent**: Strands-powered realistic data creation
- **Sourcing Agent**: Supplier sustainability analysis
- **Logistics Agent**: Route optimization for emissions
- **Inventory Agent**: Waste reduction recommendations  
- **Carbon Accounting Agent**: Overall footprint calculation

### 5. AWS Services Integration
- **Strands Agents**: Enhanced AI reasoning and natural language
- **AgentCore**: Agent orchestration and context management
- **Amazon Q Developer**: Development assistance and code generation
- **Kiro**: Data pipeline processing and analytics

## Data Flow

```
User Request → Flask API → MCP Server → Agent Orchestrator →
[Data Gen → Sourcing → Logistics → Inventory → Carbon] →
Results Aggregation → Dashboard Visualization
```

## Key Design Principles

1. **Separation of Concerns**: Each layer has distinct responsibilities
2. **Scalability**: Modular agent architecture supports easy expansion
3. **Resilience**: Fallback mechanisms and error handling at each layer
4. **Interoperability**: MCP protocol ensures standard agent communication
5. **Enhanced AI**: Strands integration provides superior reasoning capabilities

## Deployment Architecture

- **Local Development**: All layers run on localhost
- **Cloud Deployment**: Vercel/Netlify for UI, AWS for agents
- **Mobile Access**: QR codes enable instant demo sharing