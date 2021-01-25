import sys
import json

if len(sys.argv) < 2:
  print("No input file name")
  exit()

in_file = sys.argv[1]
o_file = "default.swf"
if len(sys.argv) > 2:
  o_file = sys.argv[2]

with open(in_file) as f:
  d = json.load(f)

keys =      ["job_id", "username", "submit"   , "duration", "wclimit",
             "tasks" , "qosname" , "partition", "account" , "cpus_per_task",
             "tasks_per_node", "nice", "req_nodes"]
defaults =  {"job_id":0, "username":"tester", "submit":0, "duration":0,
             "wclimit":0, "tasks":0, "qosname":"none", "partition":"all",
             "account":"1000", "cpus_per_task":0, "tasks_per_node":0, "nice":0, "req_nodes":"ice115"}

with open(o_file, 'w') as o:
  o.write(f"{len(d)}\n")
  for job in d:
    for key in keys:
      if key in job.keys():
        o.write(f"{job[key]} ")
      else:
        o.write(f"{defaults[key]} ")
    o.write("\n")
