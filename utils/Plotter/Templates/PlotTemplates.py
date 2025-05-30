from utils.Plotter.Limits import Limits
from statistics import mean, stdev
from utils.Plotter.Backend import plt

class IterUtil:
    def __init__(self, var : list[list[float]]):
        self.var = var
    def __iter__(self):
        i = 0
        while True:
            res = []
            for v in self.var:
                if i < len(v): res.append( v[i] )
            i += 1
            if res: yield res
            else: break


class PlotTemplates:
    def Preamble( create_new_figure : bool = False ):
        if create_new_figure: plt.figure()
    def Postamble(
        title : str = "Stress-strain curve",
        labels : list[ str ] = [r"Strain $(\varepsilon)$", r"Stress $(\sigma)$" ],
        limits : Limits = Limits( [[],[]] )
    ):
        plt.title( title )
        plt.xlabel( labels[0] )
        plt.ylabel( labels[1] )
        if limits.x(): plt.xlim( limits.x() )
        if limits.y(): plt.ylim( limits.y() )
        


    def SimplePlot(
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
    
    def MeanStdPlot(
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
    
