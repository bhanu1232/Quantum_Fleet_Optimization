"""
Test script to verify Q-Route backend API integration.
This script tests the optimization endpoint with sample data.
"""

import requests
import json
import time

# Backend URL
BASE_URL = "http://localhost:8000"

def test_health_check():
    """Test the health check endpoint."""
    print("🔍 Testing health check endpoint...")
    try:
        response = requests.get(f"{BASE_URL}/api/health")
        print(f"✅ Health check status: {response.status_code}")
        print(f"   Response: {response.json()}")
        return True
    except Exception as e:
        print(f"❌ Health check failed: {e}")
        return False

def test_optimization():
    """Test the route optimization endpoint."""
    print("\n🔍 Testing route optimization...")
    
    # Sample data: New York City area
    test_data = {
        "locations": [
            {"lat": 40.7128, "lng": -74.0060, "label": "Depot (Manhattan)"},
            {"lat": 40.7580, "lng": -73.9855, "label": "Times Square"},
            {"lat": 40.7489, "lng": -73.9680, "label": "Queens"},
            {"lat": 40.6782, "lng": -73.9442, "label": "Brooklyn"},
            {"lat": 40.7614, "lng": -73.9776, "label": "Central Park"},
            {"lat": 40.7061, "lng": -74.0087, "label": "Financial District"}
        ],
        "num_vehicles": 2,
        "optimize_for": "distance"
    }
    
    try:
        print(f"   Sending request with {len(test_data['locations'])} locations and {test_data['num_vehicles']} vehicles...")
        start_time = time.time()
        
        response = requests.post(
            f"{BASE_URL}/api/optimize-route",
            json=test_data,
            headers={"Content-Type": "application/json"}
        )
        
        elapsed_time = time.time() - start_time
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Optimization successful!")
            print(f"   Status code: {response.status_code}")
            print(f"   Request time: {elapsed_time:.2f}s")
            print(f"\n📊 Results:")
            print(f"   Total Distance: {result['total_distance_km']} km")
            print(f"   Total Emissions: {result['total_emissions_kg']} kg CO₂")
            print(f"   Quantum Time: {result['quantum_time_seconds']}s")
            print(f"   Vehicles Used: {result['num_vehicles']}")
            print(f"\n🚚 Route Breakdown:")
            for route in result['routes']:
                print(f"   Vehicle {route['vehicle_id'] + 1}:")
                print(f"      - Distance: {route['distance_km']} km")
                print(f"      - Emissions: {route['emissions_kg']} kg CO₂")
                print(f"      - Stops: {len(route['route']) - 2}")
                print(f"      - Color: {route['color']}")
            return True
        else:
            print(f"❌ Optimization failed with status {response.status_code}")
            print(f"   Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Optimization test failed: {e}")
        return False

def test_carbon_optimization():
    """Test carbon emission optimization mode."""
    print("\n🔍 Testing carbon optimization mode...")
    
    test_data = {
        "locations": [
            {"lat": 40.7128, "lng": -74.0060, "label": "Depot"},
            {"lat": 40.7580, "lng": -73.9855, "label": "Point 1"},
            {"lat": 40.7489, "lng": -73.9680, "label": "Point 2"},
            {"lat": 40.6782, "lng": -73.9442, "label": "Point 3"}
        ],
        "num_vehicles": 2,
        "optimize_for": "carbon"
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/api/optimize-route",
            json=test_data,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Carbon optimization successful!")
            print(f"   Total Emissions: {result['total_emissions_kg']} kg CO₂")
            return True
        else:
            print(f"❌ Carbon optimization failed: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Carbon optimization test failed: {e}")
        return False

def main():
    """Run all tests."""
    print("=" * 60)
    print("🚀 Q-Route Backend Integration Tests")
    print("=" * 60)
    
    results = []
    
    # Test 1: Health check
    results.append(("Health Check", test_health_check()))
    
    # Test 2: Distance optimization
    results.append(("Distance Optimization", test_optimization()))
    
    # Test 3: Carbon optimization
    results.append(("Carbon Optimization", test_carbon_optimization()))
    
    # Summary
    print("\n" + "=" * 60)
    print("📋 Test Summary")
    print("=" * 60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} - {test_name}")
    
    print(f"\n🎯 Overall: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 All tests passed! Backend is working correctly.")
        print("   Frontend should be able to connect at: http://localhost:5173")
    else:
        print("\n⚠️ Some tests failed. Check the backend server logs.")

if __name__ == "__main__":
    main()
