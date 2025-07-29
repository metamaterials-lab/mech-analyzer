from typing import Iterable
from statistics import mean, stdev

from utils.Analyzer.IterUtil import IterUtil
from utils.Plotter.Plotter import Plotter
from utils.Processor.DataReader import DataReader

class Analyzer:
    def __init__(self, results : DataReader):
        self.results = results

    def analyze(
        self,
        data_type : str,
        data_range : Iterable[ int ],
        stress_range : tuple[ float, float]
    ):
        if not data_type in [ Plotter.ENGINEER, Plotter.REAL ]: raise Exception( f"Incorrect data type ({data_type})" )
        Strain = []
        Stress = []
        self.results.setStensil( list( data_range ) )
        for data in self.results:
            Strain.append( data[data_type]["strain"] )
            Stress.append( data[data_type]["stress"] )
        self( Strain, Stress, *stress_range )

    def __call__(self, Strain, Stress, MIN, MAX):
        data = []
        for i in range( len(Stress) ):
            print( f"Result {i + 1}:" )
            data.append( Analyzer.crop( Strain[i], Stress[i], MIN, MAX ) )

        strain_m = [ mean(r)  for r in IterUtil(Strain) ]
        stress_m = [ mean(r)  for r in IterUtil(Stress) ]

        print( f"Result Mean:" )
        Analyzer.crop( strain_m, stress_m, MIN, MAX )
        print( "Std. Dev: ", stdev( data ), "MPa" )

    def crop( strain, stress, MIN, MAX ):
        data = []
        for e, s in zip( strain, stress ):
            if s > MIN:
                data.append( (e,s) )
            if s > MAX: break
        
        x0, y0 = data[0]
        xf, yf = data[-1]
        E = (yf - y0) / (xf - x0)
        #print( "X_0: ", data[0], "X_f: ", data[-1] )
        print( f"Modulus: {E:.2f} MPa" )
        return E