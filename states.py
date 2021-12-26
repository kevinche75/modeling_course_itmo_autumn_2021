import numpy as np
from numpy.core.fromnumeric import ptp
from create_queue import get_queue_states
from tabulate import tabulate

class Unit():

    def __init__(self, p, capacity, i) -> None:
        self.p = p
        self.capacity = capacity
        self.i = i

class Agent():

    def __init__(self, lambd, mu, i) -> None:
        self.lambd = lambd
        self.mu = mu
        self.i = i

class State():

    def __init__(self, queue, smo):
        self.queue = queue
        self.smo = smo

    def to_string(self):
        return str(list(self.queue)) + " " + str(self.smo)

lam = "λ"
mu = "μ"

units_names = [[1, 2]]

def create_agents(number):
    agents = []
    for i in range(number):
        agents.append(Agent(lam+str(i+1), mu+str(i+1), i+1))

    return agents

def create_units(units_names):
    units = []
    for i, [p, capacity] in enumerate(units_names):
        units.append(Unit(p, capacity, i))
    return units

def create_states(agents, queue_states):
    states = []
    for queue_state in queue_states:
        for agent in agents:
            states.append(State(queue_state, agent.i))
    return states

def check_diff(diff):
    n = len(diff[diff == 0])
    if n == len(diff)-1:
        return sum(diff)
    return 2


agents = create_agents(4)
agents = np.array(agents)
units = create_units(units_names)
queue_states = get_queue_states(len(agents), units[0].capacity)
queue_states = np.array(queue_states)
states_with_smo = [State(queue_states[0], 0)] + create_states(agents, queue_states)

for state in states_with_smo:
    print(state.to_string())
transitions = np.full((len(states_with_smo), len(states_with_smo)), '0', 'U4')

for i in range(transitions.shape[0]):
    state_i = states_with_smo[i]
    for j in range(transitions.shape[1]):
        state_j = states_with_smo[j]
        diff = np.add(-1 * state_i.queue, state_j.queue)

        if np.array_equal(state_i.queue, state_j.queue) and state_i.smo == state_j.smo:
            continue

        if sum(state_i.queue) == 0 and sum(state_j.queue) == 0:
            if (state_i.smo == 0):
                transitions[i, j] = agents[state_j.smo-1].lambd
                continue
            if(state_j.smo == 0):
                transitions[i, j] = agents[state_i.smo-1].mu
                continue

        diff_one = check_diff(diff)

        if state_i.smo == state_j.smo and diff_one == 1:
            transitions[i, j] = agents[np.array(diff, dtype=bool)][0].lambd
            continue
        
        if diff_one == -1:
            if sum(state_i.queue[:2]) > 0 and state_j.smo > 2:
                continue
            agent_from_queue = agents[np.array(np.abs(diff), dtype=bool)][0]
            if agent_from_queue.i != state_j.smo:
                continue
            transitions[i, j] = agents[state_i.smo-1].mu
            continue

f = open("matrix.csv", 'w')
for i in range(len(transitions)):
    for j in range(len(transitions)):
        if j == len(transitions)-1:
            f.write(transitions[i, j] + "\n")
        else:
            f.write(transitions[i, j] + ",")
f.close()