class EPIProcessorSimulator:
    """Simulate European Processor Initiative RISC-V processors"""
    
    def __init__(self):
        self.epi_models = {
            'Rhea': {'cores': 32, 'tflops': 0.5, 'power_w': 75, 'type': 'General Purpose'},
            'Zeus': {'cores': 128, 'tflops': 2.5, 'power_w': 250, 'type': 'Accelerator'},
            'Poseidon': {'cores': 512, 'tflops': 12.0, 'power_w': 800, 'type': 'Vector Processor'}
        }
    
    def simulate_epi_performance(self, model, workload_tflops):
        """Simulate EPI processor performance"""
        epi = self.epi_models.get(model, self.epi_models['Rhea'])
        
        compute_time = workload_tflops / epi['tflops']
        energy_consumed = epi['power_w'] * compute_time / 3600
        
        return {
            'processor': model,
            'compute_time_hours': round(compute_time, 2),
            'energy_kwh': round(energy_consumed, 3),
            'efficiency': round(workload_tflops / epi['power_w'], 2),
            'eurohpc_ready': True
        }
    
    def compare_with_x86(self, epi_model, x86_tflops, workload):
        """Compare EPI with traditional x86 processors"""
        epi_perf = self.simulate_epi_performance(epi_model, workload)
        x86_time = workload / x86_tflops
        x86_energy = 200 * x86_time / 3600
        
        return {
            'epi_faster': epi_perf['compute_time_hours'] < x86_time,
            'epi_energy_savings': round((x86_energy - epi_perf['energy_kwh']) / x86_energy * 100, 1) if x86_energy > 0 else 0,
            'eurohpc_recommended': epi_perf['compute_time_hours'] < x86_time
        }
