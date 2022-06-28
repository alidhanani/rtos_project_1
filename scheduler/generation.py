import random
import math

def gen(tasks_number, utilization):
    tasks = []
    
    # We arbitrarily set a max when creating random ints
    max_period = 100
    max_offset = 30
    
    # We create tasks one at a time.
    # Each task has some random utilization less than the total utilization.
    # For each task, we subtract the task utilization from the total utilization.
    for task in range(0, tasks_number - 1):
        offset = random.randint(0, max_offset)

        # We should leave at least 1 utilization for each remaining task
        max_utilization = utilization - (tasks_number - task) + 1
        task_utilization = random.randint(1, max_utilization)

        # We need to chose a period high enough so wcet can be at least 1
        min_period = math.ceil(100 / task_utilization)
        period = random.randint(min_period, max_period)

        # Note that for a single task: utilization = wcet / period
        # Then we know that: wcet = utilization * period
        # After we chose a random task_utilization and a random period, we calculate the wcet
        wcet = int(task_utilization * period / 100)
        tasks.append({ "offset": offset, "wcet": wcet, "period": period , "id": task})
        utilization -= task_utilization
        
    # Generate the last task. We make sure that it consumes the remaining utilization.
    offset = random.randint(0, max_offset)
    period = random.randint(math.ceil(100/utilization), max_period)
    wcet = int(utilization * period / 100)
    tasks.append({ "offset": offset, "wcet": wcet, "period": period, "id": tasks_number - 1 })
    return tasks
