import numpy as np
import json
import sys

# Get the input of the regular expression
inpfile = sys.argv[1]
with open(inpfile, 'r') as fp:
    regexp = json.load(fp)
inp = regexp["regex"]
fname = sys.argv[2]
# Add concatenation operators
regex = [inp[0]]
for i in range(1, len(inp)):
    if (regex[-1] not in ['.', '+', '(']) and (inp[i]
                                               not in ['.', '+', '*', ')']):
        regex.append('.')
    regex.append(inp[i])

# Declare all possible operations
union = '+'
concat = '.'
closure = '*'


def precedence(operator):
    precedence_map = {"(": 0, ".": 3, "*": 4, "+": 2}
    if operator not in ["(", ".", "*", "+"]:
        return 4
    return precedence_map[operator]


def infix_to_postfix(regex):
    # Use shunting yard's algorithm to convert infix notation to postfix
    '''
    Precendence: 
    1. Paranthesis
    2. Kleene Star
    3. Concatenation
    4. Union
    '''
    output_queue = []
    operator_stack = []
    i = 0
    while i < len(regex):
        val = regex[i]
        if val == "(":
            operator_stack.append(val)
        elif val == ")":
            while operator_stack:
                if operator_stack[-1] == "(":
                    break
                output_queue.append(operator_stack[-1])
                operator_stack.pop()
            operator_stack.pop()
        else:
            while operator_stack:
                if precedence(operator_stack[-1]) >= precedence(val):
                    output_queue.append(operator_stack[-1])
                    operator_stack.pop()
                else:
                    break
            operator_stack.append(val)

        i = i + 1

    while operator_stack:
        output_queue.append(operator_stack[-1])
        operator_stack.pop()

    return output_queue


def remove_instance(start_state, inputs, next_state, transition):
    for i in range(0, len(transition)):
        if (transition[i]["start_state"] == start_state
                and transition[i]["input"] == inputs
                and transition[i]["next_state"] == next_state):
            # Remove the transition instance
            transition.pop(i)
            break


def exists_ephsilon(state1, state2, transition):
    for i in range(0, len(transition)):
        if transition[i]["start_state"] == state1 and transition[i][
                "next_state"] == state2 and transition[i]["input"] == '$':
            return 1
    return 0


def thomopson(output_queue):
    # Use thompson's algorithm to convert infix notation to postfix
    # let us try to convert regex to non-finite automata
    # in order to do so, we have to append the final starts of previous states
    # Declare all variables
    start_state = ''
    final_states = []
    alphabets = []
    transition = []
    state_set = []

    # Find the total number of alphabets in the regex
    for i in range(0, len(regex)):
        if (regex[i]
                not in alphabets) and ((regex[i] >= '0' and regex[i] <= '9') or
                                       (regex[i] >= 'a' and regex[i] <= 'z')):
            alphabets.append(regex[i])

    # take care of corner cases first
    if len(output_queue) == 1:
        if output_queue[0] == "$":
            transition.append({
                "start_state": 'q0',
                "input": '$',
                "next_state": 'q1'
            })
            start_state = 'q0'
            final_states.append('q1')
        elif output_queue[0] == "/":
            start_state = 'q0'
        elif (output_queue[0] >= '0'
              and output_queue[0] <= '9') or (output_queue[0] >= 'a'
                                              and output_queue[0] <= 'z'):
            val1 = output_queue[0]
            transition.append({
                "start_state": 'q' + '0',
                "input": val1,
                "next_state": 'q' + '1'
            })
            start_state = 'q0'
            final_states.append('q1')
        return state_set, start_state, final_states, alphabets, transition

    track_dict = {}
    thompson_stack = []
    j = 0
    i = 0
    while i < len(output_queue):
        if (output_queue[i] >= '0' and output_queue[i] <= '9') or (
                output_queue[i] >= 'a'
                and output_queue[i] <= 'z') or (output_queue[i] == '$'):
            thompson_stack.append(output_queue[i])
        if output_queue[i] == "+":
            val1 = thompson_stack.pop()
            val2 = thompson_stack.pop()
            new_str = "new" + str(i)
            final = []
            state_set.append('q' + str(j) + '4')
            if len(val1) == 1:
                transition.append({
                    "start_state": 'q' + str(j) + '0',
                    "input": val1,
                    "next_state": 'q' + str(j) + '1'
                })
                transition.append({
                    "start_state": 'q' + str(j) + '4',
                    "input": '$',
                    "next_state": 'q' + str(j) + '0'
                })
                state_set.append('q' + str(j) + '0')
                state_set.append('q' + str(j) + '1')
                final.append('q' + str(j) + '1')
            if len(val2) == 1:
                transition.append({
                    "start_state": 'q' + str(j) + '2',
                    "input": val2,
                    "next_state": 'q' + str(j) + '3'
                })
                transition.append({
                    "start_state": 'q' + str(j) + '4',
                    "input": '$',
                    "next_state": 'q' + str(j) + '2'
                })
                state_set.append('q' + str(j) + '2')
                state_set.append('q' + str(j) + '3')
                final.append('q' + str(j) + '3')
            if not len(val1) == 1:
                transition.append({
                    "start_state": 'q' + str(j) + '4',
                    "input": '$',
                    "next_state": track_dict[val1]["start_state"]
                })
                for k in range(0, len(track_dict[val1]["final_states"])):
                    final.append(track_dict[val1]["final_states"][k])
            if not len(val2) == 1:
                transition.append({
                    "start_state": 'q' + str(j) + '4',
                    "input": '$',
                    "next_state": track_dict[val2]["start_state"]
                })
                for k in range(0, len(track_dict[val2]["final_states"])):
                    final.append(track_dict[val2]["final_states"][k])
            track_dict[new_str] = {
                "start_state": 'q' + str(j) + '4',
                "final_states": final
            }
            thompson_stack.append(new_str)

            j += 1

        if output_queue[i] == "*":
            val1 = thompson_stack.pop()
            new_str = "new" + str(i)
            final = []
            start = ''
            if len(val1) == 1:
                transition.append({
                    "start_state": 'q' + str(j) + '0',
                    "input": val1,
                    "next_state": 'q' + str(j) + '1'
                })
                transition.append({
                    "start_state": 'q' + str(j) + '1',
                    "input": '$',
                    "next_state": 'q' + str(j) + '0'
                })
                transition.append({
                    "start_state": 'q' + str(j) + '2',
                    "input": '$',
                    "next_state": 'q' + str(j) + '0'
                })
                state_set.append('q' + str(j) + '0')
                state_set.append('q' + str(j) + '1')
                state_set.append('q' + str(j) + '2')
                final.append('q' + str(j) + '2')
                final.append('q' + str(j) + '1')
                start = 'q' + str(j) + '2'
            if not len(val1) == 1:
                for k in range(0, len(track_dict[val1]["final_states"])):
                    transition.append({
                        "start_state":
                        track_dict[val1]["final_states"][k],
                        "input":
                        '$',
                        "next_state":
                        track_dict[val1]["start_state"]
                    })
                    final.append(track_dict[val1]["final_states"][k])
                transition.append({
                    "start_state": 'q' + str(j) + '0',
                    "input": '$',
                    "next_state": track_dict[val1]["start_state"]
                })
                state_set.append('q' + str(j) + '0')
                start = 'q' + str(j) + '0'
                final.append('q' + str(j) + '0')
            track_dict[new_str] = {"start_state": start, "final_states": final}
            thompson_stack.append(new_str)

            j += 1

        if output_queue[i] == ".":
            val2 = thompson_stack.pop()
            val1 = thompson_stack.pop()
            final = []
            start = ''
            new_str = "new" + str(i)
            if len(val1) == 1:
                transition.append({
                    "start_state": 'q' + str(j) + '0',
                    "input": val1,
                    "next_state": 'q' + str(j) + '1'
                })
                state_set.append('q' + str(j) + '0')
                state_set.append('q' + str(j) + '1')
            if len(val2) == 1:
                transition.append({
                    "start_state": 'q' + str(j) + '2',
                    "input": val2,
                    "next_state": 'q' + str(j) + '3'
                })
                state_set.append('q' + str(j) + '2')
                state_set.append('q' + str(j) + '3')

            if len(val2) == 1 and (not len(val1) == 1):
                for k in range(0, len(track_dict[val1]["final_states"])):
                    transition.append({
                        "start_state":
                        track_dict[val1]["final_states"][k],
                        "input":
                        '$',
                        "next_state":
                        'q' + str(j) + '2'
                    })
                final.append('q' + str(j) + '3')
                start = track_dict[val1]["start_state"]
            elif len(val2) == 1 and (len(val1) == 1):
                transition.append({
                    "start_state": 'q' + str(j) + '1',
                    "input": '$',
                    "next_state": 'q' + str(j) + '2'
                })
                final.append('q' + str(j) + '3')
                start = 'q' + str(j) + '0'
            elif (not len(val2) == 1) and (len(val1) == 1):
                transition.append({
                    "start_state": 'q' + str(j) + '1',
                    "input": '$',
                    "next_state": track_dict[val2]["start_state"]
                })
                for k in range(0, len(track_dict[val2]["final_states"])):
                    final.append(track_dict[val2]["final_states"][k])
                start = 'q' + str(j) + '0'
            elif (not len(val2) == 1) and (not len(val1) == 1):
                for k in range(0, len(track_dict[val1]["final_states"])):
                    transition.append({
                        "start_state":
                        track_dict[val1]["final_states"][k],
                        "input":
                        '$',
                        "next_state":
                        track_dict[val2]["start_state"]
                    })
                for k in range(0, len(track_dict[val2]["final_states"])):
                    final.append(track_dict[val2]["final_states"][k])
                start = track_dict[val1]["start_state"]
            track_dict[new_str] = {"start_state": start, "final_states": final}
            thompson_stack.append(new_str)

            j += 1
        i += 1
    assign = thompson_stack.pop()
    start_state = track_dict[assign]["start_state"]
    final_states = track_dict[assign]["final_states"]
    return state_set, start_state, final_states, alphabets, transition


output_queue = infix_to_postfix(regex)
state_set, start_state, final_states, alphabets, transition = thomopson(
    output_queue)

transition_function = []
start_states = [start_state]
for i in range(0, len(transition)):
    transition_function.append([
        transition[i]["start_state"], transition[i]["input"],
        transition[i]["next_state"]
    ])

answer = {
    "states": state_set,
    "letters": alphabets,
    "transition_function": transition_function,
    "start_states": start_states,
    "final_states": final_states
}
with open(fname, 'w') as fp:
    json.dump(answer, fp, indent=4)
