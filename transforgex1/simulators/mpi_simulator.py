"""
MPI (Message Passing Interface) Communication Simulator
Models collective operations, point-to-point communication, and network contention
Based on MPI-3.1 standard and real HPC communication patterns
"""

import math
import random
from typing import List, Dict, Tuple
from dataclasses import dataclass

@dataclass
class MPICommunication:
    """Represents an MPI communication event"""
    operation: str  # Send, Recv, Broadcast, Reduce, Alltoall, Barrier
    source: int
    dest: int
    size_mb: float
    time_us: float
    bytes_transferred: int

class MPISimulator:
    """Simulate MPI communication patterns and collective operations"""
    
    def __init__(self):
        # MPI operation latency models (microseconds)
        self.latency_model = {
            'point_to_point': 1.5,      # μs base latency
            'broadcast': 2.0,           # μs per message
            'reduce': 2.5,              # μs per reduction
            'alltoall': 5.0,            # μs base
            'barrier': 3.0,             # μs synchronization
            'allreduce': 4.0,           # μs combined
            'scatter': 2.0,             # μs distribution
            'gather': 2.0               # μs collection
        }
        
        # Bandwidth in MB/s (InfiniBand HDR = 200 Gbps = 25000 MB/s)
        self.bandwidth_mbps = 25000
        
        # Network topology awareness
        self.topology_penalty = {
            'same_node': 1.0,
            'same_switch': 1.2,
            'same_rack': 1.5,
            'cross_rack': 2.0,
            'cross_domain': 3.0
        }
    
    def point_to_point(self, source: int, dest: int, size_mb: float, topology: str = 'same_switch') -> Dict:
        """Simulate MPI_Send/MPI_Recv point-to-point communication"""
        # Calculate communication time
        latency = self.latency_model['point_to_point']
        transfer_time = size_mb / self.bandwidth_mbps * 1000  # Convert to μs
        topology_factor = self.topology_penalty.get(topology, 1.5)
        
        total_time = (latency + transfer_time) * topology_factor
        
        return {
            'operation': 'Point-to-Point',
            'source': source,
            'destination': dest,
            'size_mb': size_mb,
            'time_us': round(total_time, 2),
            'bandwidth_used_mbps': round(size_mb / (transfer_time / 1000), 2),
            'latency_us': latency,
            'topology': topology
        }
    
    def broadcast(self, root: int, size_mb: float, num_processes: int, topology: str = 'same_switch') -> Dict:
        """Simulate MPI_Bcast collective operation"""
        # MPI_Bcast time = (latency + bandwidth * size) * log2(P)
        latency = self.latency_model['broadcast']
        transfer_time = size_mb / self.bandwidth_mbps * 1000
        
        # Logarithmic scaling for tree-based broadcast
        log_p = math.log2(num_processes)
        total_time = (latency + transfer_time) * log_p
        
        topology_factor = self.topology_penalty.get(topology, 1.5)
        total_time *= topology_factor
        
        return {
            'operation': 'MPI_Bcast',
            'root': root,
            'size_mb': size_mb,
            'num_processes': num_processes,
            'time_us': round(total_time, 2),
            'bandwidth_mbps': round(self.bandwidth_mbps, 2),
            'scaling': f'O(log P) = {log_p:.2f}',
            'formula': f'Time = (latency + size/BW) * log2(P) = ({latency} + {size_mb}/25000) * {log_p:.2f}'
        }
    
    def reduce(self, root: int, size_mb: float, num_processes: int, operation: str = 'MPI_Sum') -> Dict:
        """Simulate MPI_Reduce collective operation"""
        latency = self.latency_model['reduce']
        transfer_time = size_mb / self.bandwidth_mbps * 1000
        
        # Reduction uses tree algorithm
        log_p = math.log2(num_processes)
        total_time = (latency + transfer_time) * log_p
        
        return {
            'operation': 'MPI_Reduce',
            'reduce_op': operation,
            'root': root,
            'size_mb': size_mb,
            'num_processes': num_processes,
            'time_us': round(total_time, 2),
            'complexity': f'O(log P) = {log_p:.2f}'
        }
    
    def alltoall(self, size_mb: float, num_processes: int) -> Dict:
        """Simulate MPI_Alltoall (each process sends to all others)"""
        # All-to-all is more expensive: O(P) per process
        latency = self.latency_model['alltoall']
        transfer_time = size_mb / self.bandwidth_mbps * 1000
        
        # Each process sends to P-1 others
        total_time = (latency + transfer_time) * (num_processes - 1)
        
        return {
            'operation': 'MPI_Alltoall',
            'size_mb': size_mb,
            'num_processes': num_processes,
            'time_us': round(total_time, 2),
            'total_data_mb': round(size_mb * num_processes, 2),
            'complexity': f'O(P) = {num_processes - 1}'
        }
    
    def barrier(self, num_processes: int) -> Dict:
        """Simulate MPI_Barrier synchronization"""
        latency = self.latency_model['barrier']
        
        # Barrier time scales with log P
        log_p = math.log2(num_processes)
        total_time = latency * log_p
        
        return {
            'operation': 'MPI_Barrier',
            'num_processes': num_processes,
            'time_us': round(total_time, 2),
            'synchronization_cost': f'{latency} * log2(P) = {total_time:.2f} μs'
        }
    
    def allreduce(self, size_mb: float, num_processes: int, operation: str = 'MPI_Sum') -> Dict:
        """Simulate MPI_Allreduce (reduce + broadcast combined)"""
        # Allreduce = Reduce + Broadcast = 2 * log P
        latency = self.latency_model['allreduce']
        transfer_time = size_mb / self.bandwidth_mbps * 1000
        
        log_p = math.log2(num_processes)
        total_time = (latency + transfer_time) * 2 * log_p
        
        return {
            'operation': 'MPI_Allreduce',
            'reduce_op': operation,
            'size_mb': size_mb,
            'num_processes': num_processes,
            'time_us': round(total_time, 2),
            'formula': 'Time = 2 * (latency + size/BW) * log2(P)'
        }
    
    def estimate_communication_overhead(self, mpi_operations: List[Dict]) -> Dict:
        """Estimate total communication overhead"""
        total_time = sum(op.get('time_us', 0) for op in mpi_operations)
        total_data = sum(op.get('size_mb', 0) for op in mpi_operations)
        
        return {
            'total_time_ms': round(total_time / 1000, 3),
            'total_data_gb': round(total_data / 1024, 3),
            'effective_bandwidth_gbps': round(total_data / (total_time / 1e6) / 125, 2) if total_time > 0 else 0,
            'num_operations': len(mpi_operations)
        }
    
    def compare_collectives(self, size_mb: float, num_processes: int) -> Dict:
        """Compare performance of different collective operations"""
        return {
            'broadcast': self.broadcast(0, size_mb, num_processes),
            'reduce': self.reduce(0, size_mb, num_processes),
            'alltoall': self.alltoall(size_mb, num_processes),
            'barrier': self.barrier(num_processes),
            'allreduce': self.allreduce(size_mb, num_processes)
        }

class OpenMPSimulator:
    """Simulate OpenMP shared-memory parallelism"""
    
    def __init__(self):
        self.scheduling_policies = {
            'static': 'Fixed chunk size, round-robin distribution',
            'dynamic': 'Dynamic assignment of iterations to threads',
            'guided': 'Decreasing chunk size, starting large',
            'auto': 'Compiler/runtime decides',
            'runtime': 'Environment variable determines policy'
        }
        
        self.omp_constructs = {
            'parallel': 'Creates team of threads',
            'for': 'Distributes loop iterations',
            'sections': 'Independent code blocks',
            'single': 'Executed by one thread',
            'task': 'Explicit tasks',
            'simd': 'SIMD vectorization'
        }
    
    def parallel_region(self, num_threads: int, workload_gflops: float) -> Dict:
        """Simulate OpenMP parallel region performance"""
        # Amdahl's law with OpenMP overhead
        overhead = 0.05  # 5% OpenMP overhead
        serial_fraction = 0.02  # 2% serial portion
        
        ideal_speedup = num_threads
        actual_speedup = 1.0 / (serial_fraction + (1 - serial_fraction) / num_threads)
        
        # Add OpenMP runtime overhead
        actual_speedup *= (1 - overhead)
        
        execution_time = workload_gflops / (actual_speedup * 10)  # 10 GFLOPS per thread base
        
        return {
            'num_threads': num_threads,
            'workload_gflops': workload_gflops,
            'ideal_speedup': round(ideal_speedup, 2),
            'actual_speedup': round(actual_speedup, 2),
            'efficiency': round(actual_speedup / ideal_speedup * 100, 1),
            'execution_time_seconds': round(execution_time, 3),
            'overhead_percent': overhead * 100
        }
    
    def loop_schedule(self, num_iterations: int, num_threads: int, schedule_type: str = 'static', chunk_size: int = None) -> Dict:
        """Simulate different OpenMP loop scheduling policies"""
        
        # Calculate iteration distribution
        if schedule_type == 'static':
            iterations_per_thread = num_iterations // num_threads
            remainder = num_iterations % num_threads
            distribution = [iterations_per_thread + (1 if i < remainder else 0) for i in range(num_threads)]
            load_balance = max(distribution) / min(distribution) if min(distribution) > 0 else 1.0
            
        elif schedule_type == 'dynamic':
            # Dynamic has better load balance but more overhead
            distribution = [num_iterations // num_threads + random.randint(-5, 5) for _ in range(num_threads)]
            load_balance = 1.1  # ~10% imbalance due to overhead
            
        elif schedule_type == 'guided':
            # Guided starts with large chunks, decreases
            distribution = []
            remaining = num_iterations
            for i in range(num_threads):
                chunk = max(1, remaining // (num_threads - i) // 2)
                distribution.append(min(chunk, remaining))
                remaining -= chunk
            load_balance = max(distribution) / min(distribution) if min(distribution) > 0 else 1.0
        
        else:
            distribution = [num_iterations // num_threads] * num_threads
            load_balance = 1.0
        
        overhead_us = {
            'static': 50,
            'dynamic': 200,
            'guided': 150,
            'auto': 100,
            'runtime': 120
        }.get(schedule_type, 100)
        
        return {
            'schedule_type': schedule_type,
            'num_iterations': num_iterations,
            'num_threads': num_threads,
            'distribution': distribution,
            'load_balance': round(load_balance, 2),
            'overhead_us': overhead_us,
            'description': self.scheduling_policies.get(schedule_type, 'Unknown'),
            'recommended_for': self.get_schedule_recommendation(schedule_type, num_iterations, num_threads)
        }
    
    def get_schedule_recommendation(self, schedule_type: str, iterations: int, threads: int) -> str:
        """Get recommendation for schedule type"""
        recommendations = {
            'static': f'Good for {iterations} iterations with regular workload',
            'dynamic': f'Best for irregular workloads with {iterations} iterations',
            'guided': f'Good balance for {iterations} iterations on {threads} threads',
            'auto': f'Let compiler decide for {iterations} iterations'
        }
        return recommendations.get(schedule_type, 'Use for general purpose')
    
    def task_parallelism(self, num_tasks: int, num_threads: int, task_granularity: str = 'medium') -> Dict:
        """Simulate OpenMP task-based parallelism"""
        # Task overhead based on granularity
        granularity_overhead = {
            'fine': 0.30,    # 30% overhead
            'medium': 0.15,  # 15% overhead
            'coarse': 0.05   # 5% overhead
        }.get(task_granularity, 0.15)
        
        # Task scheduling overhead
        scheduling_overhead = num_tasks * 10  # 10 μs per task
        
        # Parallel efficiency with tasks
        ideal_speedup = min(num_tasks, num_threads)
        actual_speedup = ideal_speedup * (1 - granularity_overhead)
        
        return {
            'num_tasks': num_tasks,
            'num_threads': num_threads,
            'task_granularity': task_granularity,
            'overhead_percent': granularity_overhead * 100,
            'ideal_speedup': round(ideal_speedup, 2),
            'actual_speedup': round(actual_speedup, 2),
            'scheduling_overhead_us': scheduling_overhead,
            'recommendation': 'Use coarse granularity for best performance' if granularity_overhead > 0.2 else 'Granularity is appropriate'
        }
    
    def compare_schedules(self, num_iterations: int, num_threads: int) -> Dict:
        """Compare all scheduling policies"""
        schedules = ['static', 'dynamic', 'guided', 'auto']
        results = {}
        
        for schedule in schedules:
            results[schedule] = self.loop_schedule(num_iterations, num_threads, schedule)
        
        return results
