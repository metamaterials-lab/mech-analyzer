import re
from utils.LaTeX import LaTeXPlotTemplate
from utils.LaTeX.LaTeXConverter import savefig
from utils.LaTeX.DownSampler import DownSampler

class LaTeXFigure:
    FIGURES = {}
    def __new__(cls, num : int | str = 0):
        if not num in cls.FIGURES.keys():
            cls.FIGURES[num] = super().__new__( cls )
        return cls.FIGURES[num]
        
    def __init__(self,num : int | str = 0):
        if not hasattr( self, "num" ):
            self.num = num
            self.params = { "PLOTS" : "" }
            self.data   = []
            self.colors = self.color_roulette( [ "blue", "red", "green", "black" ] )

    def color_roulette( self, colors : list[ str ] ):
        self.color = colors[0]
        while True:
            for color in colors:
                self.color = color
                yield color

    def __str__(self):
        if self.params["PLOTS"]:
            tex = str(LaTeXPlotTemplate)
            for label, val in self.params.items():
                if label == "PLOTS": continue
                tex = tex.replace( f"(<{label}>)", str(val) )

            for m in re.findall( r"(.*\(<[^>\)]+>\).*)", tex ):
                if "PLOTS" in m: continue
                tex = tex.replace( f"{m}\n", "" )

            tex = tex.replace( "(<PLOTS>)", self.params["PLOTS"] )
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
        self.data.append( "x,y\n" + "\n".join( DownSampler( ( x, y ) ) ) )
        self.params["PLOTS"] += """
        \\addplot[ color = {color} ]
        table[x=x,y=y,col sep=comma] {{data_csv}};
        """.replace( "{color}", color )\
           .replace( "{data_csv}", f"data_{len(self.data)-1}.csv" )
        
    def fill_between( self, x : list[float], y_p : list[float], y_m : list[float], color : str = None, alpha : float = 1.0 ):
        if len( x ) != len( y_p ) or len( x ) != len( y_m )  : raise Exception( "Arrays must have compatible sizes." )
        color = self.color if color is None else color
        self.data.append( "x,y_p,y_m\n" + "\n".join( DownSampler( ( x, y_p, y_m ) ) ) )
        self.params["PLOTS"] += """
        \\addplot[color={color}, opacity=0.0, name path=A{id}] table[x=x,y=y_p,col sep=comma] {{data_csv}};
        \\addplot[color={color}, opacity=0.0, name path=B{id}] table[x=x,y=y_m,col sep=comma] {{data_csv}};
        \\addplot[color={color}, fill opacity={alpha}] fill between[of=A{id} and B{id}];
        """.replace( "{color}", color )\
           .replace( "{data_csv}", f"data_{len(self.data)-1}.csv" )\
           .replace( "{id}", f"{len(self.data)-1}" )\
           .replace( "{alpha}", f"{alpha}" )
        
    def savefig( self, filename : str ):
        savefig( filename, str(self), self.data )

    def close( self, *args ):
        LaTeXFigure.FIGURES.clear()