import { MapContainer, TileLayer, Marker, Popup, Polyline, useMapEvents } from 'react-leaflet';
import { useState, useEffect } from 'react';
import L from 'leaflet';
import 'leaflet/dist/leaflet.css';
import { motion } from 'framer-motion';
import { Search, X, MapPin } from 'lucide-react';
import axios from 'axios';
import './MapComponent.css';

// Fix for default marker icons in React-Leaflet
delete L.Icon.Default.prototype._getIconUrl;
L.Icon.Default.mergeOptions({
    iconRetinaUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-icon-2x.png',
    iconUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-icon.png',
    shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-shadow.png',
});

// Custom marker icons - Yellow for Delivery, Red for Warehouse
const createCustomIcon = (isDepot, isNew = false) => {
    return L.divIcon({
        className: 'custom-marker',
        html: `
            <div class="marker-pin ${isDepot ? 'depot' : 'delivery'} ${!isNew ? 'no-animate' : ''}">
                <div class="marker-icon">
                    ${isDepot ? '🏭' : '📦'}
                </div>
            </div>
        `,
        iconSize: [40, 40],
        iconAnchor: [20, 40],
        popupAnchor: [0, -40]
    });
};

const MapClickHandler = ({ onMapClick }) => {
    useMapEvents({
        click: (e) => {
            onMapClick(e.latlng);
        },
    });
    return null;
};

const MapComponent = ({ locations, onAddLocation, routes, onRemoveLocation }) => {
    // Default center: Vijayawada, Andhra Pradesh, India
    const [center] = useState([16.5062, 80.6480]);
    const [zoom] = useState(10);
    const [lastLocationCount, setLastLocationCount] = useState(0);

    // Search state
    const [searchQuery, setSearchQuery] = useState('');
    const [searchResults, setSearchResults] = useState([]);
    const [isSearching, setIsSearching] = useState(false);

    // Track which marker is new to only animate that one
    useEffect(() => {
        setLastLocationCount(locations.length);
    }, [locations.length]);

    // Search for locations
    const handleSearch = async (query) => {
        setSearchQuery(query);

        if (query.length < 3) {
            setSearchResults([]);
            return;
        }

        setIsSearching(true);
        try {
            const response = await axios.get(
                `https://nominatim.openstreetmap.org/search?format=json&q=${encodeURIComponent(query)},India&limit=5`
            );
            setSearchResults(response.data);
        } catch (error) {
            console.error('Search error:', error);
            setSearchResults([]);
        } finally {
            setIsSearching(false);
        }
    };

    const handleSelectLocation = (result) => {
        const lat = parseFloat(result.lat);
        const lng = parseFloat(result.lon);

        // Trigger the add location event
        window.dispatchEvent(new CustomEvent('addLocationFromSearch', {
            detail: { lat, lng, label: result.display_name.split(',')[0] }
        }));

        setSearchQuery('');
        setSearchResults([]);
    };

    const clearSearch = () => {
        setSearchQuery('');
        setSearchResults([]);
    };

    return (
        <div className="map-wrapper">
            {/* Floating Search Bar */}
            <div className="map-search-overlay">
                <div className="map-search-container">
                    <Search className="map-search-icon" size={18} />
                    <input
                        type="text"
                        placeholder="Search for a location in India..."
                        value={searchQuery}
                        onChange={(e) => handleSearch(e.target.value)}
                        className="map-search-input"
                    />
                    {searchQuery && (
                        <button onClick={clearSearch} className="map-search-clear">
                            <X size={16} />
                        </button>
                    )}
                </div>

                {/* Search Results Dropdown */}
                {searchResults.length > 0 && (
                    <div className="map-search-results">
                        {searchResults.map((result, index) => (
                            <button
                                key={index}
                                onClick={() => handleSelectLocation(result)}
                                className="map-search-result-item"
                            >
                                <MapPin size={16} className="result-icon" />
                                <div className="result-text">
                                    <div className="result-name">{result.display_name.split(',')[0]}</div>
                                    <div className="result-address">{result.display_name}</div>
                                </div>
                            </button>
                        ))}
                    </div>
                )}
            </div>

            <MapContainer
                center={center}
                zoom={zoom}
                className="map-container"
                zoomControl={true}
            >
                <TileLayer
                    attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
                    url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
                />

                <MapClickHandler onMapClick={onAddLocation} />

                {/* Render location markers */}
                {locations.map((location, index) => {
                    const isDepot = index === 0;
                    const isNew = index === locations.length - 1 && locations.length > lastLocationCount;

                    return (
                        <Marker
                            key={`marker-${index}-${location.lat}-${location.lng}`}
                            position={[location.lat, location.lng]}
                            icon={createCustomIcon(isDepot, isNew)}
                        >
                            <Popup>
                                <div className="popup-content">
                                    <strong>{location.label}</strong>
                                    <p>Lat: {location.lat.toFixed(4)}, Lng: {location.lng.toFixed(4)}</p>
                                    <button
                                        onClick={() => onRemoveLocation(index)}
                                        className="remove-btn"
                                    >
                                        Remove
                                    </button>
                                </div>
                            </Popup>
                        </Marker>
                    );
                })}

                {/* Render optimized routes */}
                {routes && routes.map((route, routeIndex) => {
                    // Use real road geometry if available, otherwise use straight lines
                    const routePositions = route.geometry 
                        ? route.geometry.map(coord => [coord[0], coord[1]])  // OSRM returns [lat, lng]
                        : route.coordinates.map(coord => [coord.lat, coord.lng]);  // Fallback to straight lines
                    
                    return (
                        <Polyline
                            key={routeIndex}
                            positions={routePositions}
                            pathOptions={{
                                color: route.color,
                                weight: route.geometry ? 5 : 4,  // Slightly thicker for real roads
                                opacity: route.geometry ? 0.9 : 0.7,
                                dashArray: route.geometry ? null : '10, 5'  // Solid for roads, dashed for straight
                            }}
                        >
                            <Popup>
                                <div className="route-popup">
                                    <h4>🚗 Vehicle {route.vehicle_id + 1}</h4>
                                    <p><strong>Distance:</strong> {route.distance_km} km</p>
                                    {route.duration_minutes && (
                                        <p><strong>Duration:</strong> {Math.round(route.duration_minutes)} min</p>
                                    )}
                                    <p><strong>Emissions:</strong> {route.emissions_kg} kg CO₂</p>
                                    <p><strong>Stops:</strong> {route.route.length - 2}</p>
                                    {route.geometry && (
                                        <p className="text-muted" style={{ fontSize: '0.8rem', marginTop: '4px' }}>
                                            ✓ Real road route
                                        </p>
                                    )}
                                </div>
                            </Popup>
                        </Polyline>
                    );
                })}
            </MapContainer>

            {/* Instructions overlay */}
            {locations.length === 0 && (
                <motion.div
                    className="map-instructions"
                    initial={{ opacity: 0, y: -20 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ delay: 0.5 }}
                >
                    <div className="instruction-card glass">
                        <h3>🗺️ Click on the map to add locations</h3>
                        <p className="text-muted">
                            First click sets the depot (warehouse). Subsequent clicks add delivery points.
                        </p>
                        <p className="text-muted" style={{ fontSize: '0.85rem', marginTop: '8px' }}>
                            ⚠️ Only land locations are accepted. Water bodies will be rejected.
                        </p>
                    </div>
                </motion.div>
            )}
        </div>
    );
};

export default MapComponent;
