from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import ray
import time
import numpy as np
import pickle


# Start Ray. By default, Ray does not schedule more tasks concurrently than there are CPUs. 
# This example requires four tasks to run concurrently, so we tell Ray that there are four CPUs. 
# Usually this is not done and Ray computes the number of CPUs using `psutil.cpu_count()`. The argument `ignore_reinit_error=True` just ignores errors if the cell is run multiple times.
# The call to `ray.init` starts a number of processes.

ray.init(num_cpus=4, include_webui=False, ignore_reinit_error=True, redis_max_memory=1000000000, object_store_memory=10000000000)


# **EXERCISE:** The function below is slow. Turn it into a remote function using the `@ray.remote` decorator. 


# This function is a proxy for a more interesting and computationally
# intensive function.

@ray.remote
def slow_function(i):
    time.sleep(1)
    return i


