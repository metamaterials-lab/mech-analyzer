from utils.LaTeX.LaTeXPlot import LaTeXPlot

plt = LaTeXPlot()
plt.figure()
plt.figure()

plt.plot( [1,2,3,4],[1,2,3,4] )
plt.plot( [1,2,3,4],[-1,-2,-3,-4] )
plt.title( "Title" )
plt.xlabel( "$x$ axis" )

for n in plt.get_fignums():
    fig = plt.figure( n )
    fig.savefig( "./temp/test.svg" )
    fig.savefig( "./temp/test.pdf" )
    fig.savefig( "./temp/test.tex" )
    fig.savefig( "./temp/test.png" )
    fig.savefig( "./temp/test.jpeg" )
    fig.savefig( "./temp/test.eps" )
