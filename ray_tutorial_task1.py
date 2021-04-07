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

def task2():
    time.sleep(10.0)
    start_time = time.time()

    results = [slow_function.remote(i) for i in range(4)]

    end_time = time.time()
    duration = end_time - start_time

    results = ray.get(results)
    print('The results are {}. This took {} seconds. Run the next cell to see '
      'if the exercise was done correctly.'.format(results, duration))

    assert results == [0, 1, 2, 3], 'Did you remember to call ray.get?'
    assert duration < 1.1, ('The loop took {} seconds. This is too slow.'
                        .format(duration))
    assert duration > 1, ('The loop took {} seconds. This is too fast.'
                      .format(duration)) 

    print('Success! The example took {} seconds.'.format(duration))


#TASK 3

def task3():

    @ray.remote
    def load_data(filename):
        time.sleep(0.1)
        return np.ones((1000, 100))

    @ray.remote
    def normalize_data(data):
        time.sleep(0.1)
        return data - np.mean(data, axis=0)

    @ray.remote
    def extract_features(normalized_data):
        time.sleep(0.1)
        return np.hstack([normalized_data, normalized_data ** 2])

    @ray.remote
    def compute_loss(features):
        num_data, dim = features.shape
        time.sleep(0.1)
        return np.sum((np.dot(features, np.ones(dim)) - np.ones(num_data)) ** 2)

    assert hasattr(load_data, 'remote'), 'load_data must be a remote function'
    assert hasattr(normalize_data, 'remote'), 'normalize_data must be a remote function'
    assert hasattr(extract_features, 'remote'), 'extract_features must be a remote function'
    assert hasattr(compute_loss, 'remote'), 'compute_loss must be a remote function'

    time.sleep(2.0)
    start_time = time.time()

    losses = []
    for filename in ['file1', 'file2', 'file3', 'file4']:
        inner_start = time.time()

        data = load_data.remote(filename)
        normalized_data = normalize_data.remote(data)
        features = extract_features.remote(normalized_data)
        loss = compute_loss.remote(features)
        losses.append(loss)
        
        inner_end = time.time()
        
        if inner_end - inner_start >= 0.1:
            raise Exception('You may be calling ray.get inside of the for loop! '
                            'Doing this will prevent parallelism from being exposed. '
                            'Make sure to only call ray.get once outside of the for loop.')

    losses = ray.get(losses)
    print('The losses are {}.'.format(losses) + '\n')
    loss = sum(losses)

    end_time = time.time()
    duration = end_time - start_time

    print('The loss is {}. This took {} seconds. Run the next cell to see '
        'if the exercise was done correctly.'.format(loss, duration))

    assert loss == 4000
    assert duration < 0.8, ('The loop took {} seconds. This is too slow.'
                        .format(duration))
    assert duration > 0.4, ('The loop took {} seconds. This is too fast.'
                        .format(duration))

    print('Success! The example took {} seconds.'.format(duration))


# TASK 4

def task4():

    @ray.remote
    class Foo(object):
        def __init__(self):
            self.counter = 0

        def reset(self):
            self.counter = 0

        def increment(self):
            time.sleep(0.5)
            self.counter += 1
            return self.counter

    assert hasattr(Foo, 'remote'), 'You need to turn "Foo" into an actor with @ray.remote.'

    f1 = Foo.remote()
    f2 = Foo.remote()

    time.sleep(2.0)
    start_time = time.time()

    f1.reset.remote()
    f2.reset.remote()

    results = []
    for _ in range(5):
        results.append(f1.increment.remote())
        results.append(f2.increment.remote())

    end_time = time.time()
    duration = end_time - start_time
    results = ray.get(results)
    print("Results are: ", results)

    assert not any([isinstance(result, ray.ObjectID) for result in results]), 'Looks like "results" is {}. You may have forgotten to call ray.get.'.format(results)

    assert results == [1, 1, 2, 2, 3, 3, 4, 4, 5, 5]

    assert duration < 3, ('The experiments ran in {} seconds. This is too '
                      'slow.'.format(duration))
    assert duration > 2.5, ('The experiments ran in {} seconds. This is too '
                        'fast.'.format(duration))

    print('Success! The example took {} seconds.'.format(duration))


    #TASK 5

    def task5():

        @ray.remote
        def f(i):
            np.random.seed(5 + i)
            x = np.random.uniform(0, 4)
            time.sleep(x)
            return i, time.time()


        # **EXERCISE:** Using `ray.wait`, change the code below so 
        # that `initial_results` consists of the outputs of the first three tasks 
        # to complete instead of the first three tasks that were submitted.

        # Sleep a little to improve the accuracy of the timing measurements below.
        time.sleep(2.0)
        start_time = time.time()

        # This launches 6 tasks, each of which takes a random amount of time to
        # complete.
        result_ids = [f.remote(i) for i in range(6)]
        # Get one batch of tasks. Instead of waiting for a fixed subset of tasks, we
        # should instead use the first 3 tasks that finish.
        initial_results = ray.get(result_ids[:3])

        ready_ids, remaining_ids = ray.wait(initial_results, num_returns=3, timeout=None)
        print("Ready ids: ", ready_ids)
        print("remaining ids: ", remaining_ids)

        end_time = time.time()
        duration = end_time - start_time

