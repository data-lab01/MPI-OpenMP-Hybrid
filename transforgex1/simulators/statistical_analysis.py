"""
Statistical methods for HPC performance evaluation
Based on:
- Confidence intervals for performance metrics
- Hypothesis testing for scheduler comparison
- Regression analysis for scaling models
"""

import math
import random
from typing import List, Tuple, Dict
from scipy import stats  # Note: requires pip install scipy

class StatisticalAnalyzer:
    """Scientific statistical analysis for HPC simulations"""
    
    def __init__(self):
        self.confidence_levels = {0.90: 1.645, 0.95: 1.96, 0.99: 2.576}
    
    def confidence_interval(self, data: List[float], confidence: float = 0.95) -> Tuple[float, float]:
        """
        Calculate confidence interval for performance metrics
        Based on Student's t-distribution
        """
        n = len(data)
        if n < 2:
            return (0, 0)
        
        mean = sum(data) / n
        variance = sum((x - mean) ** 2 for x in data) / (n - 1)
        std_error = math.sqrt(variance / n)
        
        z_score = self.confidence_levels.get(confidence, 1.96)
        margin = z_score * std_error
        
        return (mean - margin, mean + margin)
    
    def t_test_compare_schedulers(self, scheduler_a_results: List[float], 
                                  scheduler_b_results: List[float]) -> Dict:
        """
        Paired t-test for comparing two scheduling algorithms
        Null hypothesis: No significant difference between schedulers
        """
        from scipy import stats as scipy_stats
        
        # Paired t-test
        t_stat, p_value = scipy_stats.ttest_rel(scheduler_a_results, scheduler_b_results)
        
        # Calculate effect size (Cohen's d)
        mean_diff = sum(scheduler_a_results) / len(scheduler_a_results) - sum(scheduler_b_results) / len(scheduler_b_results)
        pooled_std = math.sqrt((self.variance(scheduler_a_results) + self.variance(scheduler_b_results)) / 2)
        cohens_d = mean_diff / pooled_std if pooled_std > 0 else 0
        
        return {
            't_statistic': round(t_stat, 3),
            'p_value': round(p_value, 4),
            'significant_difference': p_value < 0.05,
            'effect_size': round(cohens_d, 3),
            'effect_magnitude': self.interpret_effect_size(cohens_d),
            'confidence_interval': self.confidence_interval([mean_diff]),
            'interpretation': f"Significant difference (p={p_value:.4f})" if p_value < 0.05 else "No significant difference"
        }
    
    def variance(self, data: List[float]) -> float:
        """Calculate sample variance"""
        if len(data) < 2:
            return 0
        mean = sum(data) / len(data)
        return sum((x - mean) ** 2 for x in data) / (len(data) - 1)
    
    def interpret_effect_size(self, cohens_d: float) -> str:
        """Interpret Cohen's d effect size"""
        if abs(cohens_d) < 0.2:
            return "negligible"
        elif abs(cohens_d) < 0.5:
            return "small"
        elif abs(cohens_d) < 0.8:
            return "medium"
        else:
            return "large"
    
    def anova_analysis(self, groups: List[List[float]]) -> Dict:
        """
        One-way ANOVA for comparing multiple configurations
        """
        from scipy import stats as scipy_stats
        
        f_stat, p_value = scipy_stats.f_oneway(*groups)
        
        # Calculate eta-squared (effect size for ANOVA)
        ss_between = self.between_group_variance(groups)
        ss_total = self.total_variance(groups)
        eta_squared = ss_between / ss_total if ss_total > 0 else 0
        
        return {
            'f_statistic': round(f_stat, 3),
            'p_value': round(p_value, 4),
            'significant_difference': p_value < 0.05,
            'eta_squared': round(eta_squared, 3),
            'interpretation': f"ANOVA indicates {'significant' if p_value < 0.05 else 'no'} differences between groups"
        }
    
    def between_group_variance(self, groups: List[List[float]]) -> float:
        """Calculate between-group variance for ANOVA"""
        all_data = [x for group in groups for x in group]
        grand_mean = sum(all_data) / len(all_data)
        
        ss_between = 0
        for group in groups:
            group_mean = sum(group) / len(group)
            ss_between += len(group) * ((group_mean - grand_mean) ** 2)
        
        return ss_between
    
    def total_variance(self, groups: List[List[float]]) -> float:
        """Calculate total variance for ANOVA"""
        all_data = [x for group in groups for x in group]
        grand_mean = sum(all_data) / len(all_data)
        
        return sum((x - grand_mean) ** 2 for x in all_data)
    
    def regression_analysis(self, x_data: List[float], y_data: List[float]) -> Dict:
        """
        Linear regression for scaling analysis
        Model: log(speedup) = a + b * log(cores)
        """
        from scipy import stats as scipy_stats
        
        # Convert to log space for power law
        log_x = [math.log(x) for x in x_data]
        log_y = [math.log(y) for y in y_data]
        
        slope, intercept, r_value, p_value, std_err = scipy_stats.linregress(log_x, log_y)
        
        return {
            'slope': round(slope, 3),  # Scaling exponent
            'intercept': round(intercept, 3),
            'r_squared': round(r_value ** 2, 3),
            'p_value': round(p_value, 4),
            'std_error': round(std_err, 4),
            'scaling_model': 'power_law' if slope < 1.0 else 'linear',
            'strong_scaling_efficiency': round(2 ** (slope - 1), 3) if slope > 0 else 0,
            'interpretation': self.interpret_scaling(slope)
        }
    
    def interpret_scaling(self, slope: float) -> str:
        """Interpret scaling exponent"""
        if slope > 0.9:
            return "Excellent strong scaling (near-linear)"
        elif slope > 0.7:
            return "Good strong scaling"
        elif slope > 0.5:
            return "Moderate strong scaling"
        else:
            return "Poor strong scaling - consider optimization"
    
    def bootstrap_analysis(self, data: List[float], n_iterations: int = 1000) -> Dict:
        """
        Bootstrap resampling for robust confidence intervals
        Non-parametric method for performance analysis
        """
        boot_means = []
        n = len(data)
        
        for _ in range(n_iterations):
            sample = [random.choice(data) for _ in range(n)]
            boot_means.append(sum(sample) / n)
        
        boot_means.sort()
        ci_lower = boot_means[int(n_iterations * 0.025)]
        ci_upper = boot_means[int(n_iterations * 0.975)]
        
        return {
            'mean': round(sum(data) / len(data), 3),
            'bootstrap_ci_95': (round(ci_lower, 3), round(ci_upper, 3)),
            'bias': round(ci_lower - (sum(data) / len(data)), 3),
            'method': 'Efron\'s bootstrap (1979)',
            'iterations': n_iterations
        }
