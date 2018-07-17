from __future__ import print_function

import sys, os, time, re, copy
import json
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


class UsersDB(object):


    def __init__(self, dataPath):
        self._dataPath = dataPath
        self._db = self._load(self._dataPath)


    def loadAll(self):
        """
        Load info of all users contained in data path.
        @param dataPath: Path to data folder which has structure dataPath/usr/info.json
        @return pandas DataFrame.
        """

        infos = [os.path.join(dataPath, usr, 'info.json') for usr in os.listdir(dataPath)]
        d = []

        for info in infos:
            with open(info, 'r') as f:
                d.append(json.load(f))

        d = pd.DataFrame(d)

        return d


    def hist(self, var, groupby = None, nbins = 20, varUnits = ''):
        """
        Generate histogram for a given (numerical) variable.
        @param var: Variable to plot.
        @param groupby: Variable to group by.
        @param nbins: Number of bins.
        @param varUnits: Variable units, e.g. km.
        @return Matplotlib figure and axis object.
        """

        if groupby is None:
            data = self._db.loc[:, var]
        else:
            # TODO add groupby feature
            data = self._db.loc[:, var]

        fig, ax = plt.subplots()
        plt.sca(ax)
        
        plt.hist(data, nbins = nbins)
        plt.xlabel(var + '[{}]'.format(varUnits))
        plt.ylabel('Tinder users')
        plt.tight_layout()

        return fig, ax

    # TODO
    # Boxplots
    # Automatic outlier detection/removal
    # Something something NPL with bios
