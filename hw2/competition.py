import ray
import time
from copy import deepcopy
import matplotlib.pyplot as plt
from random import randint, choice
import pickle


@ray.remote
class VI_server_v2(object):
    #INSERT YOUR CODE HERE
    def __init__(self, size):
        self.v_current = [0] * size
        self.v_new = [0] * size
        self.pi = [0] * size

    def get_value_and_policy(self):
        return self.v_current, self.pi

    def update(self, start_state, end_state, batch_v, batch_a):
        self.v_new[start_state : end_state] = batch_v
        self.pi[start_state : end_state] = batch_a

    def get_error_and_update(self):
        max_error = 0
        for i in range(len(self.v_current)):
            error = abs(self.v_new[i] - self.v_current[i])
            if error > max_error:
                max_error = error
            self.v_current[i] = self.v_new[i]
        return max_error
    
@ray.remote
def VI_worker_v2(VI_server, data, start_state, end_state):
        env, workers_num, beta, epsilon = data
        A = env.GetActionSpace()
        S = env.GetStateSpace()
        
        V, _ = ray.get(VI_server.get_value_and_policy.remote())
        
        state = start_state
        batch_v, batch_a = [], []
        while state < end_state:
            max_v = float('-inf')
            max_a = 0
            for action in range(A):
                successors = env.GetSuccessors(state, action)
                transition_value = 0
                for observation, transition_prob in successors:
                    transition_value += transition_prob * V[observation]
                bellman_v = env.GetReward(state, action) + (beta * transition_value)
                if bellman_v > max_v:
                    max_v = bellman_v
                    max_a = action
            state += 1
            batch_v.append(max_v)
            batch_a.append(max_a)
        VI_server.update.remote(start_state, end_state, batch_v, batch_a)


def fast_value_iteration(env, beta = 0.999, epsilon = epsilon, workers_num = 4):
    S = env.GetStateSpace()
    VI_server = VI_server_v2.remote(S)
    workers_list = []
    data_id = ray.put((env, workers_num, beta, epsilon))

    error = float('inf')
    while error > epsilon:
        batch_size = S // workers_num
        remaining = S % workers_num
        workers_list = []
        for i in range(workers_num):
            start = i * batch_size
            end = start + batch_size
            if i == workers_num - 1:
                end += remaining - 1
            w_id = VI_worker_v2.remote(VI_server, data_id, start, end)
            workers_list.append(w_id)
        results, _ = ray.wait(workers_list, num_returns=workers_num, timeout=None)
        error = ray.get(VI_server.get_error_and_update.remote())
        
    v, pi = ray.get(VI_server.get_value_and_policy.remote())
        
    return v, pi