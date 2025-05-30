from utils.LaTeX.LaTeXFigure import LaTeXFigure

class LaTeXPlot:
    def __init__(self):
        self.fig = LaTeXFigure()

    def figure(self, num : int | str = None):
        if num is None:
            self.fig = LaTeXFigure( max( [ key if isinstance( key, int ) else 0 for key in LaTeXFigure.FIGURES.keys() ] ) + 1 )
        else:
            self.fig = LaTeXFigure( num )
        return self.fig
    
    def title( self, title : str = "" ):
        self.fig.title( title )

    def xlabel( self, label : str = "" ):
        self.fig.xlabel( label )

    def ylabel( self, label : str = "" ):
        self.fig.ylabel( label )

    def xlim( self, limits : list[float,float] ):
        self.fig.xlim( limits )

    def ylim( self, limits : list[float,float] ):
        self.fig.ylim( limits )

    def plot( self, x : list[ float ], y : list[ float ], color : str = None ):
        self.fig.plot( x,y,color )

    def fill_between( self, x : list[float], y_p : list[float], y_m : list[float], color : str = None, alpha : float = 1.0 ):
        self.fig.fill_between( x,y_p,y_m,color,alpha )

    def get_fignums( self ):
        for n in LaTeXFigure.FIGURES.keys():
            yield n

    def show( self ):
        print( "Not implemented yet. :P" )