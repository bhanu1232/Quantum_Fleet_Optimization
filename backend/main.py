"""
Q-Route FastAPI Backend
Quantum-powered vehicle routing optimization API
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import List, Dict, Optional
import numpy as np

from quantum_solver import solve_route_quantum
from utils import build_distance_matrix, format_routes_response, generate_color_for_vehicle


app = FastAPI(
    title="Q-Route API",
    description="Quantum Vehicle Routing Optimization",
    version="1.0.0"
)

# CORS middleware for frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Request/Response Models
class Location(BaseModel):
    lat: float = Field(..., description="Latitude")
    lng: float = Field(..., description="Longitude")
    label: Optional[str] = Field(None, description="Location label/name")


class RouteRequest(BaseModel):
    locations: List[Location] = Field(..., min_items=2, max_items=20)
    num_vehicles: int = Field(..., ge=1, le=5, description="Number of vehicles (1-5)")
    optimize_for: str = Field(default="distance", description="Optimization target: 'distance' or 'carbon'")


class RouteInfo(BaseModel):
    vehicle_id: int
    route: List[int]
    coordinates: List[Location]
    distance_km: float
    emissions_kg: float
    color: str


class RouteResponse(BaseModel):
    success: bool
    routes: List[RouteInfo]
    total_distance_km: float
    total_emissions_kg: float
    quantum_time_seconds: float
    num_vehicles: int
    num_locations: int


# API Endpoints
@app.get("/")
async def root():
    """Root endpoint - API information"""
    return {
        "name": "Q-Route: The Entangled Fleet",
        "description": "Quantum-powered vehicle routing optimization",
        "version": "1.0.0",
        "endpoints": {
            "optimize": "/api/optimize-route",
            "health": "/api/health"
        }
    }


@app.get("/api/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "quantum_backend": "AerSimulator",
        "algorithm": "QAOA-inspired"
    }


@app.post("/api/optimize-route", response_model=RouteResponse)
async def optimize_route(request: RouteRequest):
    """
    Optimize vehicle routes using quantum algorithms.
    
    Args:
        request: RouteRequest containing locations and parameters
    
    Returns:
        RouteResponse with optimized routes and metrics
    """
    try:
        # Validate input
        if len(request.locations) < 2:
            raise HTTPException(
                status_code=400,
                detail="At least 2 locations required (including depot)"
            )
        
        if request.num_vehicles > len(request.locations) - 1:
            raise HTTPException(
                status_code=400,
                detail=f"Number of vehicles ({request.num_vehicles}) cannot exceed number of delivery locations ({len(request.locations) - 1})"
            )
        
        # Convert locations to list of dicts
        locations_data = [loc.dict() for loc in request.locations]
        
        # Build distance matrix
        distance_matrix = build_distance_matrix(locations_data)
        
        # Apply carbon optimization if requested (weight distances by emission factor)
        if request.optimize_for == "carbon":
            # Heavier vehicles prefer shorter routes (multiply by emission factor)
            distance_matrix = distance_matrix * 1.2
        
        # Solve using quantum algorithm
        routes, quantum_time = solve_route_quantum(
            distance_matrix=distance_matrix,
            num_vehicles=request.num_vehicles
        )
        
        # Format response
        response_data = format_routes_response(
            routes=routes,
            locations=locations_data,
            distance_matrix=distance_matrix,
            quantum_time=quantum_time
        )
        
        # Add colors to routes
        for i, route_info in enumerate(response_data['routes']):
            route_info['color'] = generate_color_for_vehicle(i, len(response_data['routes']))
        
        return RouteResponse(**response_data)
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Quantum optimization failed: {str(e)}"
        )


@app.post("/api/simulate-failure")
async def simulate_vehicle_failure(request: RouteRequest, failed_vehicle_id: int):
    """
    Simulate dynamic re-routing when a vehicle fails.
    Demonstrates quantum advantage in real-time optimization.
    
    Args:
        request: Original route request
        failed_vehicle_id: ID of the vehicle that failed
    
    Returns:
        New optimized routes redistributing the load
    """
    try:
        # Get original routes
        original_response = await optimize_route(request)
        
        # Find the failed vehicle's route
        if failed_vehicle_id >= len(original_response.routes):
            raise HTTPException(
                status_code=400,
                detail=f"Invalid vehicle ID: {failed_vehicle_id}"
            )
        
        failed_route = original_response.routes[failed_vehicle_id]
        
        # Redistribute locations to remaining vehicles
        remaining_vehicles = request.num_vehicles - 1
        
        if remaining_vehicles < 1:
            raise HTTPException(
                status_code=400,
                detail="Cannot redistribute with no remaining vehicles"
            )
        
        # Re-optimize with one fewer vehicle
        new_request = RouteRequest(
            locations=request.locations,
            num_vehicles=remaining_vehicles,
            optimize_for=request.optimize_for
        )
        
        new_response = await optimize_route(new_request)
        
        return {
            "success": True,
            "failed_vehicle_id": failed_vehicle_id,
            "original_routes": original_response.routes,
            "new_routes": new_response.routes,
            "redistribution_time": new_response.quantum_time_seconds,
            "message": "Routes successfully recalculated using quantum optimization"
        }
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Re-routing failed: {str(e)}"
        )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
