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

    results = ray.get([slow_function.remote(i) for i in range(4)])

    end_time = time.time()
    duration = end_time - start_time

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

    results = ray.get(results)
    end_time = time.time()
    duration = end_time - start_time
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
    ready_ids, remaining_ids = ray.wait(result_ids, num_returns=3, timeout=None)
    initial_results = ray.get(ready_ids)

    end_time = time.time()
    duration = end_time - start_time

    remaining_results = ray.get(remaining_ids)

    assert len(initial_results) == 3
    assert len(remaining_results) == 3

    initial_indices = [result[0] for result in initial_results]
    initial_times = [result[1] for result in initial_results]
    remaining_indices = [result[0] for result in remaining_results]
    remaining_times = [result[1] for result in remaining_results]

    assert set(initial_indices + remaining_indices) == set(range(6))

    assert duration < 1.5, ('The initial batch of ten tasks was retrieved in '
                            '{} seconds. This is too slow.'.format(duration))

    assert duration > 0.8, ('The initial batch of ten tasks was retrieved in '
                            '{} seconds. This is too slow.'.format(duration))

    # Make sure the initial results actually completed first.
    assert max(initial_times) < min(remaining_times)

    print('Success! The example took {} seconds.'.format(duration))


#TASK 6

def task6():

    neural_net_weights = {'variable{}'.format(i): np.random.normal(size=1000000)
                      for i in range(50)}

    @ray.remote
    def use_weights(weights, i):
        return i


    # **EXERCISE:** In the code below, use `ray.put` to avoid copying the neural net weights 
    # to the object store multiple times.


    # Sleep a little to improve the accuracy of the timing measurements below.
    time.sleep(2.0)
    start_time = time.time()

    neural_net_weights_ids = ray.put(neural_net_weights)

    results = ray.get([use_weights.remote(neural_net_weights_ids, i)
                    for i in range(20)])

    end_time = time.time()
    duration = end_time - start_time


    # **VERIFY:** Run some checks to verify that the changes you made to the code were correct. Some of the checks should fail when you initially run the cells. After completing the exercises, the checks should pass.

    # In[34]:


    assert results == list(range(20))
    assert duration < 1, ('The experiments ran in {} seconds. This is too '
                        'slow.'.format(duration))

    print('Success! The example took {} seconds.'.format(duration))
