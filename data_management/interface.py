"""provides the interface for data_management"""
import os
import sys


from AML/parameter import Parameter

class DatasetInterface():
    '''This interface defines the most important attributes and methods to load/get the raw dataset'''
    # DO NOT IMPLEMENT THIS
    # attributes
    m_parameter = clsParameter.getInstance()

    # methods
    def __init__(self):
        raise NotImplementedError

    def load_data(self):
        raise NotImplementedError

    def more_functions_tb_implemented(self):
        raise NotImplementedError
