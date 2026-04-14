"""European HPC Standards and Compliance Module"""

class EuropeanHPCStandards:
    """Implements EuroHPC JU and PRACE standards"""
    
    def __init__(self):
        self.eurohpc_tiers = {
            'Tier-0': 'Leadership-class (Exascale) - 10+ PFLOPS',
            'Tier-1': 'National capability - 1-10 PFLOPS', 
            'Tier-2': 'Regional/University - 0.1-1 PFLOPS',
            'Tier-3': 'Departmental - <0.1 PFLOPS'
        }
        
        self.prace_metrics = {
            'scaling_efficiency': 0.70,
            'parallel_efficiency': 0.60,
            'load_balance': 0.85,
            'memory_bound': 0.30
        }
    
    def check_eurohpc_compliance(self, performance_metrics):
        """Check if system meets EuroHPC standards"""
        compliance = {
            'meets_tier_0': performance_metrics.get('pflops', 0) >= 10,
            'meets_tier_1': performance_metrics.get('pflops', 0) >= 1,
            'green500_ready': performance_metrics.get('gflops_per_watt', 0) >= 10,
            'energy_efficient': performance_metrics.get('pue', 1.5) <= 1.2,
            'scalable': performance_metrics.get('scaling_efficiency', 0) >= 0.7
        }
        return compliance
    
    def get_eurohpc_requirements(self):
        """Return EuroHPC JU requirements"""
        return {
            'processor': 'EPI (European Processor Initiative) or equivalent',
            'interconnect': 'InfiniBand EDR/HDR or Slingshot',
            'storage': 'Burst buffer + parallel FS (Lustre/BeeGFS)',
            'energy': 'Maximum 20 MW for Exascale systems',
            'cooling': 'Direct liquid cooling or immersion',
            'software': 'EUROHPC software stack (EESSI)'
        }
    
    def calculate_prace_score(self, system_metrics):
        """Calculate PRACE benchmarking score"""
        scores = {
            'hpl_score': system_metrics.get('hpl_tflops', 0) / system_metrics.get('peak_tflops', 1),
            'io_score': system_metrics.get('io_bw_gbps', 0) / 100,
            'memory_score': system_metrics.get('mem_bw_gbps', 0) / 500,
            'network_score': system_metrics.get('network_latency_us', 100) / 2,
        }
        
        overall_score = (scores['hpl_score'] * 0.4 + 
                        scores['io_score'] * 0.2 + 
                        scores['memory_score'] * 0.2 + 
                        scores['network_score'] * 0.2) * 100
        
        return {
            'overall_score': round(overall_score, 1),
            'rating': 'Gold' if overall_score > 80 else 'Silver' if overall_score > 60 else 'Bronze',
            'components': {k: round(v * 100, 1) for k, v in scores.items()}
        }

class OpenEBenchIntegration:
    """OpenEBench benchmarking integration"""
    
    def __init__(self):
        self.benchmarks = {
            'HPL': 'High-Performance Linpack (Top500)',
            'HPCG': 'High-Performance Conjugate Gradients',
            'Graph500': 'Graph analytics benchmark',
            'Green500': 'Energy efficiency ranking',
            'IO500': 'Storage performance'
        }
    
    def run_compliance_check(self, system_specs):
        """Run OpenEBench compliance checks"""
        return {
            'top500_compatible': system_specs.get('hpl_tflops', 0) > 100,
            'graph500_compatible': system_specs.get('graph_teps', 0) > 1000,
            'io500_compatible': system_specs.get('io_bw_gbps', 0) > 50,
            'green500_compatible': system_specs.get('gflops_per_watt', 0) > 20,
            'recommended_benchmarks': list(self.benchmarks.keys())
        }
