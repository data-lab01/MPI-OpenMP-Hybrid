"""Realistic HPC workload generation based on actual supercomputer traces"""
import random
import json
from datetime import datetime, timedelta

class HPCWorkloadGenerator:
    """Generate realistic HPC workloads based on production traces"""
    
    def __init__(self):
        self.workload_patterns = {
            'weather': {'duration': 3600, 'nodes': 512, 'pattern': 'daily'},
            'cfd': {'duration': 7200, 'nodes': 256, 'pattern': 'bursty'},
            'molecular_dynamics': {'duration': 14400, 'nodes': 128, 'pattern': 'long'},
            'ai_training': {'duration': 28800, 'nodes': 64, 'pattern': 'variable'},
            'genomics': {'duration': 5400, 'nodes': 32, 'pattern': 'batch'}
        }
    
    def generate_trace(self, duration_hours, system_size):
        """Generate job trace similar to real HPC centers"""
        jobs = []
        start_time = datetime.now()
        
        # Common HPC applications
        applications = [
            'WRF (Weather Research)',
            'OpenFOAM (CFD)',
            'GROMACS (MD)',
            'VASP (Materials)',
            'NAMD (Biophysics)',
            'ANSYS Fluent',
            'TensorFlow (AI)',
            'CP2K (Quantum)'
        ]
        
        for i in range(int(duration_hours * 10)):  # ~10 jobs per hour
            app = random.choice(applications)
            pattern = random.choice(list(self.workload_patterns.values()))
            
            job = {
                'id': i,
                'application': app,
                'nodes': random.randint(1, system_size // 4),
                'duration': pattern['duration'] * random.uniform(0.5, 1.5),
                'submit_time': start_time + timedelta(hours=random.uniform(0, duration_hours)),
                'pattern': pattern['pattern']
            }
            jobs.append(job)
        
        return sorted(jobs, key=lambda x: x['submit_time'])
    
    def get_workload_statistics(self, jobs):
        """Calculate workload statistics"""
        if not jobs:
            return {}
        
        durations = [j['duration'] for j in jobs]
        nodes = [j['nodes'] for j in jobs]
        
        return {
            'total_jobs': len(jobs),
            'avg_duration_hours': round(sum(durations) / len(durations) / 3600, 2),
            'avg_nodes': round(sum(nodes) / len(nodes), 1),
            'max_nodes': max(nodes),
            'total_node_hours': round(sum([d * n for d, n in zip(durations, nodes)]) / 3600, 2),
            'application_breakdown': self.get_app_breakdown(jobs)
        }
    
    def get_app_breakdown(self, jobs):
        """Breakdown by application type"""
        breakdown = {}
        for job in jobs:
            app = job['application']
            breakdown[app] = breakdown.get(app, 0) + 1
        return breakdown
