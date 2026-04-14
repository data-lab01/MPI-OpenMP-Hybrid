"""
Hybrid MPI+OpenMP Simulation Model
Models modern HPC systems using hybrid programming model
"""

import math
from typing import Dict, List

class HybridSimulator:
    """Simulate hybrid MPI+OpenMP execution"""
    
    def __init__(self):
        self.node_configs = {
            'small': {'nodes': 4, 'cores_per_node': 16, 'mpi_ranks_per_node': 4, 'omp_threads_per_rank': 4},
            'medium': {'nodes': 16, 'cores_per_node': 32, 'mpi_ranks_per_node': 8, 'omp_threads_per_rank': 4},
            'large': {'nodes': 64, 'cores_per_node': 64, 'mpi_ranks_per_node': 16, 'omp_threads_per_rank': 4},
            'exascale': {'nodes': 1024, 'cores_per_node': 128, 'mpi_ranks_per_node': 32, 'omp_threads_per_rank': 4}
        }
    
    def analyze_hybrid_performance(self, config_name: str, workload_gflops: float, 
                                   communication_intensity: float = 0.3) -> Dict:
        """Analyze performance of hybrid MPI+OpenMP configuration"""
        
        config = self.node_configs.get(config_name, self.node_configs['medium'])
        
        total_cores = config['nodes'] * config['cores_per_node']
        mpi_ranks = config['nodes'] * config['mpi_ranks_per_node']
        omp_threads = config['omp_threads_per_rank']
        
        # Theoretical peak (assuming 10 GFLOPS per core)
        theoretical_peak = total_cores * 10
        
        # Communication overhead (MPI)
        mpi_overhead = communication_intensity * math.log2(mpi_ranks)
        
        # OpenMP overhead
        omp_overhead = 0.02 * omp_threads
        
        # Shared memory efficiency
        smp_efficiency = 0.95 ** math.log2(omp_threads)
        
        # Overall parallel efficiency
        parallel_efficiency = (1 - mpi_overhead) * smp_efficiency * (1 - omp_overhead)
        
        # Strong scaling speedup
        speedup = min(total_cores, workload_gflops / 10) * parallel_efficiency
        
        # Weak scaling (problem size grows with cores)
        weak_scaling = 0.95 ** math.log2(total_cores / 100)
        
        return {
            'config_name': config_name,
            'total_nodes': config['nodes'],
            'total_cores': total_cores,
            'mpi_ranks': mpi_ranks,
            'omp_threads_per_rank': omp_threads,
            'theoretical_peak_gflops': theoretical_peak,
            'parallel_efficiency': round(parallel_efficiency * 100, 1),
            'speedup': round(speedup, 2),
            'mpi_overhead': round(mpi_overhead * 100, 1),
            'omp_overhead': round(omp_overhead * 100, 1),
            'smp_efficiency': round(smp_efficiency * 100, 1),
            'weak_scaling_efficiency': round(weak_scaling * 100, 1),
            'recommended_balance': self.get_balance_recommendation(config)
        }
    
    def get_balance_recommendation(self, config: Dict) -> str:
        """Recommend MPI vs OpenMP balance"""
        mpi_ranks = config['nodes'] * config['mpi_ranks_per_node']
        omp_threads = config['omp_threads_per_rank']
        
        if mpi_ranks > 100 and omp_threads < 8:
            return "Increase OpenMP threads to reduce communication"
        elif mpi_ranks < 50 and omp_threads > 16:
            return "Consider more MPI ranks for better load balancing"
        else:
            return "Good balance between MPI and OpenMP"
    
    def optimize_configuration(self, total_cores: int, workload_type: str) -> Dict:
        """Find optimal MPI/OpenMP configuration for given workload"""
        
        configurations = []
        
        # Test different MPI rank / OpenMP thread ratios
        for mpi_ranks in [1, 2, 4, 8, 16, 32, 64, 128]:
            if mpi_ranks > total_cores:
                break
            omp_threads = total_cores // mpi_ranks
            
            # Calculate efficiency based on workload type
            if workload_type == 'computation_intensive':
                mpi_cost = 0.1 * math.log2(mpi_ranks)
                omp_benefit = 0.9 * (1 - 1/omp_threads)
                efficiency = (1 - mpi_cost) * omp_benefit
                
            elif workload_type == 'communication_intensive':
                mpi_cost = 0.3 * math.log2(mpi_ranks)
                omp_benefit = 0.7 * (1 - 1/omp_threads)
                efficiency = (1 - mpi_cost) * omp_benefit
                
            else:  # balanced
                mpi_cost = 0.15 * math.log2(mpi_ranks)
                omp_benefit = 0.85 * (1 - 1/omp_threads)
                efficiency = (1 - mpi_cost) * omp_benefit
            
            configurations.append({
                'mpi_ranks': mpi_ranks,
                'omp_threads': omp_threads,
                'efficiency': round(efficiency * 100, 1),
                'nodes': math.ceil(mpi_ranks / 16),  # Assume 16 ranks per node
                'communication_overhead': round(mpi_cost * 100, 1)
            })
        
        # Find best configuration
        best = max(configurations, key=lambda x: x['efficiency'])
        
        return {
            'optimal_config': best,
            'alternatives': sorted(configurations, key=lambda x: x['efficiency'], reverse=True)[:5],
            'workload_type': workload_type,
            'total_cores': total_cores
        }
    
    def compare_parallel_models(self, cores: int, workload_gflops: float) -> Dict:
        """Compare pure MPI, pure OpenMP, and Hybrid approaches"""
        
        # Pure MPI (1 thread per rank)
        mpi_ranks = cores
        omp_threads = 1
        mpi_overhead = 0.2 * math.log2(mpi_ranks)
        mpi_speedup = cores / (1 + mpi_overhead)
        
        # Pure OpenMP (1 rank, shared memory)
        omp_ranks = 1
        omp_threads = cores
        omp_overhead = 0.05 * omp_threads
        omp_speedup = cores / (1 + omp_overhead) * 0.95  # Shared memory overhead
        
        # Hybrid (balanced)
        hybrid_ranks = int(math.sqrt(cores))
        hybrid_threads = cores // hybrid_ranks
        hybrid_overhead = 0.1 * math.log2(hybrid_ranks) + 0.02 * hybrid_threads
        hybrid_speedup = cores / (1 + hybrid_overhead)
        
        return {
            'pure_mpi': {
                'speedup': round(mpi_speedup, 2),
                'efficiency': round(mpi_speedup / cores * 100, 1),
                'description': 'One MPI rank per core'
            },
            'pure_openmp': {
                'speedup': round(omp_speedup, 2),
                'efficiency': round(omp_speedup / cores * 100, 1),
                'description': 'Shared memory across all cores'
            },
            'hybrid': {
                'mpi_ranks': hybrid_ranks,
                'omp_threads': hybrid_threads,
                'speedup': round(hybrid_speedup, 2),
                'efficiency': round(hybrid_speedup / cores * 100, 1),
                'description': f'{hybrid_ranks} MPI ranks × {hybrid_threads} OpenMP threads'
            },
            'best_model': 'hybrid' if hybrid_speedup > max(mpi_speedup, omp_speedup) else 'mpi' if mpi_speedup > omp_speedup else 'openmp',
            'recommendation': self.get_model_recommendation(cores, workload_gflops)
        }
    
    def get_model_recommendation(self, cores: int, workload_gflops: float) -> str:
        """Get recommendation based on system size and workload"""
        if cores < 64:
            return "Pure OpenMP is sufficient for small-scale parallelism"
        elif cores < 256:
            return "Hybrid MPI+OpenMP recommended for moderate scale"
        elif cores < 2048:
            return "Use MPI with moderate OpenMP (4-8 threads per rank)"
        else:
            return "MPI-dominant with 2-4 OpenMP threads per rank for large scale"
