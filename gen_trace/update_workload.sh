#!/bin/sh

python3 gen_workload.py 2000 100 test2.json
python3 json_to_swf.py test2.json test2.swf
./swf2trace test2.swf
mv simple.trace test2.trace
cp test2.trace ../../simulator/slurm_simulator_tools/workloads/
