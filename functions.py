import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import os
def read_data():
    column_names = ['Time', 'Open', 'High', 'Low', 'Close', 'Volume']
    path = os.path.join(os.getcwd(), 'XAG.csv')
    return pd.read_csv(path, names=column_names, parse_dates=True, sep='\t')\
        .drop(['Open', 'High', 'Low', 'Volume'], axis=1)

def inspect_data(dataset):
    print('Dataset shape:')
    print(dataset.shape)

    print('Statistics:')
    print(dataset.describe().transpose())

    #sns.pairplot(dataset['Time', 'Close'], diag_kind='kde')
    #plt.show()