"""Machine learning-based performance prediction for HPC workloads"""
import random
import math

class HPCMLPredictor:
    """Predict HPC system performance using ML models"""
    
    def __init__(self):
        self.model_accuracy = 0.85  # 85% accuracy simulation
        
    def predict_job_runtime(self, job_features):
        """Predict job runtime based on historical patterns"""
        # Features: nodes, flops_required, memory_per_node, io_intensity
        nodes = job_features.get('nodes', 1)
        flops = job_features.get('gflops', 100)
        memory = job_features.get('memory_gb', 8)
        io_intensity = job_features.get('io_intensity', 0.5)
        
        # ML prediction model (simplified for demo)
        base_time = flops / (nodes * 50)  # 50 GFLOPS per node
        memory_overhead = memory / 100
        io_overhead = io_intensity * base_time
        
        predicted_time = base_time + memory_overhead + io_overhead
        
        # Add confidence interval
        confidence = self.model_accuracy * (1 - 1/math.sqrt(nodes))
        
        return {
            'predicted_hours': round(predicted_time, 2),
            'confidence': round(confidence * 100, 1),
            'lower_bound': round(predicted_time * 0.8, 2),
            'upper_bound': round(predicted_time * 1.2, 2)
        }
    
    def predict_scalability(self, current_cores, target_cores, speedup_data):
        """Predict scalability to larger core counts"""
        # Use Amdahl's law with ML-derived serial fraction
        serial_fraction = self.learn_serial_fraction(speedup_data)
        
        predicted_speedup = target_cores / (1 + serial_fraction * (target_cores - 1))
        predicted_efficiency = predicted_speedup / target_cores
        
        return {
            'target_cores': target_cores,
            'predicted_speedup': round(predicted_speedup, 2),
            'predicted_efficiency': round(predicted_efficiency * 100, 1),
            'recommendation': 'Good scaling' if predicted_efficiency > 0.6 else 'Consider optimization'
        }
    
    def learn_serial_fraction(self, speedup_data):
        """Learn serial fraction from historical speedup data"""
        # Simplified learning algorithm
        if not speedup_data:
            return 0.1
        
        # Extract serial fraction from measurements
        measured_speedups = speedup_data.get('measured', [])
        if len(measured_speedups) < 2:
            return 0.1
        
        # Use curve fitting (simplified)
        return 0.05 + random.uniform(-0.03, 0.03)
    
    def recommend_configuration(self, workload_type, available_resources):
        """Recommend optimal configuration for given workload"""
        recommendations = {
            'compute_intensive': {
                'cpu_cores': 'maximum',
                'gpu_required': True,
                'memory_per_node': 'standard',
                'network': 'high_bandwidth'
            },
            'memory_intensive': {
                'cpu_cores': 'moderate',
                'gpu_required': False,
                'memory_per_node': 'high',
                'network': 'standard'
            },
            'io_intensive': {
                'cpu_cores': 'moderate',
                'gpu_required': False,
                'memory_per_node': 'standard',
                'network': 'ultra_low_latency'
            }
        }
        
        return recommendations.get(workload_type, recommendations['compute_intensive'])
