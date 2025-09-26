#!/usr/bin/env python3
import asyncio
import json
from typing import Any, Dict, List
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent
import boto3
from agents.data_generator import DataGeneratorAgent
from agents.agent_core import AgentCore

# Initialize MCP Server
server = Server("supply-chain-optimizer")

# AWS Bedrock client for agent interactions
bedrock = boto3.client('bedrock-runtime', region_name='us-east-1')

# Agent registry with Phase 2 integration
agents = {
    'data_generator': DataGeneratorAgent(),
    'agent_core': AgentCore()
}

@server.list_tools()
async def list_tools() -> List[Tool]:
    return [
        Tool(
            name="generate_supply_chain_data",
            description="Generate realistic supply chain data with suppliers, routes, and products",
            inputSchema={
                "type": "object",
                "properties": {
                    "suppliers": {"type": "integer", "default": 20},
                    "routes": {"type": "integer", "default": 30},
                    "products": {"type": "integer", "default": 15}
                }
            }
        ),
        Tool(
            name="analyze_suppliers",
            description="Analyze supplier sustainability metrics",
            inputSchema={
                "type": "object",
                "properties": {
                    "data": {"type": "object"}
                }
            }
        ),
        Tool(
            name="orchestrate_sustainability_analysis",
            description="Run complete sustainability analysis with all agents",
            inputSchema={
                "type": "object",
                "properties": {
                    "supply_chain_data": {"type": "object"}
                }
            }
        )
    ]

@server.call_tool()
async def call_tool(name: str, arguments: Dict[str, Any]) -> List[TextContent]:
    if name == "generate_supply_chain_data":
        agent = agents['data_generator']
        result = await agent.execute(arguments)
        return [TextContent(type="text", text=json.dumps(result, indent=2))]
    
    elif name == "analyze_suppliers":
        agent_core = agents['agent_core']
        result = agent_core.orchestrate_sustainability_analysis(arguments.get('data', {}))
        return [TextContent(type="text", text=json.dumps(result, indent=2))]
    
    elif name == "orchestrate_sustainability_analysis":
        agent_core = agents['agent_core']
        result = agent_core.orchestrate_sustainability_analysis(arguments.get('supply_chain_data', {}))
        return [TextContent(type="text", text=json.dumps(result, indent=2))]
    
    raise ValueError(f"Unknown tool: {name}")

async def main():
    async with stdio_server() as (read_stream, write_stream):
        await server.run(read_stream, write_stream, server.create_initialization_options())

if __name__ == "__main__":
    asyncio.run(main())