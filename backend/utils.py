"""
Utility functions for Q-Route quantum vehicle routing system.
Includes distance calculations, matrix building, and result formatting.
"""

import numpy as np
from math import radians, sin, cos, sqrt, atan2
from typing import List, Dict, Tuple


def haversine_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """
    Calculate the great circle distance between two points on Earth.
    
    Args:
        lat1, lon1: Latitude and longitude of first point in degrees
        lat2, lon2: Latitude and longitude of second point in degrees
    
    Returns:
        Distance in kilometers
    """
    # Convert to radians
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
    
    # Haversine formula
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * atan2(sqrt(a), sqrt(1-a))
    
    # Earth's radius in kilometers
    R = 6371.0
    
    return R * c


def build_distance_matrix(locations: List[Dict[str, float]]) -> np.ndarray:
    """
    Build a distance matrix from a list of locations.
    
    Args:
        locations: List of dicts with 'lat' and 'lng' keys
    
    Returns:
        NxN numpy array where element [i,j] is distance from location i to j
    """
    n = len(locations)
    matrix = np.zeros((n, n))
    
    for i in range(n):
        for j in range(n):
            if i != j:
                matrix[i][j] = haversine_distance(
                    locations[i]['lat'], 
                    locations[i]['lng'],
                    locations[j]['lat'], 
                    locations[j]['lng']
                )
    
    return matrix


def calculate_carbon_emissions(distance_km: float, vehicle_type: str = "truck") -> float:
    """
    Calculate CO2 emissions based on distance and vehicle type.
    
    Args:
        distance_km: Distance traveled in kilometers
        vehicle_type: Type of vehicle (truck, van, car)
    
    Returns:
        CO2 emissions in kg
    """
    # Emission factors in kg CO2 per km
    emission_factors = {
        "truck": 0.8,   # Heavy duty truck
        "van": 0.25,    # Delivery van
        "car": 0.15     # Standard car
    }
    
    factor = emission_factors.get(vehicle_type, 0.8)
    return distance_km * factor


def format_routes_response(
    routes: List[List[int]], 
    locations: List[Dict],
    distance_matrix: np.ndarray,
    quantum_time: float
) -> Dict:
    """
    Format the quantum solver output into a user-friendly response.
    
    Args:
        routes: List of routes, each route is a list of location indices
        locations: Original location data
        distance_matrix: Distance matrix used for optimization
        quantum_time: Time taken by quantum solver in seconds
    
    Returns:
        Formatted response dict with routes, costs, and metrics
    """
    total_distance = 0.0
    total_emissions = 0.0
    formatted_routes = []
    
    for vehicle_idx, route in enumerate(routes):
        route_distance = 0.0
        route_coords = []
        
        # Calculate route distance
        for i in range(len(route) - 1):
            route_distance += distance_matrix[route[i]][route[i+1]]
        
        # Get coordinates for visualization
        for loc_idx in route:
            route_coords.append({
                'lat': locations[loc_idx]['lat'],
                'lng': locations[loc_idx]['lng'],
                'label': locations[loc_idx].get('label', f'Location {loc_idx}')
            })
        
        route_emissions = calculate_carbon_emissions(route_distance)
        
        formatted_routes.append({
            'vehicle_id': vehicle_idx,
            'route': route,
            'coordinates': route_coords,
            'distance_km': round(route_distance, 2),
            'emissions_kg': round(route_emissions, 2)
        })
        
        total_distance += route_distance
        total_emissions += route_emissions
    
    return {
        'success': True,
        'routes': formatted_routes,
        'total_distance_km': round(total_distance, 2),
        'total_emissions_kg': round(total_emissions, 2),
        'quantum_time_seconds': round(quantum_time, 3),
        'num_vehicles': len(routes),
        'num_locations': len(locations)
    }


def generate_color_for_vehicle(vehicle_id: int, total_vehicles: int) -> str:
    """
    Generate a distinct color for each vehicle route.
    
    Args:
        vehicle_id: Index of the vehicle (0-based)
        total_vehicles: Total number of vehicles
    
    Returns:
        Hex color string
    """
    colors = [
        '#6366f1',  # Indigo
        '#ec4899',  # Pink
        '#10b981',  # Emerald
        '#f59e0b',  # Amber
        '#8b5cf6',  # Purple
        '#06b6d4',  # Cyan
        '#ef4444',  # Red
        '#14b8a6',  # Teal
    ]
    
    return colors[vehicle_id % len(colors)]
