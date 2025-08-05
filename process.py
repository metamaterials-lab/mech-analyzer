from utils.Processor import parse_data
from utils.Processor.Shimadzu import Shimadzu
from utils.Processor.Instron import Instron


from utils.Processor.DataReader import DataReader
from utils.Plotter.Plotter import Plotter
from utils.Plotter.Limits import Limits
from utils.Plotter.Templates.PlotTemplates import PlotTemplates

template = PlotTemplates.SimplePlot(
    limits = Limits( xlimit=0.2,ylimit=None )
)

template = PlotTemplates.MeanStdPlot(
    limits = Limits( xlimit=0.3,ylimit=None )
)

with DataReader( "./results/cured/Shimadzu" ) as data:
    plt = Plotter( data )

    plt.figure( "0deg" )
    plt.plot( Plotter.ENGINEER, template, [ 0,1,2,3,4 ] )
    #plt.figure( "45deg" )
    plt.plot( Plotter.ENGINEER, template, [ 5,6,7,8,9 ] )
    #plt.figure( "90deg" )
    plt.plot( Plotter.ENGINEER, template, [ 10,11,12,13,14 ] )
    plt.show()

    plt.savefigs( "./temp/fig_{0}.png" )

#with Shimadzu( "./results/raw/Shimadzu/muestra_15-1.csv", "./dimensions.csv" ) as data:
#    parse_data( data, "./results/cured/Shimadzu/result_probe_{}.csv", CS_SHAPES.CIRCLE )

#with Instron( "./results/raw/Instron/", "./dimensions_I.csv" ) as data:
#    parse_data( data, "./results/cured/Instron/results_probe_{}.csv", CS_SHAPES.SQUARE )


        
