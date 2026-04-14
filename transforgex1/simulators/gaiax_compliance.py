class GaiaXCompliance:
    """GAIA-X data infrastructure compliance checker"""
    
    def __init__(self):
        self.standards = {
            'data_sovereignty': True,
            'interoperability': 'IDS (International Data Spaces)',
            'security_level': 'EU-RATED',
            'federated_catalog': True
        }
    
    def check_data_compliance(self, data_volume_gb, data_sensitivity):
        """Check if data handling meets GAIA-X standards"""
        
        compliance_status = {
            'gdpr_compliant': data_sensitivity in ['public', 'internal', 'confidential'],
            'encryption_required': data_sensitivity == 'confidential',
            'storage_location': 'EU-only' if data_sensitivity == 'confidential' else 'Any',
            'audit_required': data_sensitivity != 'public'
        }
        
        if data_volume_gb > 10000:
            compliance_status['tier'] = 'Large Scale - requires federated storage'
        elif data_volume_gb > 1000:
            compliance_status['tier'] = 'Medium Scale - standard compliance'
        else:
            compliance_status['tier'] = 'Small Scale - basic compliance'
        
        return compliance_status
    
    def get_gaiax_requirements(self):
        """Return GAIA-X compliance requirements"""
        return {
            'identity_management': 'Self-sovereign identity (SSI)',
            'data_sovereignty': 'Data usage control',
            'interoperability': 'Eclipse Dataspace Components (EDC)',
            'security': 'EU-QRATED certification',
            'federation': 'GAIA-X Federation Services'
        }
