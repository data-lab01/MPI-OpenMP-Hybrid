import math

class NetworkSimulator:
    def __init__(self):
        self.topology = 'fat_tree'
        self.nodes = []
        self.packets = []
        self.generate_topology()
        
    def generate_topology(self):
        if self.topology == 'fat_tree':
            self.generate_fat_tree()
        elif self.topology == 'dragonfly':
            self.generate_dragonfly()
        elif self.topology == 'torus':
            self.generate_torus()
    
    def generate_fat_tree(self):
        self.nodes = []
        radius = 250
        center = (400, 250)
        
        for i in range(16):
            angle = (i / 16) * 2 * math.pi
            x = center[0] + radius * math.cos(angle)
            y = center[1] + radius * math.sin(angle)
            
            links = []
            pod = i // 4
            pos_in_pod = i % 4
            
            for j in range(4):
                if j != pos_in_pod:
                    links.append(pod * 4 + j)
            
            links.append((pod + 4) % 16)
            
            self.nodes.append({
                'id': i,
                'x': x,
                'y': y,
                'links': links
            })
    
    def generate_dragonfly(self):
        self.nodes = []
        groups = 4
        nodes_per_group = 5
        
        for group in range(groups):
            group_angle = (group / groups) * 2 * math.pi
            group_center_x = 400 + 200 * math.cos(group_angle)
            group_center_y = 250 + 200 * math.sin(group_angle)
            
            for node_in_group in range(nodes_per_group):
                node_angle = (node_in_group / nodes_per_group) * 2 * math.pi
                x = group_center_x + 50 * math.cos(node_angle)
                y = group_center_y + 50 * math.sin(node_angle)
                
                node_id = group * nodes_per_group + node_in_group
                links = self.get_dragonfly_links(node_id, groups, nodes_per_group)
                
                self.nodes.append({
                    'id': node_id,
                    'x': x,
                    'y': y,
                    'links': links
                })
    
    def get_dragonfly_links(self, node_id, groups, nodes_per_group):
        links = []
        my_group = node_id // nodes_per_group
        my_pos = node_id % nodes_per_group
        
        for i in range(nodes_per_group):
            if i != my_pos:
                links.append(my_group * nodes_per_group + i)
        
        for g in range(groups):
            if g != my_group:
                links.append(g * nodes_per_group + (my_pos % nodes_per_group))
        
        return links
    
    def generate_torus(self):
        self.nodes = []
        dim = 4
        spacing = 80
        start_x = 200
        start_y = 100
        
        for i in range(dim):
            for j in range(dim):
                node_id = i * dim + j
                x = start_x + j * spacing
                y = start_y + i * spacing
                
                links = []
                links.append(((i + dim - 1) % dim) * dim + j)
                links.append(((i + 1) % dim) * dim + j)
                links.append(i * dim + (j + dim - 1) % dim)
                links.append(i * dim + (j + 1) % dim)
                
                self.nodes.append({
                    'id': node_id,
                    'x': x,
                    'y': y,
                    'links': links
                })
    
    def set_topology(self, topology):
        self.topology = topology
        self.generate_topology()
        self.packets = []
        return self.get_topology_data()
    
    def send_packet(self, source, destination):
        packet = {
            'id': len(self.packets) + 1,
            'source': source,
            'destination': destination,
            'progress': 0.0
        }
        self.packets.append(packet)
        return packet
    
    def update(self):
        completed = []
        for i, packet in enumerate(self.packets):
            packet['progress'] += 0.02
            if packet['progress'] >= 1.0:
                completed.append(i)
        
        for i in reversed(completed):
            self.packets.pop(i)
    
    def get_topology_data(self):
        return {
            'nodes': self.nodes,
            'packets': self.packets,
            'topology': self.topology
        }
    
    def get_state(self):
        return self.get_topology_data()
