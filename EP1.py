from statistics import mean
import numpy as np
import pandas as pd
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

filename = input("Nome do arquivo: ")
rede = input("Tipo de rede: ")
variante = input("Variante TOM (min ou mean): ")
index1 = int(input("Index do primeiro gene: "))
index2 = int(input("Index do segundo gene: "))

file = pd.read_csv(filename, index_col=0)
file = file.to_numpy(dtype="float")
diag = np.diag(file)
np.fill_diagonal(file, 0)

# Computar TOM: O cálculo da TOM precisa do correto cálculo no denominado e no numerador. Analise a fórmula da TOM comentada na aula.

# No numerador calculamos a multiplicação das adjacências para todo gene "i" e "j" com um gene vizinho "u". Se calcularmos para a matriz de adjacência completa, o cálculo fica representado por um "dot product".
L = np.dot(file[index1], file[index2])

# No denominador temos a conetividade para cada gene do par "i" e "j". A conetividade é a soma da adjacência do gene com todos os outros da matriz. Dado que a matriz é simétrica, vamos consider um gene das filas e o outro das colunas.
ki = np.sum(file[index1])
kj = np.sum(file[index2])
np.fill_diagonal(file, diag)

if variante == "min":  # cálculo do denominador quando a variante da TOM seleciona a mínima conetividade.
  den = min(ki, kj) + 1 - abs(file[index1, index2])
elif variante == "mean":
  ks = [ki, kj]
  den = mean(ks) + 1 - abs(file[index1, index2])
  
if rede == "unsigned":  # unsigned TOM, como descrito na fórmula
  tom = (L + abs(file[index1, index2])) / den
elif rede == "signed": # signed TOM, onde o numerador e a matriz de adjacência do denominador são transformados em valores positivos.
  tom = (abs(L + file[index1, index2])) / den

if index1 == index2:
  tom = 1
print(np.around(tom, decimals=4))