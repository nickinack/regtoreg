# Automata Theory

Designing finite optimised automaton from regular expressions, and converting them back into regular expressions! The repository consists of the following codes:

| Code        | Description |
| ----------- | ----------- |
| q1.py       | Convert a Regular Expression into Non-Deterministic Finite Automaton using Thompson's algorithm       |
| q2.py      | Convert a Non-Deterministic Finite Automaton into a Deterministic Finite Automaton with 2^k states        |
| q3.py      | Convert a Deterministic Finite Automaton into Regular Expression using the Transitive Closure Method        |
| q4.py      | Optimize a Deterministic Finite Automaton using Hopcroft's algorithm        |

## Execution
 
In order to execute the codes, use the following command
```bash
python3 <file_name>.py arg1 arg2
```


| Code        | Arguments |
| ----------- | ----------- |
| q1.py       | REG JSON, NFA JSON   |
| q2.py      | NFA JSON, DFA JSON        |
| q3.py      | DFA JSON, REG JSON|
| q4.py      | DFA JSON, OPT JSON|

The second argument consists of the file name where you would like to store your result.

# Approach and Assumptions

A brief table on how each problem has been approached:

| Code        | Approach |
| ----------- | ----------- |
| q1.py       | Convert the regular expression to postfix notation and use Thompson's algorithm.|
| q2.py      | Create a powerset for the given states in the NFA. For a given state in the DFA, find out the next state for a given letter by taking the union of ephsilon transfer of transitions in NFA for each element in the DFA state|
| q3.py      | Use the transitive closure method and eliminate states k-times (where k is the number of states in the DFA) using a modified Bellmann Ford Method|
| q4.py      | Use Hopcroft's algorithm after removing the unreachable states in the DFA|

Assumptions:

| Code        | Approach |
| ----------- | ----------- |
| q1.py       |None|
| q2.py      |None|
| q3.py      |Complex DFA's won't be provided. Regex need not be simplified.|
| q4.py      |None|

# Video

The video provides a walkthrough on how to execute the codes.
