"""
Test script for OSRM routing service integration
"""

import sys
import os

# Add backend to path
sys.path.insert(0, os.path.dirname(__file__))

from routing_service import get_routing_service

def test_routing_service():
    print("=" * 60)
    print("Testing OSRM Routing Service Integration")
    print("=" * 60)
    
    # Initialize routing service
    print("\n1. Initializing OSRM routing service...")
    routing_service = get_routing_service()
    
    # Health check
    print("\n2. Performing health check...")
    is_healthy = routing_service.health_check()
    print(f"   ✓ OSRM service is {'available' if is_healthy else 'unavailable'}")
    
    if not is_healthy:
        print("\n   ⚠ OSRM service is not available. Will fall back to haversine.")
        return
    
    # Test single route
    print("\n3. Testing single route (New York: Times Square to Central Park)...")
    origin = (40.758, -73.9855)  # Times Square
    destination = (40.7829, -73.9654)  # Central Park
    
    route = routing_service.get_route(origin, destination)
    
    if route:
        print(f"   ✓ Route found!")
        print(f"     Distance: {route['distance_km']:.2f} km")
        print(f"     Duration: {route['duration_minutes']:.1f} minutes")
        print(f"     Geometry points: {len(route['geometry'])}")
    else:
        print("   ✗ Route not found")
    
    # Test distance matrix
    print("\n4. Testing distance matrix (3 locations in NYC)...")
    locations = [
        {'lat': 40.758, 'lng': -73.9855},   # Times Square
        {'lat': 40.7829, 'lng': -73.9654},  # Central Park
        {'lat': 40.7061, 'lng': -73.9969}   # Brooklyn Bridge
    ]
    
    try:
        distance_matrix, duration_matrix = routing_service.build_road_distance_matrix(locations)
        print(f"   ✓ Distance matrix built successfully!")
        print(f"     Matrix shape: {distance_matrix.shape}")
        print(f"\n     Distance Matrix (km):")
        for i, row in enumerate(distance_matrix):
            print(f"       Location {i}: {[f'{d:.2f}' for d in row]}")
        print(f"\n     Duration Matrix (minutes):")
        for i, row in enumerate(duration_matrix):
            print(f"       Location {i}: {[f'{d:.1f}' for d in row]}")
    except Exception as e:
        print(f"   ✗ Error: {e}")
    
    # Test multi-waypoint route
    print("\n5. Testing multi-waypoint route...")
    waypoints = [
        (40.758, -73.9855),   # Times Square
        (40.7829, -73.9654),  # Central Park
        (40.7061, -73.9969),  # Brooklyn Bridge
        (40.758, -73.9855)    # Back to Times Square
    ]
    
    multi_route = routing_service.get_multi_waypoint_route(waypoints)
    
    if multi_route:
        print(f"   ✓ Multi-waypoint route found!")
        print(f"     Total distance: {multi_route['distance_km']:.2f} km")
        print(f"     Total duration: {multi_route['duration_minutes']:.1f} minutes")
        print(f"     Waypoints: {multi_route['num_waypoints']}")
        print(f"     Geometry points: {len(multi_route['geometry'])}")
    else:
        print("   ✗ Multi-waypoint route not found")
    
    print("\n" + "=" * 60)
    print("✓ All tests completed!")
    print("=" * 60)

if __name__ == "__main__":
    test_routing_service()
