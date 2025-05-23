from utils.LaTeX.LaTeXPlot import LaTeXPlot

plt = LaTeXPlot()
plt.fig()
plt.fig()

plt.plot( [1,2,3,4],[1,2,3,4] )
plt.plot( [1,2,3,4],[-1,-2,-3,-4] )
plt.title( "Title" )
plt.xlabel( "$x$ axis" )

print( plt.figure )