# Author: Jacob Hoffer

from matplotlib import pyplot as plt
from scipy import interpolate
import numpy as np
import pandas as pd


class Sample:

    def __init__(self, values, time):
        self.values = np.array(values)
        self.time = time


class Test:

    def __init__(self, samples):
        self.values = np.array([sample.values for sample in samples])
        self.time = np.array([sample.time for sample in samples])
        self.values_r = []
        self.time_r = []

    def interpolate(self):

        self.values_r = [interpolate.interp1d(self.time, y, kind='cubic') for y in self.values.T]
        self.time_r = np.arange(self.time[0], self.time[-1], 10)

        # yps = [pd.Series(y) for y in self.values.T]
        # yps = [yp.interpolate(limit_direction='both', kind='cubic') for yp in yps]

        # self.values_r = yps

        return

    def plot_samples(self):

        plt.figure()

        plt.title('Parker Field Test Samples')
        plt.xlabel('Time (s)')
        plt.ylabel('Magnetic Field (nT)')

        [plt.plot((self.time / 1000), x) for x in self.values.T]
        plt.show()

        return
