from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import ray
import time
import numpy as np
import pickle


ray.init(num_cpus=4, include_webui=False, ignore_reinit_error=True, redis_max_memory=1000000000, object_store_memory=10000000000)


#TASK 1

@ray.remote
def slow_function(i):
    time.sleep(1)
    return i


#TASK 2

def task2(i):
    time.sleep(10.0)
    start_time = time.time()

    results = [slow_function.remote(i) for _ in range(4)]

    end_time = time.time()
    duration = end_time - start_time

    print('The results are {}. This took {} seconds. Run the next cell to see '
      'if the exercise was done correctly.'.format(results, duration))

    return results 

