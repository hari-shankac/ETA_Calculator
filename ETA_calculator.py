import datetime

class ProjectETACalculator:
    def __init__(self, total_tasks, qa_rate):
        self.total_tasks = total_tasks
        self.qa_rate = qa_rate
        self.work_hours_per_day = 6.5
        self.levels = {
            'L0': {'hc': 0, 'lt': 0, 'tasks': total_tasks},
            'L1': {'hc': 0, 'lt': 0, 'tasks': 0},
            'L2': {'hc': 0, 'lt': 0, 'tasks': 0}
        }
        self.completed_tasks = 0
        self.total_human_minutes = 0

    def set_level_params(self, level, hc, lt):
        self.levels[level]['hc'] = hc
        self.levels[level]['lt'] = lt

    def calculate_eta(self):
        start_time = datetime.datetime.now()
        current_time = start_time
        
        while self.completed_tasks < self.total_tasks:
            for level in ['L0', 'L1', 'L2']:
                tasks_completed = min(
                    self.levels[level]['tasks'],
                    self.levels[level]['hc'] * (60 / self.levels[level]['lt'])
                )
                
                self.levels[level]['tasks'] -= tasks_completed
                self.total_human_minutes += tasks_completed * self.levels[level]['lt']
                
                if level == 'L0':
                    tasks_to_qa = tasks_completed * self.qa_rate
                    self.levels['L1']['tasks'] += tasks_to_qa
                    self.completed_tasks += tasks_completed - tasks_to_qa
                elif level == 'L1':
                    self.levels['L2']['tasks'] += tasks_completed
                else:
                    self.completed_tasks += tasks_completed
            
            current_time += datetime.timedelta(hours=1)
            
            if current_time.hour == 0:
                current_time += datetime.timedelta(hours=24 - self.work_hours_per_day)
        
        total_time = current_time - start_time
        days, seconds = total_time.days, total_time.seconds
        hours = seconds // 3600
        minutes = (seconds % 3600) // 60
        
        return f"{days:02d}:{hours:02d}:{minutes:02d}", self.total_human_minutes

    def get_queue_status(self):
        return {level: self.levels[level]['tasks'] for level in self.levels}

# Example
calculator = ProjectETACalculator(total_tasks=1000, qa_rate=0.8)
calculator.set_level_params('L0', hc=40, lt=5)
calculator.set_level_params('L1', hc=10, lt=3) 
calculator.set_level_params('L2', hc=5, lt=2)  

eta, total_human_minutes = calculator.calculate_eta()
print(f"Estimated Time to Completion: {eta}")
print(f"Total Human Minutes: {total_human_minutes}")
print(f"Queue Status: {calculator.get_queue_status()}")