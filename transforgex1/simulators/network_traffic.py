"""
Scientific network traffic modeling for HPC interconnects
Based on:
- Dragonfly topology analysis (Kim et al., 2008)
- Fat-tree performance evaluation (Al-Fares et al., 2008)
- HPC communication patterns (Hoefler et al., 2015)
"""

import math
import random
from collections import defaultdict
from typing import List, Tuple

class ScientificNetworkModel:
    """Realistic network traffic simulation based on HPC literature"""
    
    def __init__(self):
        self.communication_patterns = {
            'nearest_neighbor': self.nearest_neighbor_pattern,
            'all_to_all': self.all_to_all_pattern,
            'butterfly': self.butterfly_pattern,
            'stencil': self.stencil_pattern,
            'fft': self.fft_pattern
        }
        
        # Dragonfly topology parameters (Kim et al., 2008)
        self.dragonfly_params = {
            'a': 12,  # routers per group
            'h': 8,   # hosts per router
            'g': 16   # groups
        }
        
        # Fat-tree parameters (Al-Fares et al., 2008)
        self.fat_tree_params = {
            'k': 8,    # number of ports
            'levels': 3
        }
    
    def nearest_neighbor_pattern(self, rank: int, size: int) -> List[int]:
        """1D nearest neighbor communication"""
        neighbors = []
        if rank > 0:
            neighbors.append(rank - 1)
        if rank < size - 1:
            neighbors.append(rank + 1)
        return neighbors
    
    def all_to_all_pattern(self, rank: int, size: int) -> List[int]:
        """All-to-all communication pattern"""
        return [i for i in range(size) if i != rank]
    
    def butterfly_pattern(self, rank: int, size: int) -> List[int]:
        """Butterfly network pattern for FFT"""
        neighbors = []
        step = 1
        while step < size:
            neighbor = rank ^ step
            if neighbor < size:
                neighbors.append(neighbor)
            step <<= 1
        return neighbors
    
    def stencil_pattern(self, rank: int, size: int) -> List[int]:
        """2D/3D stencil communication"""
        # Assume 2D grid for simplicity
        grid_size = int(math.sqrt(size))
        if rank < grid_size * grid_size:
            x = rank % grid_size
            y = rank // grid_size
            
            neighbors = []
            if x > 0: neighbors.append(rank - 1)
            if x < grid_size - 1: neighbors.append(rank + 1)
            if y > 0: neighbors.append(rank - grid_size)
            if y < grid_size - 1: neighbors.append(rank + grid_size)
            return neighbors
        return []
    
    def fft_pattern(self, rank: int, size: int) -> List[int]:
        """FFT communication pattern"""
        return self.butterfly_pattern(rank, size)
    
    def dragonfly_routing(self, source: int, dest: int) -> List[int]:
        """
        Dragonfly adaptive routing algorithm
        Based on Kim et al. "Technology-Driven, Highly-Scalable Dragonfly Topology"
        """
        groups = self.dragonfly_params['g']
        routers_per_group = self.dragonfly_params['a']
        
        src_group = source // (routers_per_group)
        dst_group = dest // (routers_per_group)
        
        path = [source]
        
        if src_group == dst_group:
            # Intra-group routing
            path.append(dest)
        else:
            # Inter-group routing via global links
            path.append(src_group * routers_per_group + (routers_per_group - 1))
            path.append(dst_group * routers_per_group)
            path.append(dest)
        
        return path
    
    def fat_tree_routing(self, source: int, dest: int, k: int = 8) -> List[int]:
        """Fat-tree deterministic routing (Al-Fares et al.)"""
        # Simplified fat-tree routing
        path = [source]
        
        # Go up to common ancestor
        # (Detailed implementation would use PODs and core switches)
        
        path.append(dest)
        return path
    
    def calculate_network_capacity(self, topology: str, nodes: int) -> Dict:
        """Calculate theoretical network capacity"""
        if topology == 'fat_tree':
            # Bisection bandwidth = k^3/4 for k-ary fat-tree
            k = int(math.pow(nodes * 4, 1/3))
            bisection_bandwidth = (k ** 3) / 4
            link_bandwidth = 100  # Gbps (InfiniBand EDR)
            
            return {
                'bisection_bandwidth_gbps': round(bisection_bandwidth * link_bandwidth, 2),
                'total_links': int(nodes * k / 2),
                'theoretical_capacity_tbps': round(bisection_bandwidth * link_bandwidth / 1000, 3),
                'scalability': 'O(N)',
                'reference': 'Al-Fares et al. "A Scalable, Commodity Data Center Network Architecture" (SIGCOMM 2008)'
            }
        
        elif topology == 'dragonfly':
            a, h, g = 12, 8, 16  # Default parameters
            routers = a * g
            total_nodes = routers * h
            
            # Global link bandwidth
            global_links = g * (g - 1) // 2
            link_bandwidth = 100  # Gbps
            
            return {
                'global_links': global_links,
                'routers': routers,
                'total_capacity_gbps': round(global_links * link_bandwidth, 2),
                'avg_hops': 2.5,  # Kim et al. results
                'diameter': 3,
                'reference': 'Kim et al. "Technology-Driven, Highly-Scalable Dragonfly Topology" (ISCA 2008)'
            }
        
        return {'error': 'Unknown topology'}
    
    def simulate_network_congestion(self, topology: str, traffic_matrix: List[Tuple[int, int]]) -> Dict:
        """Simulate network congestion using queueing theory"""
        # Simplified congestion model based on M/M/1 queues
        link_utilizations = defaultdict(float)
        link_counts = defaultdict(int)
        
        for src, dst in traffic_matrix:
            # Determine path length
            if topology == 'dragonfly':
                path_length = 3
            else:
                path_length = 2 * int(math.log2(len(traffic_matrix))) + 1
            
            # Update link utilization
            for hop in range(path_length):
                link_utilizations[hop] += 1
                link_counts[hop] += 1
        
        # Calculate congestion
        congestion = {}
        for hop, count in link_counts.items():
            utilization = link_utilizations[hop] / count if count > 0 else 0
            # M/M/1 queue length
            queue_length = utilization / (1 - utilization) if utilization < 1 else float('inf')
            congestion[hop] = {
                'utilization': round(utilization * 100, 2),
                'mean_queue_length': round(queue_length, 2) if queue_length != float('inf') else 'unstable'
            }
        
        return congestion
