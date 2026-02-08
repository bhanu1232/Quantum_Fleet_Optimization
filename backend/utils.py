"""
Utility functions for Q-Route quantum vehicle routing system.
Includes distance calculations, matrix building, and result formatting.
"""

import numpy as np
from math import radians, sin, cos, sqrt, atan2
from typing import List, Dict, Tuple, Optional
import logging

logger = logging.getLogger(__name__)


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


def build_road_distance_matrix(
    locations: List[Dict[str, float]],
    routing_service
) -> Tuple[np.ndarray, np.ndarray, bool]:
    """
    Build distance and duration matrices using real road networks.
    Falls back to haversine if routing service fails.
    
    Args:
        locations: List of dicts with 'lat' and 'lng' keys
        routing_service: OSRMRoutingService instance
    
    Returns:
        Tuple of (distance_matrix_km, duration_matrix_minutes, used_roads)
        used_roads is True if real roads were used, False if fallback to haversine
    """
    try:
        # Try to use real road routing
        distance_matrix, duration_matrix = routing_service.build_road_distance_matrix(locations)
        logger.info("Successfully built road-based distance matrix")
        return distance_matrix, duration_matrix, True
    except Exception as e:
        logger.warning(f"Road routing failed, falling back to haversine: {e}")
        # Fallback to haversine (straight-line) distances
        distance_matrix = build_distance_matrix(locations)
        # Estimate duration based on average speed of 50 km/h
        duration_matrix = (distance_matrix / 50.0) * 60.0  # Convert to minutes
        return distance_matrix, duration_matrix, False


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
    quantum_time: float,
    duration_matrix: Optional[np.ndarray] = None,
    routing_service = None,
    used_roads: bool = False
) -> Dict:
    """
    Format the quantum solver output into a user-friendly response.
    
    Args:
        routes: List of routes, each route is a list of location indices
        locations: Original location data
        distance_matrix: Distance matrix used for optimization
        quantum_time: Time taken by quantum solver in seconds
        duration_matrix: Optional duration matrix in minutes
        routing_service: Optional routing service for getting route geometries
        used_roads: Whether real roads were used for routing
    
    Returns:
        Formatted response dict with routes, costs, and metrics
    """
    total_distance = 0.0
    total_emissions = 0.0
    total_duration = 0.0
    formatted_routes = []
    
    for vehicle_idx, route in enumerate(routes):
        route_distance = 0.0
        route_duration = 0.0
        route_coords = []
        route_geometry = None
        
        # Calculate route distance and duration
        for i in range(len(route) - 1):
            route_distance += distance_matrix[route[i]][route[i+1]]
            if duration_matrix is not None:
                route_duration += duration_matrix[route[i]][route[i+1]]
        
        # Get coordinates for visualization
        for loc_idx in route:
            route_coords.append({
                'lat': locations[loc_idx]['lat'],
                'lng': locations[loc_idx]['lng'],
                'label': locations[loc_idx].get('label', f'Location {loc_idx}')
            })
        
        # Get actual road geometry if routing service available
        if routing_service and used_roads:
            try:
                waypoints = [(locations[idx]['lat'], locations[idx]['lng']) for idx in route]
                route_data = routing_service.get_multi_waypoint_route(waypoints)
                if route_data:
                    route_geometry = route_data['geometry']
                    # Use actual route distance/duration if available
                    route_distance = route_data['distance_km']
                    route_duration = route_data['duration_minutes']
            except Exception as e:
                logger.warning(f"Failed to get route geometry for vehicle {vehicle_idx}: {e}")
        
        route_emissions = calculate_carbon_emissions(route_distance)
        
        route_info = {
            'vehicle_id': vehicle_idx,
            'route': route,
            'coordinates': route_coords,
            'distance_km': round(route_distance, 2),
            'emissions_kg': round(route_emissions, 2),
            'duration_minutes': round(route_duration, 1) if route_duration > 0 else None
        }
        
        # Add geometry if available
        if route_geometry:
            route_info['geometry'] = route_geometry
        
        formatted_routes.append(route_info)
        
        total_distance += route_distance
        total_emissions += route_emissions
        total_duration += route_duration
    
    response = {
        'success': True,
        'routes': formatted_routes,
        'total_distance_km': round(total_distance, 2),
        'total_emissions_kg': round(total_emissions, 2),
        'quantum_time_seconds': round(quantum_time, 3),
        'num_vehicles': len(routes),
        'num_locations': len(locations),
        'used_real_roads': used_roads
    }
    
    if total_duration > 0:
        response['total_duration_minutes'] = round(total_duration, 1)
    
    return response


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
