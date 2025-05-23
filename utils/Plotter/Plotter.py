from typing import Callable, Iterable
from matplotlib import pyplot as plt
from utils.Processor.DataReader import DataReader

class Plotter:
    ENGINEER = "engineer"
    REAL = "real"

    def __init__(self, results : DataReader ):
        self.results = results

    def plot(
        self,
        data_type : str,
        template : Callable,
        data_range : Iterable[ int ]
    ):
        if not data_type in [ Plotter.ENGINEER, Plotter.REAL ]: raise Exception( f"Incorrect data type ({data_type})" )
        
        Strain = []
        Stress = []
        self.results.setStensil( list( data_range ) )
        for data in self.results:
            Strain.append( data[data_type]["strain"] )
            Stress.append( data[data_type]["stress"] )
        
        template( Strain, Stress )
    
    def show( self ):
        plt.show()
