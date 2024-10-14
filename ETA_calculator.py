import datetime

def calculate_eta(total_tasks, qa_rate, l0_hc, l0_lt, l1_hc, l1_lt, l2_hc, l2_lt):
    work_hours_per_day = 6.5
    levels = {
        'L0': {'hc': l0_hc, 'lt': l0_lt, 'tasks': total_tasks},
        'L1': {'hc': l1_hc, 'lt': l1_lt, 'tasks': 0},
        'L2': {'hc': l2_hc, 'lt': l2_lt, 'tasks': 0}
    }
    completed_tasks = 0
    total_human_minutes = 0
    start_time = datetime.datetime.now()
    current_time = start_time

    while completed_tasks < total_tasks:
        for level in ['L0', 'L1', 'L2']:
            tasks_completed = min(
                levels[level]['tasks'],
                levels[level]['hc'] * (60 / levels[level]['lt'])
            )
            
            levels[level]['tasks'] -= tasks_completed
            total_human_minutes += tasks_completed * levels[level]['lt']
            
            if level == 'L0':
                tasks_to_qa = tasks_completed * qa_rate
                levels['L1']['tasks'] += tasks_to_qa
                completed_tasks += tasks_completed - tasks_to_qa
            elif level == 'L1':
                levels['L2']['tasks'] += tasks_completed
            else:  # L2
                completed_tasks += tasks_completed
        
        current_time += datetime.timedelta(hours=1)
        
        if current_time.hour == 0:  # New day
            current_time += datetime.timedelta(hours=24 - work_hours_per_day)

    total_time = current_time - start_time
    days, seconds = total_time.days, total_time.seconds
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60

    return f"{days:02d}:{hours:02d}:{minutes:02d}", total_human_minutes

def get_input(prompt, input_type=float):
    while True:
        try:
            return input_type(input(prompt))
        except ValueError:
            print("Invalid input. Please try again.")

def main():
    print("Welcome to the Project ETA Calculator")
    print("Please enter the following information:")

    total_tasks = get_input("Total number of tasks: ", int)
    qa_rate = get_input("QA rate (0-1, e.g., 0.8 for 80%): ")
    
    l0_hc = get_input("L0 Headcount: ", int)
    l0_lt = get_input("L0 Lead Time (in minutes): ")
    
    l1_hc = get_input("L1 Headcount: ", int)
    l1_lt = get_input("L1 Lead Time (in minutes): ")
    
    l2_hc = get_input("L2 Headcount: ", int)
    l2_lt = get_input("L2 Lead Time (in minutes): ")

    eta, total_human_minutes = calculate_eta(
        total_tasks, qa_rate, l0_hc, l0_lt, l1_hc, l1_lt, l2_hc, l2_lt
    )

    print(f"\nResults:")
    print(f"Estimated Time to Completion: {eta}")
    print(f"Total Human Minutes: {total_human_minutes:.2f}")

if __name__ == "__main__":
    main()