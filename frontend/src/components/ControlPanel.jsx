import { motion } from 'framer-motion';
import { Truck, MapPin, Zap, Leaf, TrendingDown, Clock, Search, X, ChevronDown } from 'lucide-react';
import { useState } from 'react';
import './ControlPanel.css';
import logo from "../assets/logo.png"

const ControlPanel = ({
    numVehicles,
    onNumVehiclesChange,
    optimizeFor,
    onOptimizeForChange,
    onOptimize,
    onClear,
    isLoading,
    results,
    locationsCount,
    locations
}) => {

    return (
        <div className="control-panel">
            {/* Compact Header */}
            <div className="panel-header-compact">
                <div className="header-top">
                    <img src={logo} alt="" style={{ borderRadius: "100%", height: "60px" }} />
                    <div className="header-content">
                        <h1 className="app-title-compact">Q-ROUTE</h1>
                        <p className="app-tagline">Quantum Fleet Optimization</p>
                    </div>
                </div>
            </div>

            {/* Quick Stats */}
            {locationsCount > 0 && (
                <div className="quick-stats">
                    <div className="stat-chip">
                        <MapPin size={14} />
                        <span>{locationsCount}</span>
                    </div>
                    <div className="stat-chip">
                        <Truck size={14} />
                        <span>{numVehicles}</span>
                    </div>
                    <div className="stat-chip active">
                        {optimizeFor === 'distance' ? (
                            <>
                                <TrendingDown size={14} />
                                <span>Distance</span>
                            </>
                        ) : (
                            <>
                                <Leaf size={14} />
                                <span>Carbon</span>
                            </>
                        )}
                    </div>
                </div>
            )}

            {/* Configuration Section */}
            <div className="config-section-enhanced">
                <div className="config-group">
                    <div className="section-header">
                        <Truck size={14} />
                        <span className="section-title">Fleet Size</span>
                    </div>
                    <div className="vehicle-grid">
                        {[1, 2, 3, 4, 5].map((num) => (
                            <button
                                key={num}
                                className={`vehicle-chip ${numVehicles === num ? 'active' : ''}`}
                                onClick={() => onNumVehiclesChange(num)}
                                disabled={isLoading}
                            >
                                {num}
                            </button>
                        ))}
                    </div>
                </div>

                <div className="config-group">
                    <div className="section-header">
                        <Zap size={14} />
                        <span className="section-title">Optimization Goal</span>
                    </div>
                    <div className="mode-toggle">
                        <button
                            className={`mode-option ${optimizeFor === 'distance' ? 'active' : ''}`}
                            onClick={() => onOptimizeForChange('distance')}
                            disabled={isLoading}
                        >
                            <TrendingDown size={16} />
                            <div className="mode-text">
                                <span className="mode-label">Distance</span>
                                <span className="mode-desc">Shortest path</span>
                            </div>
                        </button>
                        <button
                            className={`mode-option ${optimizeFor === 'carbon' ? 'active' : ''}`}
                            onClick={() => onOptimizeForChange('carbon')}
                            disabled={isLoading}
                        >
                            <Leaf size={16} />
                            <div className="mode-text">
                                <span className="mode-label">Carbon</span>
                                <span className="mode-desc">Eco-friendly</span>
                            </div>
                        </button>
                    </div>
                </div>
            </div>

            {/* Action Buttons */}
            <div className="action-section-enhanced">
                <button
                    className="btn btn-primary btn-optimize-enhanced"
                    onClick={onOptimize}
                    disabled={isLoading || locationsCount < 2}
                >
                    <Zap size={18} />
                    <span>{isLoading ? 'Computing...' : 'Optimize Routes'}</span>
                </button>

                {locationsCount > 0 && (
                    <button
                        className="btn-clear-enhanced"
                        onClick={onClear}
                        disabled={isLoading}
                    >
                        <X size={16} />
                        <span>Clear</span>
                    </button>
                )}
            </div>

            {/* Results Section */}
            {results && (
                <motion.div
                    className="results-section-minimal"
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                >
                    <div className="section-label">Results</div>

                    <div className="results-grid-minimal">
                        <div className="result-card-minimal">
                            <div className="result-value-large">{results.total_distance_km}</div>
                            <div className="result-label-small">km Total</div>
                        </div>
                        <div className="result-card-minimal">
                            <div className="result-value-large">{results.total_emissions_kg}</div>
                            <div className="result-label-small">kg CO₂</div>
                        </div>
                        {results.total_duration_minutes && (
                            <div className="result-card-minimal">
                                <div className="result-value-large">{Math.round(results.total_duration_minutes)}</div>
                                <div className="result-label-small">min Total</div>
                            </div>
                        )}
                        <div className="result-card-minimal">
                            <div className="result-value-large">{results.quantum_time_seconds}</div>
                            <div className="result-label-small">sec Compute</div>
                        </div>
                        <div className="result-card-minimal">
                            <div className="result-value-large">{results.num_vehicles}</div>
                            <div className="result-label-small">Vehicles</div>
                        </div>
                    </div>

                    {/* Road Routing Status */}
                    {results.used_real_roads && (
                        <div className="routing-status" style={{
                            padding: '8px 12px',
                            background: 'rgba(16, 185, 129, 0.1)',
                            borderRadius: '8px',
                            marginTop: '12px',
                            display: 'flex',
                            alignItems: 'center',
                            gap: '8px',
                            fontSize: '0.85rem',
                            color: '#10b981'
                        }}>
                            <span>✓</span>
                            <span>Using real road networks via OSRM</span>
                        </div>
                    )}

                    {/* Routes Breakdown */}
                    <div className="routes-list">
                        {results.routes.map((route, index) => (
                            <RouteCard
                                key={index}
                                route={route}
                                locations={locations}
                            />
                        ))}
                    </div>
                </motion.div>
            )}

            {/* Help Text */}
            {locationsCount === 0 && (
                <div className="help-section">
                    <p className="help-text">
                        <MapPin size={16} />
                        Click on the map or search to add locations
                    </p>
                </div>
            )}
        </div>
    );
};

// Collapsible Route Card Component
const RouteCard = ({ route, locations }) => {
    const [isExpanded, setIsExpanded] = useState(false);

    return (
        <div
            className="route-card-minimal"
            style={{ borderLeftColor: route.color }}
        >
            <button
                className="route-header-minimal clickable"
                onClick={() => setIsExpanded(!isExpanded)}
            >
                <div className="route-header-left">
                    <Truck size={16} style={{ color: route.color }} />
                    <span className="route-name">Vehicle {route.vehicle_id + 1}</span>
                </div>
                <motion.div
                    animate={{ rotate: isExpanded ? 180 : 0 }}
                    transition={{ duration: 0.2 }}
                >
                    <ChevronDown size={16} />
                </motion.div>
            </button>

            <div className="route-stats-minimal">
                <span>{route.distance_km} km</span>
                {route.duration_minutes && (
                    <>
                        <span>•</span>
                        <span>{Math.round(route.duration_minutes)} min</span>
                    </>
                )}
                <span>•</span>
                <span>{route.emissions_kg} kg CO₂</span>
                <span>•</span>
                <span>{route.route.length - 2} stops</span>
            </div>

            {/* Collapsible Route Details */}
            <motion.div
                initial={false}
                animate={{
                    height: isExpanded ? 'auto' : 0,
                    opacity: isExpanded ? 1 : 0
                }}
                transition={{ duration: 0.3, ease: 'easeInOut' }}
                style={{ overflow: 'hidden' }}
            >
                <div className="route-details">
                    <div className="route-path">
                        {route.route.map((stopIndex, idx) => {
                            const location = locations[stopIndex];
                            const isFirst = idx === 0;
                            const isLast = idx === route.route.length - 1;
                            const isDepot = isFirst || isLast;

                            return (
                                <div key={idx} className="route-stop">
                                    <div className="stop-indicator">
                                        <div
                                            className={`stop-dot ${isDepot ? 'depot' : 'delivery'}`}
                                            style={{
                                                backgroundColor: isDepot ? route.color : 'transparent',
                                                borderColor: route.color
                                            }}
                                        />
                                        {idx < route.route.length - 1 && (
                                            <div
                                                className="stop-line"
                                                style={{ backgroundColor: route.color }}
                                            />
                                        )}
                                    </div>
                                    <div className="stop-info">
                                        <div className="stop-label">
                                            {isFirst ? '🏭 Start' : isLast ? '🏭 Return' : `📦 Stop ${idx}`}
                                        </div>
                                        <div className="stop-name">{location?.label || `Location ${stopIndex}`}</div>
                                        <div className="stop-coords">
                                            {location?.lat.toFixed(4)}, {location?.lng.toFixed(4)}
                                        </div>
                                    </div>
                                </div>
                            );
                        })}
                    </div>
                </div>
            </motion.div>
        </div>
    );
};

export default ControlPanel;
