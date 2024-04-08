""" --------      Worker Machines Parameters      -------- """
GPU_MEMORY_SIZE = 14000000  # in KB, 15BG for Tesla T4

TOTAL_NUM_OF_WORKERS = 5


"""  --------       Workload Parameters    --------  """
TOTAL_NUM_OF_JOBS = 1000

# The interval between two consecutive job creation events at each external client
DEFAULT_JOB_CREATION_INTERVAL = 2000     # ms. 

WORKLOAD_DISTRIBUTION = "UNIFORM"  # UNIFORM | POISON | GAMMA

GAMMA_CV = 10  # Coefficient of variation for gamma distribution


"""  -------        Navigator Parameters  --------- """
LOAD_INFORMATION_STALENESS = 10  # in ms

PLACEMENT_INFORMATION_STALENESS = 10  # in ms

RESCHEDULE_THREASHOLD = 1.5