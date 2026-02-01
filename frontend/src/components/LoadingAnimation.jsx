import { motion } from 'framer-motion';
import './LoadingAnimation.css';

const LoadingAnimation = () => {
    return (
        <div className="loading-overlay">
            <div className="loading-container">
                {/* Quantum qubits visualization */}
                <div className="qubits-container">
                    {[0, 1, 2].map((i) => (
                        <motion.div
                            key={i}
                            className="qubit"
                            animate={{
                                scale: [1, 1.2, 1],
                                rotate: [0, 360],
                            }}
                            transition={{
                                duration: 2,
                                repeat: Infinity,
                                delay: i * 0.2,
                                ease: "easeInOut"
                            }}
                        >
                            <div className="qubit-inner"></div>
                        </motion.div>
                    ))}

                    {/* Entanglement lines */}
                    <svg className="entanglement-lines" viewBox="0 0 200 100">
                        <motion.path
                            d="M 50 50 Q 100 20, 150 50"
                            stroke="url(#gradient1)"
                            strokeWidth="2"
                            fill="none"
                            initial={{ pathLength: 0, opacity: 0 }}
                            animate={{ pathLength: 1, opacity: 1 }}
                            transition={{
                                duration: 1.5,
                                repeat: Infinity,
                                repeatType: "reverse",
                                ease: "easeInOut"
                            }}
                        />
                        <motion.path
                            d="M 50 50 Q 100 80, 150 50"
                            stroke="url(#gradient2)"
                            strokeWidth="2"
                            fill="none"
                            initial={{ pathLength: 0, opacity: 0 }}
                            animate={{ pathLength: 1, opacity: 1 }}
                            transition={{
                                duration: 1.5,
                                repeat: Infinity,
                                repeatType: "reverse",
                                delay: 0.3,
                                ease: "easeInOut"
                            }}
                        />
                        <defs>
                            <linearGradient id="gradient1" x1="0%" y1="0%" x2="100%" y2="0%">
                                <stop offset="0%" stopColor="#6366f1" stopOpacity="0.2" />
                                <stop offset="50%" stopColor="#8b5cf6" stopOpacity="0.8" />
                                <stop offset="100%" stopColor="#06b6d4" stopOpacity="0.2" />
                            </linearGradient>
                            <linearGradient id="gradient2" x1="0%" y1="0%" x2="100%" y2="0%">
                                <stop offset="0%" stopColor="#06b6d4" stopOpacity="0.2" />
                                <stop offset="50%" stopColor="#6366f1" stopOpacity="0.8" />
                                <stop offset="100%" stopColor="#8b5cf6" stopOpacity="0.2" />
                            </linearGradient>
                        </defs>
                    </svg>
                </div>

                {/* Loading text */}
                <motion.div
                    className="loading-text"
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ delay: 0.3 }}
                >
                    <h3>Entangling Qubits...</h3>
                    <p className="text-muted">Quantum optimization in progress</p>
                </motion.div>

                {/* Progress indicator */}
                <motion.div
                    className="progress-bar"
                    initial={{ width: 0 }}
                    animate={{ width: "100%" }}
                    transition={{
                        duration: 2,
                        repeat: Infinity,
                        ease: "easeInOut"
                    }}
                />
            </div>
        </div>
    );
};

export default LoadingAnimation;
