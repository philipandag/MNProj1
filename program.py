#US dollar and one troy ounce of silver
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os
from functions import *


# Read in the data

data = read_data()
#inspect_data(data)
data = data.to_numpy()

values = data[:, 1]
times = data[:, 0]

def EMAn(data, start_index, N):
    end_index = start_index - N
    if(end_index < 0):
        end_index = 0

    if(start_index == end_index):
        return 0
        
    a = 2/(N+1)
    nominator = 0
    denominator = 0
    common = 1 # (1-a)^i

    for i in range(start_index, end_index, -1):
        nominator += data[i]*common
        denominator += common
        common *= (1-a)

    return nominator/denominator

def macd(data, index):
    return EMAn(data, index, 12) - EMAn(data, index, 26)


MACD = np.array([])

for i in range(0, len(values)):
    MACD = np.append(MACD, macd(values, i))
SIGNAL = np.array([])
for i in range(0, len(values)):
    SIGNAL = np.append(SIGNAL, EMAn(MACD, i, 9))

plt.plot(times, MACD)
plt.plot(times, SIGNAL)


for i in range(0, len(values)):
    if(MACD[i]-SIGNAL[i] < 0 and MACD[i-1]-SIGNAL[i-1] > 0):
        plt.plot(times[i], MACD[i], 'r.')
    elif(MACD[i]-SIGNAL[i] > 0 and MACD[i-1]-SIGNAL[i-1] < 0):
        plt.plot(times[i], MACD[i], 'g.')
plt.show()





