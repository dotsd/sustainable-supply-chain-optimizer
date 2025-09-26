import boto3
import json
import os
from typing import Dict, Any, List
import math
from strands_client import StrandsWrapper

class LogisticsAgent:
    def __init__(self):
        self.bedrock_client = boto3.client('bedrock-runtime')
        self.strands = StrandsWrapper(api_key=os.getenv('STRANDS_API_KEY'))
        
    def optimize_routes_for_emissions(self, routes: List[Dict]) -> Dict[str, Any]:
        """Optimize transportation routes for emission reduction"""
        optimized_routes = []
        
        for route in routes:
            emissions = self._calculate_route_emissions(route)
            optimization = self._optimize_single_route(route, emissions)
            
            optimized_routes.append({
                'route_id': route.get('id'),
                'origin': route.get('origin'),
                'destination': route.get('destination'),
                'distance_km': route.get('distance_km', 0),
                'current_emissions': emissions['current'],
                'optimized_emissions': emissions['optimized'],
                'emission_reduction': emissions['reduction_percent'],
                'transport_mode': optimization['recommended_mode'],
                'recommendations': optimization['recommendations']
            })
        
        return {
            'agent': 'logistics',
            'optimized_routes': optimized_routes,
            'total_emission_reduction': sum(r['emission_reduction'] for r in optimized_routes) / len(optimized_routes),
            'best_routes': sorted(optimized_routes, key=lambda x: x['emission_reduction'], reverse=True)[:5]
        }
    
    def _calculate_route_emissions(self, route: Dict) -> Dict[str, float]:
        """Calculate emissions for different transport modes"""
        distance = route.get('distance_km', 0)
        current_mode = route.get('transport_mode', 'truck')
        
        # Emission factors (kg CO2 per km per ton)
        emission_factors = {
            'truck': 0.62,
            'rail': 0.14,
            'ship': 0.10,
            'air': 2.1
        }
        
        current_emissions = distance * emission_factors.get(current_mode, 0.62)
        
        # Find optimal mode
        optimal_mode = min(emission_factors.keys(), key=lambda x: emission_factors[x])
        optimal_emissions = distance * emission_factors[optimal_mode]
        
        reduction_percent = ((current_emissions - optimal_emissions) / current_emissions) * 100 if current_emissions > 0 else 0
        
        return {
            'current': current_emissions,
            'optimized': optimal_emissions,
            'reduction_percent': reduction_percent
        }
    
    def _optimize_single_route(self, route: Dict, emissions: Dict) -> Dict[str, Any]:
        """Generate optimization recommendations using Strands reasoning"""
        distance = route.get('distance_km', 0)
        
        # Use Strands for intelligent transport reasoning
        strands_reasoning = self.strands.reason_about_transport({
            'distance_km': distance,
            'current_mode': route.get('transport_mode', 'truck'),
            'emissions': emissions
        })
        
        recommendations = []
        if distance > 500:
            recommendations.append("Consider rail transport for long-distance shipping")
        if distance > 1000:
            recommendations.append("Evaluate intermodal transportation options")
        if emissions['current'] > 100:
            recommendations.append("Implement load consolidation to reduce trips")
        
        return {
            'recommended_mode': strands_reasoning.get('mode', 'truck'),
            'recommendations': recommendations,
            'strands_reasoning': strands_reasoning.get('reasoning', ''),
            'strands_powered': True
        }