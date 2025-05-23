import re
from utils.LaTeX import LaTeXPlotTemplate

class LaTeXFigure:
    FIGURES = {}
    def __new__(cls, num : int = 0):
        if not num in LaTeXFigure.FIGURES.keys():
            LaTeXFigure.FIGURES[num] = super().__new__( cls )
        return LaTeXFigure.FIGURES[num]
        
    def __init__(self,num : int = 0):
        self.num = num
        self.params = { "PLOTS" : "" }
        self.colors = self.color_roulette( [ "blue", "red", "green", "black" ] )

    def color_roulette( self, colors : list[ str ] ):
        while True:
            for color in colors:
                yield color

    def __str__(self):
        if self.params["PLOTS"]:
            tex = str(LaTeXPlotTemplate)
            for label, val in self.params.items():
                tex = tex.replace( f"(<{label}>)", str(val) )

            for m in re.findall( r"(.*\(<[^>\)]+>\).*)", tex ):
                tex = tex.replace( f"{m}\n", "" )
            return tex
        else:
            return ""
    
    def __repr__(self):
        return f"LaTeXFigure(num:{self.num})"
    
    def title( self, title : str = "" ):
        self.params["title"] = title

    def xlabel( self, label : str = "" ):
        self.params["xlabel"] = label

    def ylabel( self, label : str = "" ):
        self.params["ylabel"] = label

    def xlim( self, limits : list[float,float] ):
        self.params["xmin"] = limits[0]
        self.params["xmax"] = limits[1]
    
    def ylim( self, limits : list[float,float] ):
        self.params["ymin"] = limits[0]
        self.params["ymax"] = limits[1]

    def plot( self, x : list[ float ], y : list[ float ], color : str = None ):
        if len( x ) != len( y ): raise Exception( "Arrays must have compatible sizes." )
        color = next( self.colors ) if color is None else color
        data  = "".join( [ str(t) for t in zip( x,y ) ] )
        self.params["PLOTS"] += """
        \\addplot[ color = {color} ]
        coordinates {
        {data}
        };
        """.replace( "{color}", color )\
           .replace( "{data}",  data )