"""Multi-user collaboration features for shared HPC simulations"""
import uuid
from datetime import datetime
from typing import Dict, List

class CollaborationManager:
    """Manage multi-user simulation sessions"""
    
    def __init__(self):
        self.sessions: Dict[str, dict] = {}
        self.shared_configs: Dict[str, dict] = {}
        
    def create_shared_session(self, owner_id, config):
        """Create a shareable simulation session"""
        session_id = str(uuid.uuid4())
        self.sessions[session_id] = {
            'owner': owner_id,
            'config': config,
            'users': [owner_id],
            'created_at': datetime.now(),
            'is_active': True
        }
        return session_id
    
    def join_session(self, session_id, user_id):
        """Join an existing shared session"""
        if session_id in self.sessions:
            if user_id not in self.sessions[session_id]['users']:
                self.sessions[session_id]['users'].append(user_id)
            return True
        return False
    
    def get_session_state(self, session_id):
        """Get current session state"""
        return self.sessions.get(session_id)
    
    def save_configuration(self, name, config, user_id):
        """Save configuration for sharing"""
        config_id = str(uuid.uuid4())
        self.shared_configs[config_id] = {
            'name': name,
            'config': config,
            'owner': user_id,
            'created_at': datetime.now(),
            'downloads': 0
        }
        return config_id
    
    def get_shared_configs(self):
        """Get list of shared configurations"""
        return [
            {'id': cid, 'name': data['name'], 'owner': data['owner']}
            for cid, data in self.shared_configs.items()
        ]
    
    def clone_configuration(self, config_id, user_id):
        """Clone and modify existing configuration"""
        if config_id in self.shared_configs:
            original = self.shared_configs[config_id]['config']
            new_config = original.copy()
            new_config['cloned_from'] = config_id
            new_config['cloned_by'] = user_id
            return new_config
        return None
