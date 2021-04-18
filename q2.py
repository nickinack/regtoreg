import numpy as np
import json
import math
import sys


def get_nfa(file_name):
    # Get the input from the NFA JSON file
    nfa = []
    with open(file_name, 'r') as f:
        nfa = json.load(f)
    return nfa


nfaname = sys.argv[1]
dfaname = sys.argv[2]


def get_powerset(state_set):
    # Given a set, return its powerset
    power_set_size = (int)(math.pow(2, len(state_set)))
    i = 0
    j = 0
    power_set = []
    for i in range(0, power_set_size):
        intermediate = []
        for j in range(0, len(state_set)):
            if ((i & (1 << j)) > 0):
                intermediate.append(state_set[j])
        power_set.append(intermediate)
    return power_set


def get_next_states(state, action, transition):
    next_states = []
    for i in range(0, len(transition)):
        if (transition[i][0] == state) and (transition[i][1] == action):
            next_states.append(transition[i][2])
    return next_states


def ephsilon_closure(state_set, transition):
    # Given a state set, return its ephsilon closure
    closure_stack = list(np.copy(state_set))
    closure = list(np.copy(state_set))
    while len(closure_stack) > 0:
        val = closure_stack.pop()
        next_states = get_next_states(val, '$', transition)
        for r in next_states:
            if r not in closure:
                closure.append(r)
                closure_stack.append(r)
    return closure


def get_reachable_states(state, action, transition, ephsilon_closure):
    reachable_states = []
    for i in range(0, len(transition)):
        for j in range(0, len(state)):
            if (transition[i][0] == state[j]) and (transition[i][1] == action):
                for m in ephsilon_closure[transition[i][2]]:
                    if m not in reachable_states:
                        reachable_states.append(m)
    return reachable_states


def construct_dfa(state_set, nfa, ephsilon_closure):
    # given nfa and new state set, computes and returns dfa tuple
    # append '$' to nfa's letters
    transition = []
    for i in range(0, len(state_set)):
        for l in range(0, len(nfa["letters"])):
            # search the entry for transition function
            # take ephsilon_closure(transition(ephsilon_closure(cur_state) , actions)))
            next_states = get_reachable_states(state_set[i], nfa["letters"][l],
                                               nfa["transition_function"],
                                               ephsilon_closure)
            transition.append([state_set[i], nfa["letters"][l], next_states])

    # append final state unions as a part of final states
    final_states = []
    for i in range(0, len(state_set)):
        for j in range(0, len(nfa["final_states"])):
            if nfa["final_states"][j] in state_set[i]:
                final_states.append(state_set[i])
                break

    return state_set, nfa["letters"], transition, ephsilon_closure[
        nfa["start_states"][0]], final_states


def get_ephsilon_closure(nfa_states, transition):
    # Given a state, make a dictionary with key being state and value being ephsilon closure
    ephsilon_closure_set = {}
    for r in nfa_states:
        ephsilon_closure_set[r] = ephsilon_closure([r], transition)
    return ephsilon_closure_set


nfa = get_nfa(nfaname)
ephsilon_closure_set = get_ephsilon_closure(nfa["states"],
                                            nfa["transition_function"])
power_set = get_powerset(nfa["states"])
state_set, letters, transition_function, start_states, final_states = construct_dfa(
    power_set, nfa, ephsilon_closure_set)

answer = {
    "states": state_set,
    "letters": letters,
    "transition_function": transition_function,
    "start_states": [start_states],
    "final_states": final_states
}

with open(dfaname, 'w') as fp:
    json.dump(answer, fp, indent=4)
