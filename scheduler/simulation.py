class SimulationResult:
    def __init__(self):
        self.job_history = []
        self.failed_task = None

    def is_infeasible(self):
        return self.failed_task != None

def simulation(tasks, end_time):
    runningJobs = []
    sim_result = SimulationResult()
    job_count = [0] * len(tasks)
    for time in range(0, end_time + 1):
        failed_task = completed_before_deadline(time, runningJobs)
        if failed_task != None:
            sim_result.failed_task = failed_task
            return sim_result
        add_jobs(time,  tasks, runningJobs, job_count)
        executed_job = run_job(time, tasks, runningJobs)
        update_job_history(time, sim_result, executed_job)
    return sim_result

def completed_before_deadline(time, runningJobs):
    if not runningJobs:
        return None
    for job in runningJobs:
        if time >= job["deadline"]: 
            return job["taskId"]
    return None  

def add_jobs(time, tasks, runningJobs, job_count):
    n = 0
    for task in tasks:
        job_is_at_release_time = (time -task["offset"]) % task["period"] == 0
        wcet_is_nonzero = task["wcet"] != 0
        if job_is_at_release_time and wcet_is_nonzero:
            runningJobs.append({
                "deadline": time + task["period"],
                "remainingComputationTime": task["wcet"],
                "taskId": task["id"],
                "upgradeTime": time + task["upgradeTime"],
                "jobId": job_count[task["id"]]
            })
            job_count[task["id"]] += 1        

# 1. Find highest priority job
# 2. Run the highest priority job for 1 second
# 3. If the job is finished, pop it from runningJobs
def run_job(time, tasks, runningJobs):
    if not runningJobs:
        return None
    highestPriorityJob = runningJobs[0]
    highestPriorityTask = get_task(tasks, highestPriorityJob["taskId"])
    highestPriority = get_priority(time, highestPriorityTask, highestPriorityJob)
    for job in runningJobs:
        task = get_task(tasks, job["taskId"])
        priority = get_priority(time, task, job)
        if priority < highestPriority:
            highestPriorityJob = job
            highestPriority  = priority
    highestPriorityJob["remainingComputationTime"] -= 1
    if highestPriorityJob["remainingComputationTime"] == 0:
        runningJobs.remove(highestPriorityJob)
    return {
        "taskId": highestPriorityJob["taskId"],
        "jobId": highestPriorityJob["jobId"]
    }

def update_job_history(time, sim_result, executed_job):
    if not executed_job:
        # No job was executed, so no need to update the history
        return
    elif not sim_result.job_history:
        # This is the first job we've executed, so we simply add it to the history
        add_new_job_to_history(time, sim_result, executed_job)
    else:
        previous_job = sim_result.job_history[-1]
        is_same_task = previous_job["taskId"] == executed_job["taskId"]
        is_same_job = previous_job["jobId"] == executed_job["jobId"]
        if is_same_task and is_same_job:
            # update the existing job history item
            previous_job["stopTime"] += 1
        else:
            add_new_job_to_history(time, sim_result, executed_job)

def add_new_job_to_history(time, sim_result, executed_job):
    executed_job["startTime"] = time
    executed_job["stopTime"] = time + 1
    sim_result.job_history.append(executed_job)

def get_task(tasks, taskId):            
    for task in tasks:
        if task["id"] == taskId:
            return task

def get_priority(time, task, job):
    if time < job["upgradeTime"]:
        return task["normalPriority"]
    else:
        return task["emergencyPriority"]
