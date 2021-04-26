# Author: Jacob Hoffer
# Team: Team Ampere
# Data: 04/25/2021

import csv
import numpy as np
import scipy
from matplotlib import pyplot as plt
# from processing import *
import pandas as pd

FILE_NAME = '12MAR21.CSV'
SAMPLE_START = 1500
SAMPLE_FINISH = 1600


def main():

    df = initialization()
    df = df.interpolate(method='linear')

    df.plot()
    plt.show()

    values = df.values

    signals = [scipy.fft.fft(value) for value in values.T]

    plt.figure()
    [plt.plot(df.index, np.abs(signal)) for signal in signals]
    plt.show()

    return


def initialization():

    data_matrix = read_file()

    unix_time_ref = data_matrix[3][0]
    millisecond_ref = data_matrix[4][0]

    time_ref = unix_time_ref * 1000 + millisecond_ref
    time_ms = data_matrix[3][SAMPLE_START:SAMPLE_FINISH] * 1000 + data_matrix[4][SAMPLE_START:SAMPLE_FINISH] - time_ref

    d = {'x-axis (nT)': data_matrix[0][SAMPLE_START:SAMPLE_FINISH],
         'y-axis (nT)': data_matrix[1][SAMPLE_START:SAMPLE_FINISH],
         'z-axis (nT)': data_matrix[2][SAMPLE_START:SAMPLE_FINISH]}

    df = pd.DataFrame(d, time_ms)
    df = df[~df.index.duplicated()]

    time_ms_uniform = np.arange(time_ms[0], time_ms[-1]+1, 1)

    df = df.reindex(index=time_ms_uniform)

    return df


def read_file():
    with open(FILE_NAME, mode='r', newline='') as csv_file:
        reader = csv.reader(csv_file, delimiter=',', quotechar='|')
        file = np.array([list(map(float, row)) for row in reader if 'x' not in row])

    return file.T


if __name__ == '__main__':
    main()
