import { useState, useEffect } from 'react';
import axios from 'axios';
import MapComponent from './components/MapComponent';
import ControlPanel from './components/ControlPanel';
import LoadingAnimation from './components/LoadingAnimation';
import './App.css';

function App() {
  const [locations, setLocations] = useState([]);
  const [numVehicles, setNumVehicles] = useState(2);
  const [optimizeFor, setOptimizeFor] = useState('distance');
  const [routes, setRoutes] = useState(null);
  const [results, setResults] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);

  // Listen for search location events
  useEffect(() => {
    const handleSearchLocation = (event) => {
      const { lat, lng, label } = event.detail;
      handleAddLocation({ lat, lng }, label);
    };

    window.addEventListener('addLocationFromSearch', handleSearchLocation);
    return () => window.removeEventListener('addLocationFromSearch', handleSearchLocation);
  }, [locations]);

  // Validate if location is on land (not in water)
  const validateLocation = async (lat, lng) => {
    try {
      // Use Nominatim reverse geocoding to check if location is on land
      const response = await fetch(
        `https://nominatim.openstreetmap.org/reverse?format=json&lat=${lat}&lon=${lng}&zoom=10`
      );
      const data = await response.json();

      // Check if the location has a valid address (indicates land)
      // If it's in water, Nominatim won't return proper address components
      if (!data.address || data.error) {
        return false;
      }

      // Additional check: if display_name contains water-related terms
      const waterTerms = ['ocean', 'sea', 'bay', 'gulf', 'strait', 'channel'];
      const displayName = data.display_name.toLowerCase();
      const isWater = waterTerms.some(term => displayName.includes(term)) &&
        !data.address.road &&
        !data.address.city &&
        !data.address.town &&
        !data.address.village;

      return !isWater;
    } catch (error) {
      console.error('Location validation error:', error);
      // If validation fails, allow the location (fail open)
      return true;
    }
  };

  const handleAddLocation = async (latlng, customLabel = null) => {
    // Validate location is on land
    const isOnLand = await validateLocation(latlng.lat, latlng.lng);

    if (!isOnLand) {
      setError('Cannot add location in water. Please select a location on land.');
      setTimeout(() => setError(null), 4000);
      return;
    }

    const newLocation = {
      lat: latlng.lat,
      lng: latlng.lng,
      label: customLabel || (locations.length === 0
        ? 'Depot (Warehouse)'
        : `Delivery Point ${locations.length}`)
    };
    setLocations([...locations, newLocation]);
    // Clear previous results when adding new location
    setRoutes(null);
    setResults(null);
  };

  const handleRemoveLocation = (index) => {
    const newLocations = locations.filter((_, i) => i !== index);
    setLocations(newLocations);
    setRoutes(null);
    setResults(null);
  };

  const handleClearAll = () => {
    setLocations([]);
    setRoutes(null);
    setResults(null);
    setError(null);
  };

  const handleOptimize = async () => {
    if (locations.length < 2) {
      setError('Please add at least 2 locations (depot + 1 delivery point)');
      return;
    }

    setIsLoading(true);
    setError(null);

    try {
      const response = await axios.post('http://localhost:8000/api/optimize-route', {
        locations: locations,
        num_vehicles: numVehicles,
        optimize_for: optimizeFor
      });

      if (response.data.success) {
        setRoutes(response.data.routes);
        setResults(response.data);
      } else {
        setError('Optimization failed. Please try again.');
      }
    } catch (err) {
      console.error('Optimization error:', err);
      setError(
        err.response?.data?.detail ||
        'Failed to connect to quantum backend. Make sure the server is running.'
      );
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="app">
      {isLoading && <LoadingAnimation />}

      <div className="app-layout">
        {/* Left sidebar - Control Panel */}
        <aside className="sidebar">
          <ControlPanel
            numVehicles={numVehicles}
            onNumVehiclesChange={setNumVehicles}
            optimizeFor={optimizeFor}
            onOptimizeForChange={setOptimizeFor}
            onOptimize={handleOptimize}
            onClear={handleClearAll}
            isLoading={isLoading}
            results={results}
            locationsCount={locations.length}
            locations={locations}
          />
        </aside>

        {/* Main content - Map */}
        <main className="main-content">
          <MapComponent
            locations={locations}
            onAddLocation={handleAddLocation}
            routes={routes}
            onRemoveLocation={handleRemoveLocation}
          />

          {/* Error notification */}
          {error && (
            <div className="error-notification">
              <div className="error-content">
                <span className="error-icon">⚠️</span>
                <p>{error}</p>
                <button
                  className="error-close"
                  onClick={() => setError(null)}
                >
                  ✕
                </button>
              </div>
            </div>
          )}
        </main>
      </div>
    </div>
  );
}

export default App;
