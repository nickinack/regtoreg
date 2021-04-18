import numpy as np
import json
import math
import sys


def get_dfa(file_name):
    # Given a file, retrieve the DFA
    dfa = []
    with open(file_name, 'r') as f:
        dfa = json.load(f)
    return dfa


dfaname = sys.argv[1]
optname = sys.argv[2]


def get_index_from_state_set(state, state_set):
    # Given state, return index of the state in state_set
    for i in range(0, len(state_set)):
        if set(state) == set(state_set[i]):
            return i


def get_reachable_states(cur_state, l, transition):
    # Given state and letter, get all reachable states form this state
    reachable_states = []
    for r in transition:
        if set(r[0]) == set(cur_state) and r[1] == l:
            reachable_states.append(r[2])
    return reachable_states


def get_next_states(cur_state, l, transition):
    # Given the state and letter, find the next state in transition
    for m in transition:
        if m[0] == cur_state and m[1] == l:
            return m[2]
    return None


def get_partition_index(p, state):
    # Given the partition and a singleton state, return the state set it is a part of
    for i in range(0, len(p)):
        if state in p[i]:
            return i


def dfa_reduction(dfa):
    # Given dfa, return a new dfa which only contains reachable states
    visited = []
    for m in dfa["states"]:
        visited.append(0)
    start_state = dfa["start_states"][0]
    stack = [start_state]
    letters = dfa["letters"]
    state_set = dfa["states"]
    new_state_set = [start_state]
    transition = []
    while len(stack) > 0:
        cur_state = stack.pop()
        visited[get_index_from_state_set(cur_state, state_set)] = 1
        for l in letters:
            reachable_states = get_reachable_states(
                cur_state, l, dfa["transition_function"])
            for z in reachable_states:
                if not visited[get_index_from_state_set(z, state_set)]:
                    stack.append(z)
                if z not in new_state_set:
                    new_state_set.append(z)
                transition.append([cur_state, l, z])

    final_states = []
    for m in state_set:
        if m in dfa["final_states"]:
            final_states.append(m)

    new_dfa = {
        "states": new_state_set,
        "letters": letters,
        "transition_function": transition,
        "start_states": dfa["start_states"],
        "final_states": final_states
    }

    return new_dfa


def get_reachable_states_from_cur(partition, l, transition):
    reachable_states_from = []
    for r in transition:
        if r[2] in partition and r[1] == l:
            reachable_states_from.append(r[0])
    return reachable_states_from


def intersection_exists(m, x):
    for m1 in m:
        if m1 in x:
            return 1
    return 0


def intersection(m, x):
    intersection = []
    for m1 in m:
        if m1 in x:
            intersection.append(m1)
    return intersection


def get_y(x, p):
    y = []
    index = []
    for i in range(0, len(p)):
        m = p[i]
        if intersection_exists(m, x) and len(list(set(m) - set(x))) > 0:
            y.append(m)
    return y


def get_y_index(p, y):
    for i in range(0, len(p)):
        if set(p[i]) == set(y):
            return i
    return -1


def optimize_dfa(dfa):
    # Given a dfa, optimize the dfa
    p = []
    w = []
    partition1 = []
    partition2 = []
    for m in dfa["states"]:
        if m not in dfa["final_states"]:
            partition1.append(m)
        else:
            partition2.append(m)
    if partition1 != []:
        p.append(partition1)
        w.append(partition1)
    if partition2 != []:
        p.append(partition2)
        w.append(partition2)
    while len(w) > 0:
        cur_partition = w.pop()
        for l in dfa["letters"]:
            x = get_reachable_states_from_cur(
                cur_partition, l, dfa["transition_function"])
            y1 = get_y(x, p)
            for y in y1:
                del p[get_y_index(p, y)]
                p.append(intersection(y, x))
                p.append(list(set(y) - set(x)))
                if get_y_index(w, y) != -1:
                    del w[get_y_index(w, y)]
                    w.append(intersection(y, x))
                    w.append(list(set(y) - set(x)))
                else:
                    if len(intersection(x, y)) > len(list(set(y) - set(x))):
                        w.append(intersection(x, y))
                    else:
                        w.append(list(set(y) - set(x)))

    return p


def create_new_dfa(p, transition, old_dfa):
    # Given a parition and transition, return the new DFA
    start_states = []
    for m in p:
        if old_dfa["start_states"][0] in m:
            start_states.append(m)
            break
    final_states = []
    for m in p:
        for n in old_dfa["final_states"]:
            if n in m:
                if m not in final_states:
                    final_states.append(m)
    letters = old_dfa["letters"]
    state_set = p
    transition_function = []
    for m in p:
        # take any state in m, say m[0]
        cur_state = m[0]
        for l in letters:
            # get transition function for the state,letter combination
            next_state = get_next_states(cur_state, l, transition)
            if next_state != None:
                index = get_partition_index(p, next_state)
                transition_function.append([m, l, p[index]])
    new_dfa = {
        "states": state_set,
        "letters": letters,
        "transition_function": transition_function,
        "start_states": start_states,
        "final_states": final_states
    }
    return new_dfa


old_dfa = get_dfa(dfaname)
dfa = dfa_reduction(old_dfa)
p = optimize_dfa(dfa)
# Create a new dfa for these newly created partitions
new_dfa = create_new_dfa(p, dfa["transition_function"], old_dfa)
with open(optname, 'w') as fp:
    json.dump(new_dfa, fp, indent=4)
