from utils.Processor.AbstractProcessor import AbstractProcessor

class Shimadzu( AbstractProcessor ):
    NUM  = 3
    SKIP = 3
    TOL  = 5.0

    def __init__(self, filename : str, filename_dimensions : str = "" ):
        super().__init__( filename, filename_dimensions )

    def init_recipient( pFile ):
        for _ in range( Shimadzu.SKIP ): l = pFile.readline()
        return [ { "data" : [], "min_d" : 0.0, "dim" : [] } for _ in range( len( l.split(",") ) // Shimadzu.NUM ) ]

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

    def read_results( self ):
        if isinstance( self.pFile, type( None ) ): raise Exception( "Error reading file." )
        for line in self.pFile.readlines():
            line = Shimadzu.format_line( line )
            for i in range( 0, len(line), Shimadzu.NUM ):
                time, force, disp = tuple( line[i:i+Shimadzu.NUM] )
                Shimadzu.read( i, self.data, time, force, disp )