import os

with open( os.path.join( os.path.dirname( os.path.abspath( __file__ ) ), "PlotTemplate.LaTeX" ), "r" ) as pFile:
    LaTeXPlotTemplate = pFile.read()