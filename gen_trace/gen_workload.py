import numpy as np
import json as js

def gen_trace(num_jobs, time_dist=25, length=30, pred_length = 10, size=2):
  start_times  = np.random.poisson(time_dist, num_jobs) + 1
  run_lengths  = np.random.poisson(length, num_jobs) + 1
  pred_lengths = np.random.poisson(pred_length, num_jobs) + 1
  nodes        = np.random.poisson(size, num_jobs) + 1

  for i in range(num_jobs):
    if nodes[i] >= 6:
      nodes[i] = 5

  job_arrays = []

  cur_time = 100
  for i in range(num_jobs):
    cur_time += start_times[i]
    temp = { "username": f"tester_{i}",
             "account": f"{i}",
             "submit": int(cur_time),
             "duration": int(run_lengths[i]),
             "wclimit": int(run_lengths[i] + pred_lengths[i]),
             "tasks": int(nodes[i] * 8),
             "cpus_per_task": 1,
             "tasks_per_node": 8,
             "partition": "all",
             "nice": 0}
    job_arrays.append(temp)
  return job_arrays


def inject_jobs(jobs, num_jobs, length=5, pred_length=5, size=5):
  run_lengths  = np.random.poisson(length, num_jobs) + 1
  pred_lengths = np.random.poisson(pred_length, num_jobs) + 1
  nodes        = np.random.poisson(size, num_jobs) + 1

  for i in range(num_jobs):
    if nodes[i] >= 6:
      nodes[i] = 5

  ind = len(jobs) // 2

  cur_time = jobs[ind]["submit"]
  job_arrays = []
  for i in range(num_jobs):
    temp = { "username": f"injector",
             "account": "inject:100",
             "submit": cur_time,
             "duration": int(run_lengths[i]),
             "wclimit": int(run_lengths[i] + pred_lengths[i]),
             "tasks": int(nodes[i] * 8),
             "cpus_per_task": 1,
             "tasks_per_node": 8,
             "partition": "all",
             "nice":0}
    job_arrays.append(temp)
  return np.insert(jobs, ind, job_arrays).tolist()


def add_job_inds(jobs):
  for ind in range(len(jobs)):
    jobs[ind]["job_id"] = ind+1

  return jobs

if __name__=="__main__":
  import sys
  jobs = gen_trace(int(sys.argv[1]))
  inj_jobs = inject_jobs(jobs, int(sys.argv[2]))
  fin_jobs = add_job_inds(inj_jobs)

  with open(sys.argv[3], 'w') as f:
    js.dump(fin_jobs, f, indent=2)
