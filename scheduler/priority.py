import scheduler.simulation as sim
import math
import functools

def set_priority(tasks):
    set_initial_priority(tasks)
    hyperperiod = get_hyperperiod(tasks)
    simulation_result = sim.simulation(tasks, hyperperiod)
    while simulation_result.is_infeasible():
        failed_task = get_task(tasks, simulation_result.failed_task)
        if failed_task["upgradeTime"] == 0:
            return False
        failed_task["upgradeTime"] -= 1
        simulation_result = sim.simulation(tasks, hyperperiod)
    return True    

def set_initial_priority(tasks):
    tasks = sorted(tasks, key=lambda x: x["period"], reverse=False)
    emergencyPriority = 1
    normalPriority = len(tasks) + 1
    for i in tasks:
        i["emergencyPriority"] = emergencyPriority
        i["normalPriority"] = normalPriority
        i["upgradeTime"] = i["period"]
        emergencyPriority += 1
        normalPriority += 1

def get_hyperperiod(tasks):
    return functools.reduce(
        lambda hp,task: lcm(hp, task["period"]),
        tasks,
        1
    )

def lcm(a, b):
    return a * b // math.gcd(a, b)

def get_task(tasks, taskId):            
    for task in tasks:
        if task["id"] == taskId:
            return task
