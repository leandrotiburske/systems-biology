'''
Faça um programa que tenha como entrada os parâmetros :
* Rede inicial do sistema
* Estado inicial da rede selecionada
* Número de passos
* Probabilidade de mudança de contexto
* Probabilidade de seleção para cada rede do sistema.

E retorne:
* As frequências relativas para cada possível estado no final dos passos

Exemplo de execução:

ini_net: R4
ini_state: 110
steps: 20000
p_change: 0.9, 0.1
Prob: 50,10,10,10,20
Long-Run Relative Frequencies:
000 0.524
001 0.211
010 0.057
011 0.062
100 0.010
101 0.048
110 0.042
111 0.046
'''

#seu código aqui
import random
import numpy as np
import pandas as pd
import math
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

R1 = {"000":"000",
"001":"000",
"010":"101",
"011":"001",
"100":"010",
"101":"010",
"110":"111",
"111":"011"}

R2 = {"000":"000",
"001":"110",
"010":"000",
"011":"010",
"100":"001",
"101":"111",
"110":"001",
"111":"011"}

R3 = {"000":"001",
"001":"011",
"010":"001",
"011":"111",
"100":"000",
"101":"010",
"110":"000",
"111":"110"}

R4 = {"000":"010",
"001":"010",
"010":"011",
"011":"111",
"100":"000",
"101":"000",
"110":"001",
"111":"101"}

R5 = {"000":"001",
"001":"001",
"010":"000",
"011":"100",
"100":"011",
"101":"011",
"110":"010",
"111":"110"}

random.seed(0)

ini_net = str(input("ini_net: "))
ini_net = ini_net.lstrip(" ").rstrip(" ")
ini_state = input("ini_state: ")
ini_state = ini_state.lstrip(" ")
steps = int(input("steps: "))
p_change = input("p_change: ")
p_change = p_change.split(",")
p_change = [float(x) for x in p_change]
prob = input("Prob: ")
prob = prob.split(",")
prob = [int(x) for x in prob]

if ini_net == "R1":
    net = R1
elif ini_net == "R2":
    net = R2
elif ini_net == "R3":
    net = R3
elif ini_net == "R4":
    net = R4
elif ini_net == "R5":
    net = R5


def truthtable (n):
  if n < 1:
    return [[]]
  subtable = truthtable(n-1)
  return [ row + [v] for row in subtable for v in [0,1] ]

def change_states(matrix, state):
    next_state = ""
    for k,v in matrix.items():
        if state == k:
            next_state = v
    return next_state


def markov_walk(init_state, net, p_change, steps, Prob, R1, R2, R3, R4, R5):
    state = init_state
    state_list = []
    i = 0
    while i != steps:
        context = random.choices(['Same', 'Change'], weights= p_change, k=1)
        if context == ['Same']:
            state = change_states(matrix=net, state=state)
            state_list.append(state)
        elif context == ['Change']:
            net = random.choices(["R1", "R2", "R3", "R4", "R5"], weights=Prob, k=1)
            if net == ['R1']:
                net = R1
            elif net == ['R2']:
                net = R2
            elif net == ['R3']:
                net = R3
            elif net == ['R4']:
                net = R4
            elif net == ['R5']:
                net = R5
            state = change_states(matrix=net, state=state)
            state_list.append(state)
        i += 1
 
    frequency = {}
    for item in state_list:
        if item in frequency:
            frequency[item] += 1
        else:
            frequency[item] = 1
    for k, v in frequency.items():
        frequency[k] = v / steps
    frequency = dict(sorted(frequency.items()))
    freq = []
    for k, v in frequency.items():
        freq.append(frequency[k])
    return freq

print("Long-Run Relative Frequencies:")

names = []
for item in truthtable(3):
    state = ""
    for i in item:
        state = state + str(i)
    names.append(state)

pd.options.display.float_format = '{:.3f}'.format
print(pd.DataFrame(markov_walk(init_state=ini_state, net=net, p_change=p_change, 
steps=steps, Prob=prob, R1=R1, R2=R2, R3=R3, R4=R4, R5=R5), index=names).to_string(header=False))
