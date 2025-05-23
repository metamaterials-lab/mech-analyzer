from utils.LaTeX import LaTeXFigure

class LaTeXPlot:
    def __init__(self):
        self.figure = LaTeXFigure()

    def fig(self, num : int = None):
        if num is None:
            self.figure = LaTeXFigure( max( LaTeXFigure.FIGURES.keys() ) + 1 )
        else:
            self.figure = LaTeXFigure( num )
    
    def title( self, title : str = "" ):
        self.figure.title( title )

    def xlabel( self, label : str = "" ):
        self.figure.xlabel( label )

    def ylabel( self, label : str = "" ):
        self.figure.ylabel( label )

    def xlim( self, limits : list[float,float] ):
        self.figure.xlim( limits )

    def ylim( self, limits : list[float,float] ):
        self.figure.ylim( limits )

    def plot( self, x : list[ float ], y : list[ float ], color : str = None ):
        self.figure.plot( x,y,color )