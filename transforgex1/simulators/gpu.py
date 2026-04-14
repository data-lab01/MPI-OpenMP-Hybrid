class GPUSimulator:
    def __init__(self):
        pass
    
    def calculate(self, memory_size, compute_units, bandwidth, compute_power, data_size, operations):
        # Core calculations
        memory_time = data_size / bandwidth if bandwidth > 0 else 0
        compute_time = operations / compute_power if compute_power > 0 else 0
        total_time = memory_time + compute_time
        speedup_cpu = (operations / 0.5) / total_time if total_time > 0 else 0
        memory_util = (data_size / memory_size) * 100 if memory_size > 0 else 0
        occupancy = compute_time / (memory_time + 0.001)
        
        # Theoretical peak performance
        theoretical_peak = compute_units * 2 * 1.5  # Approximate: 2 ops/cycle * 1.5 GHz
        achieved_performance = operations / total_time if total_time > 0 else 0
        
        # Memory bandwidth utilization
        bandwidth_util = (data_size / memory_time) / bandwidth * 100 if memory_time > 0 else 0
        
        if occupancy < 0.8:
            bound_type = "Memory bound"
            bound_color = "yellow"
            bottleneck = f"Memory bandwidth is the bottleneck. Only {bandwidth_util:.1f}% utilized."
        elif occupancy > 1.2:
            bound_type = "Compute bound"
            bound_color = "yellow"
            bottleneck = f"Compute performance is the bottleneck. Achieved {achieved_performance:.1f} TFLOPS of {compute_power:.1f} TFLOPS peak."
        else:
            bound_type = "Balanced"
            bound_color = "green"
            bottleneck = "Workload is well-balanced between compute and memory."
        
        # Detailed explanation
        explanation = {
            'title': 'GPU Performance Analysis',
            'memory_calculation': f'''
                Memory Transfer Time Calculation:
                Time = Data Size / Memory Bandwidth
                    = {data_size} GB / {bandwidth} GB/s
                    = {memory_time:.4f} seconds
                
                This represents the time to transfer data between CPU and GPU memory.
            ''',
            'compute_calculation': f'''
                Kernel Execution Time Calculation:
                Time = Operations / Compute Power
                    = {operations} TFLOP / {compute_power} TFLOPS
                    = {compute_time:.4f} seconds
                
                This assumes perfect utilization of all {compute_units} compute units.
            ''',
            'total_calculation': f'''
                Total Execution Time = Memory Time + Compute Time
                                     = {memory_time:.4f}s + {compute_time:.4f}s
                                     = {total_time:.4f}s
                
                GPU Speedup vs CPU:
                CPU would take approximately {operations/0.5:.1f} seconds at 0.5 TFLOPS
                Speedup = {operations/0.5:.1f}s / {total_time:.4f}s = {speedup_cpu:.1f}x
            ''',
            'bottleneck_analysis': bottleneck,
            'occupancy_formula': f'''
                Compute/Memory Ratio = Compute Time / Memory Time
                                     = {compute_time:.4f} / {memory_time:.4f}
                                     = {occupancy:.2f}
                
                {"Memory-bound" if occupancy < 0.8 else "Compute-bound" if occupancy > 1.2 else "Balanced"} workload detected.
                {"Increase compute intensity" if occupancy < 0.8 else "Increase memory bandwidth" if occupancy > 1.2 else "Optimal balance"}.
            ''',
            'recommendations': self.get_recommendations(bound_type, memory_util, occupancy)
        }
        
        return {
            'memory_time': round(memory_time, 4),
            'compute_time': round(compute_time, 4),
            'total_time': round(total_time, 4),
            'speedup_cpu': round(speedup_cpu, 1),
            'memory_utilization': round(memory_util, 1),
            'occupancy': round(occupancy, 2),
            'bandwidth_utilization': round(bandwidth_util, 1),
            'achieved_performance': round(achieved_performance, 2),
            'bound_type': bound_type,
            'bound_color': bound_color,
            'explanation': explanation
        }
    
    def get_recommendations(self, bound_type, memory_util, occupancy):
        if bound_type == "Memory bound":
            return [
                "💡 Reduce data transfers by kernel fusion",
                "💡 Use shared memory for frequently accessed data",
                "💡 Increase compute intensity by doing more work per byte",
                "💡 Consider using texture memory for spatial locality"
            ]
        elif bound_type == "Compute bound":
            return [
                "💡 Optimize arithmetic intensity",
                "💡 Use faster math functions (__sinf vs sin)",
                "💡 Reduce thread divergence in warps",
                "💡 Increase occupancy by reducing register usage"
            ]
        else:
            return [
                "✅ Current configuration is well-balanced",
                "💡 Consider increasing problem size for better scaling",
                "💡 Profile to identify micro-optimizations",
                "💡 Explore asynchronous execution for overlap"
            ]
