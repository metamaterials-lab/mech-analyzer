from utils.Plotter.Limits import Limits
from statistics import mean, stdev
from utils.Plotter.Backend import plt
from utils.Analyzer.IterUtil import IterUtil

class PlotTemplates:
    @classmethod
    def Preamble( cls, create_new_figure : bool = False ):
        if create_new_figure: plt.figure()
    @classmethod
    def Postamble(
        cls,
        title : str = "Stress-strain curve",
        labels : list[ str ] = [r"Strain $(\varepsilon)$", r"Stress $(\sigma)$" ],
        limits : Limits = Limits()
    ):
        plt.title( title )
        plt.xlabel( labels[0] )
        plt.ylabel( labels[1] )
        if limits.x(): plt.xlim( limits.x() )
        if limits.y(): plt.ylim( limits.y() )
        


    @classmethod
    def SimplePlot(
        cls,
        title : str = "Stress-strain curve",
        labels : list[ str ] = [r"Strain $(\varepsilon)$", r"Stress $(\sigma)$" ],
        limits : Limits = Limits(),
    ):
        def plot(
                Strain : list[ list[ float ] ],
                Stress : list[ list[ float ] ]
        ):
            limits.__init__(limits.xlimit,limits.ylimit)
            for strain, stress in zip( Strain, Stress ):
                plt.plot( strain, stress )
                limits( strain, stress )
            PlotTemplates.Postamble( title, labels, limits )

        return plot
    
    @classmethod
    def MeanStdPlot(
        cls,
        title : str = "Stress-strain curve",
        labels : list[ str ] = [r"Strain $(\varepsilon)$", r"Stress $(\sigma)$" ],
        limits : Limits = Limits(),
    ):
        def plot(
                Strain : list[ list[ float ] ],
                Stress : list[ list[ float ] ]
        ):
            limits.__init__(limits.xlimit,limits.ylimit)
            
            strain_m = [ mean(r)  for r in IterUtil(Strain) ]
            stress_m = [ mean(r)  for r in IterUtil(Stress) ]
            stress_d = [ stdev(r) if len(r) > 1 else 0 for r in IterUtil(Stress) ]

            plt.plot( strain_m, stress_m )
            plt.fill_between(
                strain_m,
                [ m + d for m,d in zip( stress_m, stress_d ) ],
                [ m - d for m,d in zip( stress_m, stress_d ) ],
                alpha=0.5
            )
            limits( strain_m, stress_m )
            PlotTemplates.Postamble( title, labels, limits )

        return plot
    
