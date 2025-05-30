from typing import Callable, Iterable
from utils.Processor.DataReader import DataReader
from utils.Plotter.Backend import plt

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
    
    def figure( self, num : int | str = None ):
        plt.figure( num )

    def show( self ):
        plt.show()
    
    def savefigs( self, path : str ):
        for num in plt.get_fignums():
            print( "COMPILING: " + path.format(num) )
            fig = plt.figure( num )
            fig.savefig( path.format( num ) )
