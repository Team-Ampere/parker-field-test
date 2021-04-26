# Author: Jacob Hoffer
# Team: Team Ampere
# Data: 04/25/2021

import csv
import numpy as np
from matplotlib import pyplot as plt
from processing import *

FILE_NAME = '12MAR21.CSV'
SAMPLE_START = 1500
SAMPLE_FINISH = 2000


def main():

    test = initialization()

    test.plot_samples()

    test.interpolate()

    plt.figure()
    [plt.plot(test.time_r, y(test.time_r)) for y in test.values_r]
    # [plt.plot(test.time, yp) for yp in test.values_r]
    plt.show()

    return


def initialization():

    data_matrix = read_file()

    unix_time_ref = data_matrix[0][3]
    millisecond_ref = data_matrix[0][4]

    time_ref = unix_time_ref * 1000 + millisecond_ref

    samples = [Sample(row[0:3], row[3]*1000 + row[4] - time_ref) for row in data_matrix]

    test = Test(samples[SAMPLE_START:SAMPLE_FINISH])

    return test


def read_file():
    with open(FILE_NAME, mode='r', newline='') as csv_file:
        reader = csv.reader(csv_file, delimiter=',', quotechar='|')
        file = [list(map(float, row)) for row in reader if 'x' not in row]

    return file


if __name__ == '__main__':
    main()
