"""
DOI (Digital Object Identifier) integration for experiments
Based on DataCite schema and Zenodo API
"""

import json
import hashlib
from datetime import datetime
from typing import Dict, Optional

class DOIManager:
    """Generate and manage DOIs for experiments"""
    
    def __init__(self, zenodo_token: Optional[str] = None):
        self.zenodo_token = zenodo_token
        self.base_url = "https://zenodo.org/api"
    
    def generate_doi_metadata(self, experiment_id: str, results: Dict) -> Dict:
        """Generate DataCite-compliant metadata"""
        return {
            'identifier': f"10.5281/zenodo.{experiment_id}",
            'creators': [{'name': 'TransForgeX1', 'affiliation': 'HPC Simulation'}],
            'titles': [{'title': f"HPC Simulation Experiment {experiment_id}"}],
            'publisher': 'TransForgeX1',
            'publication_year': datetime.now().year,
            'subjects': [
                {'subject': 'High-Performance Computing'},
                {'subject': 'Job Scheduling'},
                {'subject': 'Network Simulation'}
            ],
            'contributors': [],
            'dates': [{'date': datetime.now().isoformat(), 'type': 'Created'}],
            'language': 'en',
            'resourceType': {'resourceType': 'Dataset', 'resourceTypeGeneral': 'Dataset'},
            'rights_list': [{'rights': 'Creative Commons Attribution 4.0 International'}],
            'descriptions': [{
                'description': f"Reproducible HPC simulation experiment {experiment_id}",
                'descriptionType': 'Abstract'
            }]
        }
    
    def create_zenodo_deposit(self, experiment_id: str, metadata: Dict) -> Dict:
        """Create Zenodo deposit for DOI (requires API token)"""
        if not self.zenodo_token:
            return {'error': 'Zenodo API token required', 'doi': f"10.5281/zenodo.{experiment_id}"}
        
        # This would make actual API call to Zenodo
        # Simplified for demonstration
        return {
            'doi': f"10.5281/zenodo.{experiment_id}",
            'doi_url': f"https://doi.org/10.5281/zenodo.{experiment_id}",
            'status': 'draft',
            'message': 'Deposit created successfully'
        }
    
    def export_cff(self, experiment_id: str, authors: List[str]) -> str:
        """Export CITATION.cff file for experiment"""
        cff_content = f"""
cff-version: 1.2.0
message: "If you use these results, please cite it as below."
title: "TransForgeX1 HPC Simulation Experiment"
doi: 10.5281/zenodo.{experiment_id}
version: 1.0.0
date-released: {datetime.now().strftime('%Y-%m-%d')}
authors:
{self.format_authors(authors)}
license: MIT
repository-code: "https://github.com/transforgex1/transforgex1"
keywords:
  - HPC
  - Job Scheduling
  - Network Simulation
  - Reproducibility
"""
        return cff_content
    
    def format_authors(self, authors: List[str]) -> str:
        """Format authors for CFF"""
        return '\n'.join([f'  - name: "{author}"' for author in authors])
    
    def generate_ro_crate(self, experiment_id: str, files: List[str]) -> Dict:
        """
        Generate RO-Crate for packaging research objects
        Compliant with Research Object Crate specification
        """
        ro_crate = {
            '@context': 'https://w3id.org/ro/crate/1.1/context',
            '@graph': [
                {
                    '@id': './',
                    '@type': 'CreativeWork',
                    'name': f'Experiment {experiment_id}',
                    'datePublished': datetime.now().isoformat(),
                    'license': 'https://creativecommons.org/licenses/by/4.0/',
                    'hasPart': [{'@id': f} for f in files]
                }
            ]
        }
        
        return ro_crate

class ReproZipIntegration:
    """Generate ReproZip packages for complete reproducibility"""
    
    def generate_reprozip_config(self, experiment_dir: str) -> Dict:
        """Generate ReproZip configuration"""
        return {
            'version': '1.0',
            'experiment_dir': experiment_dir,
            'packages': [
                'python3',
                'flask',
                'numpy',
                'scipy'
            ],
            'environment': {
                'PYTHONHASHSEED': '42',
                'LC_ALL': 'C'
            },
            'inputs': ['templates/', 'simulators/', 'app.py'],
            'outputs': ['experiments/'],
            'command': 'python3 app.py'
        }
    
    def create_reprozip_rpz(self, config: Dict) -> str:
        """Create .rpz file (simplified)"""
        # In real implementation, would call reprozip command line
        return "experiment.rpz"
