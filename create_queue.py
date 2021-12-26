def get_queue_state(r, n, t, acc=[]):
    if t == 0:
        if n >= 0:
            yield acc
        return
    for x in r:
        if x > n:  # <---- do not recurse if sum is larger than `n`
            break
        for lst in get_queue_state(r, n-x, t-1, acc + [x]):
            yield lst

def get_queue_states(states_number, resources_number):
    i = 0
    states = []
    for xs in get_queue_state(range(resources_number+1), resources_number, states_number):
        states.append(xs)
        i+=1

    print(i)
    return states

print(get_queue_states(4, 2))