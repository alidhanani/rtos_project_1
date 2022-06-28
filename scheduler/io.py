import matplotlib.pyplot as plt

def parse_tasks(tasks_file):
    file_handle = open(tasks_file, "r")
    lines = file_handle.readlines()
    file_handle.close()
    tasks = []
    for id, line in enumerate(lines):
        values = line.split("; ")
        tasks.append({
            "offset": int(values[0]),
            "wcet": int(values[1]),
            "period": int(values[2]),
            "id": id
        })
    return tasks

def write_tasks(tasks_file, tasks):
    file_handle = open(tasks_file,"w+")
    for task in tasks:
            file_handle.write(f'{task["offset"]}; {task["wcet"]}; {task["period"]}\n')
    file_handle.close()

# TODO: Print that a task failed as well?
def print_simulation_result(simulation_result, tasks, end_time):
    print(f'Schedule from: 0 to: {end_time} ; {len(tasks)} tasks')
    for job_execution in simulation_result.job_history:
        print(f'{job_execution["startTime"]}-{job_execution["stopTime"]}: T{job_execution["taskId"]}J{job_execution["jobId"]}')

def print_fdms(tasks):
    for task in tasks:
        print(f'Task {task["id"]}: {task["upgradeTime"]}')

def display_simulation_graph(simulation_result):
    fig, ax = plt.subplots()
    for job in simulation_result.job_history:
        task_name = f'task-{job["taskId"]}'
        duration = job["stopTime"] - job["startTime"]
        # For a given task, we alternate between red jobs and blue jobs
        # This makes it clear when each job starts and finishes
        color = "red" if job["jobId"] % 2 == 0 else "blue"
        ax.barh(task_name, duration, left=job["startTime"], color=color)
    plt.xlim(left=0)
    plt.show()
    # TODO: output to a file
