from math import pi, log
import os
import shutil

class Shimadzu:
    NUM  = 3
    SKIP = 3
    TOL  = 5.0

    def __init__(self, filename : str, filename_dimensions : str = "" ):
        self.filename   = filename
        self.filename_dimensions = filename_dimensions
        self.pFile      = None
        self.data       = None

    def read( i, data : list[dict], time, force, disp ):
        if time:
            time  = float(time)
            force = float(force)
            disp  = float(disp)
            n = i//Shimadzu.NUM
            if force < Shimadzu.TOL:
                data[n]["data"]  = [  ]
                data[n]["min_d"] = disp
            else:
                data[n]["data"].append( ( time, disp - data[n]["min_d"], force ) )

    def init_recipient( pFile ):
        for _ in range( Shimadzu.SKIP ): l = pFile.readline()
        return [ { "data" : [], "min_d" : 0.0, "dim" : [] } for _ in range( len( l.split(",") ) // Shimadzu.NUM ) ]

    def format_line( line : str, map = lambda x : x ):
        return [ map( l.replace( "\"", "" ) ) for l in line.split( "," ) ]
    
    def read_dimensions( filename : str, data : list[dict] ):
        with open( filename, "r" ) as pFile:
            for n, line in enumerate( pFile.readlines() ):
                data[n]["dim"] = tuple( Shimadzu.format_line( line, map=float ) )

    def __enter__( self ):
        self.pFile = open( self.filename, "r" )
        self.data  = Shimadzu.init_recipient( self.pFile )
        Shimadzu.read_dimensions( self.filename_dimensions, self.data )
        self.read_results()
        return self.data
    
    def __exit__( self, *_ ):
        self.pFile.close()

    def read_results( self ):
        if isinstance( self.pFile, type( None ) ): raise Exception( "Error reading file." )
        for line in self.pFile.readlines():
            line = Shimadzu.format_line( line )
            for i in range( 0, len(line), Shimadzu.NUM ):
                time, force, disp = tuple( line[i:i+Shimadzu.NUM] )
                Shimadzu.read( i, self.data, time, force, disp )

class CS_SHAPES:
    SQUARE = 1
    CIRCLE = 2

    square_area = lambda base: base**2
    circle_area = lambda diameter: pi * ( diameter / 2.0 )**2

    def Area( shape : int, *dimensions ):
        if shape == CS_SHAPES.SQUARE:
            return CS_SHAPES.square_area( *dimensions[:-1] ), dimensions[-1]
        elif shape == CS_SHAPES.CIRCLE:
            return CS_SHAPES.circle_area( *dimensions[:-1] ), dimensions[-1]

def parse_data( data : list[dict], filename : str, cross_section_shape : int ):

    dirname = os.path.dirname( filename )
    shutil.rmtree( dirname, True )
    os.makedirs( dirname )

    for i, entry in enumerate( data ):
        with open( filename.format( i + 1 ), "w" ) as pFile:
            area, height = CS_SHAPES.Area( cross_section_shape, *entry["dim"] )
            for time, disp, force in entry["data"]:
                eng_strain = disp / height
                eng_stress = force / area
                real_stress = eng_stress * ( 1 + eng_strain )
                real_strain = log( 1 + eng_strain )
                print( f"{eng_strain},{eng_stress},{real_strain},{real_stress}", file=pFile )        