"""Generate professional HPC simulation reports"""
import json
from datetime import datetime
import os

class HPCReportGenerator:
    """Generate PDF/HTML reports of simulation results"""
    
    def __init__(self):
        self.report_types = ['performance', 'energy', 'compliance', 'full']
    
    def generate_performance_report(self, simulation_data, format='html'):
        """Generate performance analysis report"""
        
        report = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>TransForgeX1 - HPC Performance Report</title>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 40px; }}
                .header {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                          color: white; padding: 30px; border-radius: 10px; }}
                .section {{ margin: 20px 0; padding: 20px; border: 1px solid #ddd; border-radius: 10px; }}
                .metric {{ display: inline-block; margin: 10px; padding: 15px; background: #f5f5f5; border-radius: 5px; }}
                .value {{ font-size: 24px; font-weight: bold; color: #667eea; }}
                table {{ width: 100%; border-collapse: collapse; }}
                th, td {{ padding: 10px; text-align: left; border-bottom: 1px solid #ddd; }}
            </style>
        </head>
        <body>
            <div class="header">
                <h1> TransForgeX1 HPC Performance Report</h1>
                <p>Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
            </div>
            
            <div class="section">
                <h2>📊 Executive Summary</h2>
                <div class="metric">
                    <div>Peak Performance</div>
                    <div class="value">{simulation_data.get('peak_tflops', 0)} TFLOPS</div>
                </div>
                <div class="metric">
                    <div>Energy Efficiency</div>
                    <div class="value">{simulation_data.get('energy_efficiency', 0)} GFLOP/W</div>
                </div>
                <div class="metric">
                    <div>System Utilization</div>
                    <div class="value">{simulation_data.get('utilization', 0)}%</div>
                </div>
            </div>
            
            <div class="section">
                <h2>📈 Performance Metrics</h2>
                <table>
                    <tr><th>Metric</th><th>Value</th><th>Status</th></tr>
                    <tr><td>HPL Score</td><td>{simulation_data.get('hpl_tflops', 0)} TFLOPS</td>
                        <td>{'✅' if simulation_data.get('hpl_tflops', 0) > 100 else '⚠️'}</td></tr>
                    <tr><td>Memory Bandwidth</td><td>{simulation_data.get('mem_bw', 0)} GB/s</td>
                        <td>{'✅' if simulation_data.get('mem_bw', 0) > 400 else '⚠️'}</td></tr>
                    <tr><td>Network Latency</td><td>{simulation_data.get('latency', 0)} μs</td>
                        <td>{'✅' if simulation_data.get('latency', 0) < 2 else '⚠️'}</td></tr>
                </table>
            </div>
            
            <div class="section">
                <h2>💡 Recommendations</h2>
                <ul>
                    <li>Consider upgrading interconnect to InfiniBand HDR</li>
                    <li>Implement job scheduling optimization</li>
                    <li>Enable energy-aware scheduling for better PUE</li>
                </ul>
            </div>
        </body>
        </html>
        """
        
        if format == 'html':
            filename = f"report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html"
            with open(filename, 'w') as f:
                f.write(report)
            return filename
        
        return report
    
    def export_simulation_state(self, simulation_data, format='json'):
        """Export simulation state for later analysis"""
        export_data = {
            'timestamp': datetime.now().isoformat(),
            'simulation_data': simulation_data,
            'version': '1.0',
            'source': 'TransForgeX1'
        }
        
        if format == 'json':
            filename = f"simulation_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            with open(filename, 'w') as f:
                json.dump(export_data, f, indent=2)
            return filename
        
        return json.dumps(export_data, indent=2)
