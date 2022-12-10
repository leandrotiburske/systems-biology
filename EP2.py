import random
import numpy as np
import pandas as pd
import math
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

def truthtable (n):
  if n < 1:
    return [[]]
  subtable = truthtable(n-1)
  return [ row + [v] for row in subtable for v in [0,1] ]

def reg(line, gene):
    filt = line[line != 0]
    f = filt.isna().any()
    f[gene] = False
    filt = filt.loc[:, ~f]
    result = list(filt)
    return result


def calc_prob(line, state, after, alpha, beta, gene):
    filt = line[line != 0]
    f = filt.isna().any()
    f[gene] = False    
    filt = filt.loc[:, ~f]
    filt = filt.fillna(0)
    Hi = filt.dot(pd.DataFrame(state)).values[0][0]

    if Hi != 0:
        if after == 1:
            calc = math.e ** (beta * Hi) / (math.e ** (beta * Hi) + math.e ** (- beta * Hi) )
        elif after == 0 :
            calc = math.e ** (- beta * Hi) / (math.e ** (beta * Hi) + math.e ** (- beta * Hi) )
    elif Hi == 0:
        if True in (state[[gene]] == after).values:
            calc = 1 / (1 + math.e ** (- alpha))
        else:
            calc = 1 - (1 / (1 + math.e ** (- alpha)))

    return calc

filename = input("arquivo: ")
file = open(filename, "r")
file = file.read().splitlines()

alpha = float(file[0])
beta = float(file[1])
file = file[2:]
file = pd.read_csv(filename, skiprows=[0,1])

print("Conditional Probability Tables")

for gene in range(len(list(file))):
    row = file.loc[[gene]]
    name = list(file)[gene]
    regulators = reg(line = row, gene = name)
    tt = truthtable(len(regulators))
    tt = pd.DataFrame(tt, columns=regulators)
    for i in range(len(regulators)):
        regulators[i] = regulators[i] + "(t)"
    tt2 = truthtable(len(regulators))
    tt2 = pd.DataFrame(tt2, columns=regulators)
    column_name = "Prob" + name + "(t+1)=0"
    result0 = tt.apply(lambda x : calc_prob(line = row, state = x, after = 0, alpha = alpha, beta = beta, gene = name), axis=1)
    tt2[column_name] = result0.round(2)
    column_name = "Prob" + name + "(t+1)=1"
    result1 = tt.apply(lambda x : calc_prob(line = row, state = x, after = 1, alpha = alpha, beta = beta, gene = name), axis=1)
    tt2[column_name] = result1.round(2)
    print(tt2.to_string(index=False))

def calc_prob2(state, after, alpha, beta, gene, Hi):
    if Hi != 0:
        if after == 1:
            calc = math.e ** (beta * Hi) / (math.e ** (beta * Hi) + math.e ** (- beta * Hi) )
        elif after == 0 :
            calc = math.e ** (- beta * Hi) / (math.e ** (beta * Hi) + math.e ** (- beta * Hi) )
    else:
        if True in (state.loc[gene] == after).values:
            calc = 1 / (1 + math.e ** (- alpha))
        else:
            calc = 1 - (1 / (1 + math.e ** (- alpha)))
    return calc



def calc_prob_state(states, state, matrix):
    probabilities = []
    state = pd.DataFrame(state, index=list(matrix))
    for config in range(len(states)):
        prob = []
        for gene in range(len(list(matrix))):
            line = pd.DataFrame(matrix.iloc[gene]).T
            Hi = line.dot(pd.DataFrame(state)).values[0][0]
            if states[config][gene] == 0:
                prob.append(calc_prob2(state = state, after = 0, alpha = alpha, beta = beta, gene = list(matrix)[gene], Hi = Hi))
            if states[config][gene] == 1:
                prob.append(calc_prob2(state = state, after = 1, alpha = alpha, beta = beta, gene = list(matrix)[gene], Hi = Hi))
        prob = math.prod(prob)
        probabilities.append(prob)
    return probabilities


def transitions(states, matrix):
    table = pd.DataFrame([calc_prob_state(state = states[x], states = states, matrix = matrix) for x in range(len(states))])
    return table

# Create conditional table
trans_table = transitions(states = truthtable(len(list(file))), matrix = file)

random.seed(0)
def markov_walk(trans_table):
    state = random.choice(range(len(trans_table)))
    state_list = []
    i = 0
    while i != 20000:
        state = random.choices(list(range(len(trans_table))), weights=trans_table.loc[state].values.flatten().tolist())
        state_list.append(state[0])
        i += 1
    frequency = {}
    for item in state_list:
        if item in frequency:
            frequency[item] += 1
        else:
            frequency[item] = 1
    for k, v in frequency.items():
        frequency[k] = v / 20000
    frequency = dict(sorted(frequency.items()))
    freq = []
    for k, v in frequency.items():
        freq.append(frequency[k])
    return freq

print("")
print("Steady State Probability")

names = []
for item in truthtable(len(list(file))):
    state = ""
    for i in item:
        state = state + str(i)
    names.append(state)

pd.options.display.float_format = '{:.2f}'.format
print(pd.DataFrame(markov_walk(trans_table), index=names).to_string(header=False))