# Author: Jacob Hoffer
# Team: Team Ampere
# Data: 04/25/2021

import csv
import numpy as np
import scipy
from matplotlib import pyplot as plt
import matplotlib.dates as mdates
# from processing import *
import pandas as pd

FILE_NAME = '12MAR21.CSV'
SAMPLE_START = 0
SAMPLE_FINISH = -1

START_DATE = '3/12/2021 19:14:58'
END_DATE = '3/12/2021 19:15:00'


def main():

    df = initialization()

    temp = df.dropna(axis=1)

    print(temp)

    print(df.min(skipna=True))
    print(df.max(skipna=True))

    df = df.interpolate(method='linear', limit_direction='both')

    ax = df.plot(x_compat=True, grid=True)
    ax.xaxis.set_major_locator(mdates.MicrosecondLocator(interval=100000))
    plt.show()

    # values = df.values
    #
    # length = len(values.T[0])
    # ys = [scipy.fft.fft(value) for value in values.T]
    #
    # p2s = [np.abs(y) / length for y in ys]
    # p1s = [p2[0: length // 2 + 1] for p2 in p2s]
    # p1s[:][2: -2] = [2 * p1[2: -2] for p1 in p1s]
    #
    # f_s = 60
    # f = f_s * np.arange(0, (length / 2), 1) / length

    # plt.figure()
    # plt.title('Single-Sided Amplitude Spectrum of X(t)')
    # plt.xlabel('f (Hz)')
    # plt.ylabel('|P1(f)|')
    # [plt.plot(f, p1) for p1 in p1s]
    # plt.show()

    return


def initialization():

    data_matrix = read_file()

    time_ms = data_matrix[3][SAMPLE_START:SAMPLE_FINISH] * 1000 + data_matrix[4][SAMPLE_START:SAMPLE_FINISH]
    index = pd.to_datetime(arg=time_ms, unit='ms')
    index = index.round('ms')

    d = {'x-axis (nT)': data_matrix[0][SAMPLE_START:SAMPLE_FINISH],
         'y-axis (nT)': data_matrix[1][SAMPLE_START:SAMPLE_FINISH],
         'z-axis (nT)': data_matrix[2][SAMPLE_START:SAMPLE_FINISH]}

    df = pd.DataFrame(d, index=index)
    df = df[~df.index.duplicated()]

    df = df.loc[START_DATE: END_DATE]

    index = pd.date_range(start=START_DATE, end=END_DATE, freq='1ms')

    df = df.reindex(index=index)

    first_valid = df.apply(pd.Series.first_valid_index).min()
    last_valid = df.apply(pd.Series.last_valid_index).max()
    df = df[first_valid:last_valid]

    return df


def read_file():
    with open(FILE_NAME, mode='r', newline='') as csv_file:
        reader = csv.reader(csv_file, delimiter=',', quotechar='|')
        file = np.array([list(map(float, row)) for row in reader if 'x' not in row])

    return file.T


if __name__ == '__main__':
    main()
