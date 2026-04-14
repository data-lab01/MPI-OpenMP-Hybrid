from collections import deque
import math

class Job:
    def __init__(self, job_id, nodes, time_required):
        self.id = job_id
        self.nodes = nodes
        self.time_required = time_required
        self.time_remaining = time_required
        self.status = 'queued'

class JobScheduler:
    def __init__(self):
        self.nodes = [{'id': i, 'job': None, 'remaining_time': 0} for i in range(8)]
        self.queue = deque()
        self.next_job_id = 1
        self.scheduler_type = 'FIFO'
        self.stats = {'total_jobs': 0, 'completed_jobs': 0, 'avg_wait_time': 0}
        
    def get_status(self):
        node_status = []
        for node in self.nodes:
            node_status.append({
                'id': node['id'],
                'busy': node['job'] is not None,
                'job_id': node['job'].id if node['job'] else None,
                'remaining_time': round(node['remaining_time'], 1)
            })
        
        queue_status = []
        for job in self.queue:
            queue_status.append({
                'id': job.id,
                'nodes': job.nodes,
                'time': job.time_required,
                'status': job.status
            })
        
        # Calculate scheduling metrics
        total_nodes = len(self.nodes)
        busy_nodes = sum(1 for n in self.nodes if n['job'] is not None)
        utilization = (busy_nodes / total_nodes) * 100
        
        return {
            'nodes': node_status,
            'queue': queue_status,
            'scheduler_type': self.scheduler_type,
            'utilization': round(utilization, 1),
            'queue_length': len(self.queue),
            'total_jobs': self.stats['total_jobs'],
            'completed_jobs': self.stats['completed_jobs']
        }
    
    def get_explanation(self):
        explanations = {
            'FIFO': {
                'name': 'First-In-First-Out (FIFO) Scheduling',
                'formula': 'Jobs executed in order of arrival. FCFS (First Come First Served)',
                'calculation': 'No priority calculation - simple queue order',
                'pros': 'Fair, simple to implement, no starvation',
                'cons': 'Convoy effect - short jobs wait behind long jobs',
                'complexity': 'O(1) per scheduling decision'
            },
            'Backfill': {
                'name': 'Backfill Scheduling (EASY-Backfill)',
                'formula': 'Small jobs can jump ahead if they don\'t delay the first large job',
                'calculation': 'Check if job.time < shadow_time AND fits in gaps',
                'pros': 'Good utilization, reduces average wait time',
                'cons': 'More complex, may delay large jobs slightly',
                'complexity': 'O(n) where n = queue length'
            },
            'Priority': {
                'name': 'Priority-Based Scheduling',
                'formula': 'Priority = 1 / (nodes_requested) [Smaller jobs get higher priority]',
                'calculation': 'Sort by nodes ascending, then schedule',
                'pros': 'Good for mixed workloads, reduces fragmentation',
                'cons': 'Large jobs may starve',
                'complexity': 'O(n log n) for sorting'
            }
        }
        return explanations.get(self.scheduler_type, explanations['FIFO'])
    
    def set_scheduler_type(self, scheduler_type):
        self.scheduler_type = scheduler_type
        self.schedule_jobs()
    
    def submit_job(self, nodes, time_required):
        job = Job(self.next_job_id, nodes, time_required)
        self.next_job_id += 1
        self.queue.append(job)
        self.stats['total_jobs'] += 1
        self.schedule_jobs()
        return {'job_id': job.id, 'status': 'submitted'}
    
    def schedule_jobs(self):
        if self.scheduler_type == 'FIFO':
            self.schedule_fifo()
        elif self.scheduler_type == 'Backfill':
            self.schedule_backfill()
        elif self.scheduler_type == 'Priority':
            self.schedule_priority()
    
    def schedule_fifo(self):
        scheduled = []
        for job in list(self.queue):
            available_nodes = sum(1 for n in self.nodes if n['job'] is None)
            if job.nodes <= available_nodes:
                scheduled.append(job)
            else:
                break
        
        for job in scheduled:
            self.queue.remove(job)
            self.assign_job(job)
    
    def schedule_backfill(self):
        scheduled = []
        remaining = []
        
        # Find the first job in queue (will determine shadow time)
        first_job = self.queue[0] if self.queue else None
        shadow_time = first_job.time_required if first_job else 0
        
        for job in self.queue:
            available_nodes = sum(1 for n in self.nodes if n['job'] is None)
            
            if job.nodes <= available_nodes:
                scheduled.append(job)
            elif job.time_required < shadow_time and job.time_required < 5:
                # Backfill: small job can run if it doesn't delay first job
                scheduled.append(job)
            else:
                remaining.append(job)
        
        self.queue = deque(remaining)
        for job in scheduled:
            self.assign_job(job)
    
    def schedule_priority(self):
        jobs = sorted(list(self.queue), key=lambda j: j.nodes)
        
        scheduled = []
        remaining = []
        
        for job in jobs:
            available_nodes = sum(1 for n in self.nodes if n['job'] is None)
            if job.nodes <= available_nodes:
                scheduled.append(job)
            else:
                remaining.append(job)
        
        self.queue = deque(remaining)
        for job in scheduled:
            self.assign_job(job)
    
    def assign_job(self, job):
        assigned = 0
        for node in self.nodes:
            if node['job'] is None and assigned < job.nodes:
                node['job'] = job
                node['remaining_time'] = job.time_required
                job.status = 'running'
                assigned += 1
    
    def update(self):
        for node in self.nodes:
            if node['job'] is not None:
                node['remaining_time'] -= 0.1
                if node['remaining_time'] <= 0:
                    self.stats['completed_jobs'] += 1
                    node['job'].status = 'completed'
                    node['job'] = None
                    node['remaining_time'] = 0
        
        self.schedule_jobs()
    
    def reset(self):
        self.nodes = [{'id': i, 'job': None, 'remaining_time': 0} for i in range(8)]
        self.queue = deque()
        self.next_job_id = 1
        self.stats = {'total_jobs': 0, 'completed_jobs': 0, 'avg_wait_time': 0}
