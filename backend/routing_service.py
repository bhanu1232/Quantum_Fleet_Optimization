"""
OSRM Routing Service Integration
Provides real road network routing using OpenStreetMap data via OSRM API.
"""

import requests
import polyline
import numpy as np
from typing import List, Dict, Tuple, Optional
from functools import lru_cache
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class OSRMRoutingService:
    """
    Integration with OSRM (Open Source Routing Machine) for real road routing.
    """
    
    def __init__(self, base_url: str = "https://router.project-osrm.org"):
        """
        Initialize OSRM routing service.
        
        Args:
            base_url: OSRM server URL (default: public demo server)
        """
        self.base_url = base_url.rstrip('/')
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Q-Route/1.0 (Quantum Fleet Optimization)'
        })
        
    def get_route(
        self, 
        origin: Tuple[float, float], 
        destination: Tuple[float, float],
        profile: str = "driving"
    ) -> Optional[Dict]:
        """
        Get route between two points using real roads.
        
        Args:
            origin: (lat, lng) tuple for start point
            destination: (lat, lng) tuple for end point
            profile: Routing profile (driving, walking, cycling)
        
        Returns:
            Dict with 'distance_km', 'duration_minutes', 'geometry' (list of [lat, lng])
        """
        try:
            # OSRM uses lng,lat format (opposite of typical lat,lng)
            coords = f"{origin[1]},{origin[0]};{destination[1]},{destination[0]}"
            url = f"{self.base_url}/route/v1/{profile}/{coords}"
            
            params = {
                'overview': 'full',  # Get full route geometry
                'geometries': 'polyline',  # Use polyline encoding
                'steps': 'false'  # Don't need turn-by-turn for now
            }
            
            response = self.session.get(url, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            
            if data['code'] != 'Ok' or not data.get('routes'):
                logger.warning(f"OSRM routing failed: {data.get('code', 'Unknown error')}")
                return None
            
            route = data['routes'][0]
            
            # Decode polyline geometry
            geometry_encoded = route['geometry']
            geometry_coords = polyline.decode(geometry_encoded)
            
            return {
                'distance_km': route['distance'] / 1000.0,  # meters to km
                'duration_minutes': route['duration'] / 60.0,  # seconds to minutes
                'geometry': geometry_coords,  # List of (lat, lng) tuples
                'distance_meters': route['distance'],
                'duration_seconds': route['duration']
            }
            
        except requests.exceptions.RequestException as e:
            logger.error(f"OSRM API request failed: {e}")
            return None
        except Exception as e:
            logger.error(f"Route calculation error: {e}")
            return None
    
    def build_road_distance_matrix(
        self, 
        locations: List[Dict[str, float]],
        profile: str = "driving"
    ) -> Tuple[np.ndarray, np.ndarray]:
        """
        Build distance and duration matrices using real road networks.
        
        Args:
            locations: List of dicts with 'lat' and 'lng' keys
            profile: Routing profile
        
        Returns:
            Tuple of (distance_matrix_km, duration_matrix_minutes)
        """
        n = len(locations)
        distance_matrix = np.zeros((n, n))
        duration_matrix = np.zeros((n, n))
        
        try:
            # Use OSRM Table service for efficient matrix calculation
            coords_str = ";".join([f"{loc['lng']},{loc['lat']}" for loc in locations])
            url = f"{self.base_url}/table/v1/{profile}/{coords_str}"
            
            params = {
                'annotations': 'distance,duration'
            }
            
            response = self.session.get(url, params=params, timeout=30)
            response.raise_for_status()
            
            data = response.json()
            
            if data['code'] != 'Ok':
                logger.warning(f"OSRM table service failed: {data.get('code')}")
                return self._fallback_pairwise_matrix(locations, profile)
            
            # Extract distance and duration matrices
            distances = np.array(data['distances']) / 1000.0  # meters to km
            durations = np.array(data['durations']) / 60.0  # seconds to minutes
            
            return distances, durations
            
        except Exception as e:
            logger.error(f"Matrix calculation failed: {e}. Falling back to pairwise routing.")
            return self._fallback_pairwise_matrix(locations, profile)
    
    def _fallback_pairwise_matrix(
        self,
        locations: List[Dict[str, float]],
        profile: str = "driving"
    ) -> Tuple[np.ndarray, np.ndarray]:
        """
        Fallback: Build matrix by requesting individual routes.
        Used when Table service fails.
        """
        n = len(locations)
        distance_matrix = np.zeros((n, n))
        duration_matrix = np.zeros((n, n))
        
        for i in range(n):
            for j in range(n):
                if i != j:
                    origin = (locations[i]['lat'], locations[i]['lng'])
                    dest = (locations[j]['lat'], locations[j]['lng'])
                    
                    route = self.get_route(origin, dest, profile)
                    
                    if route:
                        distance_matrix[i][j] = route['distance_km']
                        duration_matrix[i][j] = route['duration_minutes']
                    else:
                        # Ultimate fallback: use haversine distance
                        from utils import haversine_distance
                        dist_km = haversine_distance(
                            locations[i]['lat'], locations[i]['lng'],
                            locations[j]['lat'], locations[j]['lng']
                        )
                        distance_matrix[i][j] = dist_km
                        # Estimate duration: assume 50 km/h average speed
                        duration_matrix[i][j] = (dist_km / 50.0) * 60.0
        
        return distance_matrix, duration_matrix
    
    def get_multi_waypoint_route(
        self,
        waypoints: List[Tuple[float, float]],
        profile: str = "driving"
    ) -> Optional[Dict]:
        """
        Get route through multiple waypoints in order.
        
        Args:
            waypoints: List of (lat, lng) tuples in visit order
            profile: Routing profile
        
        Returns:
            Dict with total distance, duration, and full geometry
        """
        if len(waypoints) < 2:
            return None
        
        try:
            # OSRM uses lng,lat format
            coords = ";".join([f"{wp[1]},{wp[0]}" for wp in waypoints])
            url = f"{self.base_url}/route/v1/{profile}/{coords}"
            
            params = {
                'overview': 'full',
                'geometries': 'polyline',
                'steps': 'false'
            }
            
            response = self.session.get(url, params=params, timeout=15)
            response.raise_for_status()
            
            data = response.json()
            
            if data['code'] != 'Ok' or not data.get('routes'):
                return None
            
            route = data['routes'][0]
            geometry_coords = polyline.decode(route['geometry'])
            
            return {
                'distance_km': route['distance'] / 1000.0,
                'duration_minutes': route['duration'] / 60.0,
                'geometry': geometry_coords,
                'num_waypoints': len(waypoints)
            }
            
        except Exception as e:
            logger.error(f"Multi-waypoint route failed: {e}")
            return None
    
    def snap_to_road(
        self,
        lat: float,
        lng: float,
        profile: str = "driving"
    ) -> Optional[Tuple[float, float]]:
        """
        Snap a coordinate to the nearest road.
        
        Args:
            lat: Latitude
            lng: Longitude
            profile: Routing profile
        
        Returns:
            (lat, lng) tuple of nearest road point, or None if failed
        """
        try:
            url = f"{self.base_url}/nearest/v1/{profile}/{lng},{lat}"
            
            params = {
                'number': 1  # Return only the nearest point
            }
            
            response = self.session.get(url, params=params, timeout=5)
            response.raise_for_status()
            
            data = response.json()
            
            if data['code'] != 'Ok' or not data.get('waypoints'):
                return None
            
            waypoint = data['waypoints'][0]
            # OSRM returns [lng, lat]
            return (waypoint['location'][1], waypoint['location'][0])
            
        except Exception as e:
            logger.error(f"Road snapping failed: {e}")
            return None
    
    def health_check(self) -> bool:
        """
        Check if OSRM service is available.
        
        Returns:
            True if service is healthy, False otherwise
        """
        try:
            # Simple route request to test connectivity
            test_coords = "13.388860,52.517037;13.397634,52.529407"  # Berlin
            url = f"{self.base_url}/route/v1/driving/{test_coords}"
            
            response = self.session.get(url, timeout=5)
            response.raise_for_status()
            
            data = response.json()
            return data['code'] == 'Ok'
            
        except Exception as e:
            logger.error(f"OSRM health check failed: {e}")
            return False


# Singleton instance
_routing_service = None

def get_routing_service(base_url: str = "https://router.project-osrm.org") -> OSRMRoutingService:
    """
    Get or create the global routing service instance.
    """
    global _routing_service
    if _routing_service is None:
        _routing_service = OSRMRoutingService(base_url)
    return _routing_service
