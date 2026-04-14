import math

class AlgorithmSimulator:
    def __init__(self):
        pass
    
    def compute(self, algorithm, cores, serial_time, overhead):
        if algorithm == 'amdahl':
            return self.amdahl_with_explanation(cores, serial_time)
        elif algorithm == 'gustafson':
            return self.gustafson_with_explanation(cores, serial_time)
        elif algorithm == 'scalability':
            return self.scalability_with_explanation(cores, overhead)
        return {}
    
    def amdahl_with_explanation(self, cores, serial_time):
        # Calculate serial fraction
        total_time = 1000.0  # Base total time
        serial_fraction = serial_time / total_time
        parallel_fraction = 1 - serial_fraction
        
        # Amdahl's Law formula: Speedup = 1 / (S + (1-S)/N)
        speedup = 1.0 / (serial_fraction + parallel_fraction / cores)
        efficiency = (speedup / cores) * 100
        
        # Generate data points
        core_range = list(range(1, min(cores, 128) + 1))
        speedups = [1.0 / (serial_fraction + (1.0 - serial_fraction) / c) for c in core_range]
        ideal = [c for c in core_range]
        
        # Detailed explanation
        explanation = {
            'title': 'Amdahl\'s Law - Theoretical Speedup Limit',
            'law': 'Speedup = 1 / (S + (1-S)/N)',
            'derivation': f'''
                Given:
                - Serial portion (S) = {serial_fraction:.3f} ({serial_fraction*100:.1f}%)
                - Parallel portion (1-S) = {parallel_fraction:.3f} ({parallel_fraction*100:.1f}%)
                - Number of processors (N) = {cores}
                
                Step 1: Calculate parallel execution time
                T_parallel = (1-S)/N = {parallel_fraction:.4f} / {cores} = {parallel_fraction/cores:.4f}
                
                Step 2: Add serial portion
                T_total = S + (1-S)/N = {serial_fraction:.4f} + {parallel_fraction/cores:.4f} = {serial_fraction + parallel_fraction/cores:.4f}
                
                Step 3: Calculate speedup
                Speedup = 1 / T_total = 1 / {serial_fraction + parallel_fraction/cores:.4f} = {speedup:.2f}
            ''',
            'interpretation': f'''
                With {cores} cores, the maximum speedup is {speedup:.2f}x.
                Even with infinite cores, speedup is limited to 1/S = {1/serial_fraction:.1f}x.
                This demonstrates the fundamental limitation of parallel computing -
                the serial portion creates an upper bound on performance improvement.
            ''',
            'limitation': 'Amdahl\'s Law assumes fixed problem size, which is often unrealistic for large-scale HPC.'
        }
        
        return {
            'speedup': round(speedup, 2),
            'efficiency': round(efficiency, 1),
            'serial_fraction': round(serial_fraction * 100, 1),
            'parallel_fraction': round(parallel_fraction * 100, 1),
            'max_speedup': round(1/serial_fraction, 1),
            'core_range': core_range,
            'speedups': speedups,
            'ideal': ideal,
            'explanation': explanation
        }
    
    def gustafson_with_explanation(self, cores, serial_time):
        total_time = 1000.0
        serial_fraction = serial_time / total_time
        parallel_fraction = 1 - serial_fraction
        
        # Gustafson's Law: Speedup = N - S*(N-1)
        speedup = cores - serial_fraction * (cores - 1)
        efficiency = (speedup / cores) * 100
        
        core_range = list(range(1, min(cores, 128) + 1))
        speedups = [c - serial_fraction * (c - 1) for c in core_range]
        ideal = [c for c in core_range]
        
        explanation = {
            'title': 'Gustafson\'s Law - Scaled Speedup',
            'law': 'Speedup = N - S*(N-1)',
            'derivation': f'''
                Given:
                - Serial fraction (S) = {serial_fraction:.3f} ({serial_fraction*100:.1f}%)
                - Number of processors (N) = {cores}
                
                Step 1: Calculate scaled speedup
                Speedup = N - S*(N-1)
                       = {cores} - {serial_fraction:.4f} * ({cores} - 1)
                       = {cores} - {serial_fraction * (cores - 1):.4f}
                       = {speedup:.2f}
                
                Step 2: Calculate scaled efficiency
                Efficiency = Speedup / N * 100%
                         = {speedup:.2f} / {cores} * 100%
                         = {efficiency:.1f}%
            ''',
            'interpretation': f'''
                Unlike Amdahl's Law, Gustafson's Law shows that with larger problem sizes,
                speedup can scale almost linearly with the number of processors.
                For {cores} cores, we achieve {speedup:.2f}x speedup,
                which is {efficiency:.1f}% of ideal linear scaling.
            ''',
            'insight': 'Gustafson\'s Law is more realistic for HPC because problem sizes typically grow with available computing power.'
        }
        
        return {
            'speedup': round(speedup, 2),
            'efficiency': round(efficiency, 1),
            'serial_fraction': round(serial_fraction * 100, 1),
            'core_range': core_range,
            'speedups': speedups,
            'ideal': ideal,
            'explanation': explanation
        }
    
    def scalability_with_explanation(self, cores, overhead):
        serial_fraction = 0.1  # Assume 10% serial by default
        
        strong_speedup = 1.0 / (serial_fraction + (1.0 - serial_fraction) / cores)
        weak_efficiency = 1.0 - overhead * math.log(max(cores - 1, 1)) if cores > 1 else 1.0
        
        core_range = list(range(1, min(cores, 128) + 1))
        strong_speedups = [1.0 / (serial_fraction + (1.0 - serial_fraction) / c) for c in core_range]
        weak_efficiencies = [max(0, 1.0 - overhead * math.log(max(c - 1, 1))) for c in core_range]
        ideal = [c for c in core_range]
        
        explanation = {
            'title': 'Strong vs Weak Scaling Analysis',
            'definitions': {
                'strong_scaling': 'Fixed problem size, measure time reduction with more cores',
                'weak_scaling': 'Problem size grows with cores, measure time stability'
            },
            'strong_calculation': f'''
                Strong Scaling (Amdahl's Law with 10% serial):
                Speedup(N) = 1 / (0.1 + 0.9/N)
                
                For N = {cores}:
                Speedup = 1 / (0.1 + 0.9/{cores})
                        = 1 / (0.1 + {0.9/cores:.4f})
                        = 1 / {0.1 + 0.9/cores:.4f}
                        = {strong_speedup:.2f}x
            ''',
            'weak_calculation': f'''
                Weak Scaling (Problem size ∝ N):
                Efficiency(N) = 1 - ε·ln(N-1), where ε = {overhead}
                
                For N = {cores}:
                Efficiency = 1 - {overhead}·ln({cores-1})
                          = 1 - {overhead * math.log(max(cores-1,1)):.4f}
                          = {weak_efficiency:.3f} ({weak_efficiency*100:.1f}%)
                
                This means communication overhead reduces efficiency by {overhead * math.log(max(cores-1,1))*100:.1f}%
            ''',
            'interpretation': f'''
                - Strong scaling achieves {strong_speedup:.2f}x speedup on {cores} cores
                - Weak scaling maintains {weak_efficiency*100:.1f}% efficiency
                - Communication overhead limits scalability to about {1/overhead:.0f} cores for strong scaling
            ''',
            'formula': 'Efficiency = 1 / (1 + α·log(P)) for weak scaling'
        }
        
        return {
            'strong_speedup': round(strong_speedup, 2),
            'weak_efficiency': round(max(0, weak_efficiency) * 100, 1),
            'ideal': cores,
            'core_range': core_range,
            'strong_speedups': strong_speedups,
            'weak_efficiencies': weak_efficiencies,
            'ideal_line': ideal,
            'explanation': explanation
        }
