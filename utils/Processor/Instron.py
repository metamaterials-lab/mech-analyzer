from utils.Processor.AbstractProcessor import AbstractProcessor

import re
import os

def find_sort( dirname : str ):
    key_match = lambda filename : tuple( map( int, re.findall( "(\d+)", filename ) ) )[-1]
    return sorted( next(os.walk( dirname ))[2], key=key_match )

class Instron( AbstractProcessor ):
    NUM  = 3
    SKIP = 2
    TOL  = 5.0
    PRELOAD = 0.0

    def __init__(self, dirname : str, filename_dimensions : str = "" ):
        super().__init__( dirname, filename_dimensions )

    @classmethod
    def init_recipient( cls, pFiles ):
        unit_map = []
        for pFile in pFiles:
            for _ in range( Instron.SKIP ): l = pFile.readline()
            force_units = re.findall( r"\(([^\)]+)\)", l )[-1]
            if force_units == "kN":
                unit_map.append( lambda f: 1000*f )
            else:
                unit_map.append( lambda f: f )
        return [ { "data" : [], "min_d" : 0.0, "dim" : [], "flag" : False } for _ in range( len( pFiles ) ) ], unit_map

    @classmethod
    def read( cls, i, data : list[dict], time, force, disp ):
        if force < Instron.TOL and not data[i]["flag"]:
            data[i]["data"]  = [  ]
            data[i]["min_d"] = disp
        else:
            data[i]["flag"] = True
            data[i]["data"].append( ( time, disp - data[i]["min_d"], force ) )

    def read_results( self ):
        for i, pFile in enumerate( self.pFiles ):
            for line in pFile.readlines():
                time, disp, force = tuple( Instron.format_line( line, float ) )
                Instron.read( i, self.data, time, self.unit_map[i]( force - Instron.PRELOAD ), disp )

    def __enter__( self ):
        self.pFiles = [ open( os.path.join( self.filename, file ), "r" ) for file in find_sort( self.filename ) ]
        self.data, self.unit_map  = self.__class__.init_recipient( self.pFiles )
        AbstractProcessor.read_dimensions( self.filename_dimensions, self.data )
        self.read_results()
        return self.data
    
    def __exit__( self, *_ ):
        for pFile in self.pFiles:
            pFile.close()
