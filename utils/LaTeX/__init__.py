import os

with open( os.path.join( os.path.dirname( os.path.abspath( __file__ ) ), "PlotTemplate.tex" ), "r" ) as pFile:
    LaTeXPlotTemplate = pFile.read()