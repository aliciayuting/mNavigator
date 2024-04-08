
# Navigator: scheduler and object placement simulator
<br />

This Directory contains the Simulation code to run Navigator on Customized workflow and cluster.

## 1. set environment variable at the terminal 
### * For Unix/Linux
export SIMULATION_DIR=/path/to/simulation/directory
export PYTHONPATH="${PYTHONPATH}:{SIMULATION_DIR}"
### * For Windows
set PYTHONPATH=%PYTHONPATH%;C:\path\to\simulation\directory\

## 2. Simulatioin

### 2.1 Set Config and Workflow
At /simulation/core/config.py and 

### 2.2 Run simulation
Run the python file, /simulation/experiments/run_experiments.py , to start the simulation and generate logging data at ./experiment

``` python ./experiments/run_experiments.py <experiment_scheduler0> <experiment_scheduler1> ..(centralheft|decentralheft|hashtask) ```
