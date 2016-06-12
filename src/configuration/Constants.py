__author__ = 'farshadfahimi'

import os


class Constants():
    def __init__(self):
        pass

    cwd = os.getcwd()

    #path to dataset
    dataset_path = cwd + os.sep + 'dataset' + os.sep
    #path to the output directory
    output_path = cwd + os.sep + 'output' + os.sep