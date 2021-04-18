import numpy as np
import json
import sys

# Using the Transitive closure method


def get_dfa(file_name):
    # Given a file, retrieve the DFA
    dfa = []
    with open(file_name, 'r') as f:
        dfa = json.load(f)
    return dfa


dfaname = sys.argv[1]
regname = sys.argv[2]


def exists_transition(cur_state, letter, next_state, transition_function):
    # Gives the entries in transition
    for i in range(0, len(transition_function)):
        if transition_function[i][0] == cur_state and transition_function[i][1] == letter and transition_function[i][2] == next_state:
            return 1
    return 0


def remove_multi_edges(transition_function, state_set, letters):
    # Given a transition function, index it and return the index array
    L = [['' for i in range(len(state_set))] for j in range(len(state_set))]
    for r1 in state_set:
        for r2 in state_set:
            if r1 == r2:
                L[r1][r2] = '$'
            else:
                L[r1][r2] = '∅'
            for l in letters:
                if exists_transition(r1, l, r2, transition_function):
                    L[r1][r2] = operate_plus(L[r1][r2], l)
    return L


def initialize(transition_function, state_set, letters):
    L = [[['' for i in range(len(state_set))] for j in range(
        len(state_set))] for k in range(len(state_set))]
    for r1 in state_set:
        for r2 in state_set:
            if r1 == r2:
                L[0][r1][r2] = '$'
            else:
                L[0][r1][r2] = '∅'
            for l in letters:
                if exists_transition(r1, l, r2, transition_function):
                    L[0][r1][r2] = operate_plus(L[0][r1][r2], l)
    return L


def star(symbol):
    if symbol == '$':
        return '$'
    if symbol == '∅':
        return '∅'
    else:
        return symbol + '*'


def operate_concat(symbol1, symbol2):
    if symbol1 == '$':
        return symbol2
    if symbol2 == '$':
        return symbol1
    if symbol1 == '∅' or symbol2 == '∅':
        return '∅'
    return '(' + symbol1 + symbol2 + ')'


def operate_plus(symbol1, symbol2):
    if symbol1 == '∅':
        return symbol2
    if symbol2 == '∅':
        return symbol1
    if symbol1 == '$' and symbol2 == '$':
        return '$'
    if symbol1 == symbol2:
        return symbol1
    return '(' + symbol1 + '+' + symbol2 + ')'


def remove(k, L, state_set):
    # Given a state k for removal, perform removal operations

    for r1 in state_set:
        for r2 in state_set:
            L[r1][r1] = operate_plus(L[r1][r1], operate_concat(
                L[r1][k], operate_concat(star(L[k][k]), L[k][r1])))
            L[r2][r2] = operate_plus(L[r2][r2], operate_concat(
                L[r2][k], operate_concat(star(L[k][k]), L[k][r2])))
            L[r1][r2] = operate_plus(L[r1][r2], operate_concat(
                L[r1][k], operate_concat(star(L[k][k]), L[k][r2])))
            L[r2][r1] = operate_plus(L[r2][r1], operate_concat(
                L[r2][k], operate_concat(star(L[k][k]), L[k][r1])))

    return L


def algo_2(L, state_set):
    for k in state_set:
        for i in state_set:
            for j in state_set:
                if k > 0:
                    L[k][i][j] = operate_plus(L[k-1][i][j], operate_concat(
                        L[k - 1][i][k], operate_concat(star(L[k - 1][k][k]), L[k - 1][k][j])))
                if k == 0:
                    L[k][i][j] = operate_plus(L[k][i][j], operate_concat(
                        L[k][i][k], operate_concat(star(L[k][k][k]), L[k][k][j])))
    return L


def get_state_index(state, state_set):
    for i in range(0, len(state_set)):
        if set(state) == set(state_set[i]):
            return i


def index(dfa):
    # Given a dfa, index the dfa
    new_states = []
    new_transition = []
    new_start_states = []
    new_final_states = []
    if dfa["start_states"][0] in dfa["final_states"]:
        dfa["states"].append('Q1')
        dfa["states"].append('Q2')
        dfa["transition_function"].append(['Q1', '$', dfa["start_states"][0]])
        for m in dfa["final_states"]:
            dfa["transition_function"].append([m, '$', 'Q2'])
        dfa["final_states"] = ['Q2']
        dfa["start_states"][0] = 'Q1'
        dfa["letters"].append('$')
    for i in range(0, len(dfa["states"])):
        new_states.append(i)
    for m in dfa["transition_function"]:
        new_transition.append(
            [get_state_index(m[0], dfa["states"]), m[1], get_state_index(m[2], dfa["states"])])
    for m in dfa["start_states"]:
        new_start_states.append(get_state_index(m, dfa["states"]))
    for m in dfa["final_states"]:
        new_final_states.append(get_state_index(m, dfa["states"]))
    new_dfa = {
        "states": new_states,
        "letters": dfa["letters"],
        "transition_function": new_transition,
        "start_states": new_start_states,
        "final_states": new_final_states
    }
    return new_dfa


dfa1 = get_dfa(dfaname)
dfa = index(dfa1)
L = initialize(dfa["transition_function"],
               dfa["states"], dfa["letters"])
# for i in range(0, len(L[0])):
#    print(L[0][i])
'''
for m in dfa["states"]:
    if m not in dfa["start_states"] or m not in dfa["final_states"]:
        remove(m, L, dfa["states"])
'''
L1 = algo_2(L, dfa["states"])

s = dfa["start_states"][0]
ans = '∅'
last = len(dfa["states"]) - 1
for m in dfa["states"]:
    if m in dfa["final_states"]:
        ans = operate_plus(ans, L1[last][s][m])
answer = {
    "regex": ans
}
with open(regname, 'w') as fp:
    json.dump(answer, fp, indent=4)
