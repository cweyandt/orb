# Default class for ORB models
from abc import ABCMeta, abstractmethod
import numpy as np
from matplotlib import pyplot as plt
import pandas as pd
import csv
import logging
import copy
import os


#%% Model Class
class _Model(utility._mpcpyPandas, utility._Measurements):
    '''Base class for representing a model for ORB.
    
    '''

    __metaclass__ = ABCMeta;

    @abstractmethod
    def parameter_estimate(self):
        '''Estimate parameters of the model using the measurement and 
        parameter_data dictionary attributes.
        Yields
        ------
        Updates the ``'Value'`` key for each estimated parameter in the 
        parameter_data attribute.
        '''

        pass;


    @abstractmethod
    def state_estimate(self):
        '''Estimate states of the model using measurements dictionary attributes.
        Yields
        ------
        Updates the ``'Value'`` key for each estimated state in the 
        state_data attribute.
        '''

        pass;
        
    @abstractmethod        
    def validate(self):
        '''Validate parameters of the model using the measurement and 
        parameter_data dictionary attributes.
        '''

        pass;

    @abstractmethod        
    def analyze(self):
        '''Estiamte the model using any given exodata inputs.
        Yields
        ------
        Updates the ``'Simulated'`` key for each measured variable in the 
        measurements dictionary attribute.
        '''

        pass;
