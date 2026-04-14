class EnergyMonitor:
    """Monitor and optimize energy consumption"""
    
    def __init__(self):
        self.power_cap = 20000
        self.current_power = 0
        self.renewable_percentage = 0
        
    def calculate_energy_metrics(self, nodes, utilization, runtime_hours):
        """Calculate detailed energy metrics"""
        node_power = nodes * 0.3
        total_energy = node_power * utilization * runtime_hours
        cooling_energy = total_energy * 0.3
        
        return {
            'compute_energy_kwh': round(total_energy, 2),
            'cooling_energy_kwh': round(cooling_energy, 2),
            'total_energy_kwh': round(total_energy + cooling_energy, 2),
            'carbon_emissions_kg': round((total_energy + cooling_energy) * 0.2, 2),
            'cost_euros': round((total_energy + cooling_energy) * 0.15, 2),
            'energy_efficiency': round(1.0 / (node_power + 0.001), 3)
        }
    
    def suggest_optimizations(self, energy_metrics):
        """EU-compliant energy optimizations"""
        suggestions = []
        if energy_metrics.get('carbon_emissions_kg', 0) > 1000:
            suggestions.append("🌍 High carbon emissions - consider EU renewable energy credits")
        if energy_metrics.get('energy_efficiency', 10) < 10:
            suggestions.append("⚡ Poor energy efficiency - upgrade to newer hardware")
        suggestions.append("📊 Monitor using EU Energy Efficiency Directive (EED)")
        return suggestions
