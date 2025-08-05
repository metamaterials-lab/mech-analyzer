from utils.Processor.ExperimentTypes import ExperimentTypes

import os
import re

class DataReader:
    def __init__(self, dirname : str, mode : int = ExperimentTypes.TENSILE ):
        self.dirname = dirname
        key_match = lambda filename : tuple( map( int, re.findall( r"(\d+)", filename ) ) )[-1]
        self.files = [ filename for filename in sorted( next(os.walk( dirname ))[2], key=key_match ) ]
        self.mode = mode

    @classmethod
    def format_line( cls, line : str, map = lambda x : x ):
        return [ map( l.replace( "\"", "" ) ) for l in line.split( "," ) ]

    @classmethod
    def init_recipient( cls, mode : int = ExperimentTypes.TENSILE ):
        return ExperimentTypes.get_recipient( mode )
    
    @classmethod
    def read_results( cls, pFile, data, mode : int = ExperimentTypes.TENSILE ):
        for line in pFile.readlines():
            datum = tuple( DataReader.format_line( line, float ) )
            ExperimentTypes.read_results( data, datum, mode )

    def setStensil( self, stensil : list[int] ):
        self.stensil = stensil

    def __enter__( self ):
        self.pFiles = [ open( os.path.join( self.dirname, file ), "r" ) for file in self.files ]
        return self

    def __iter__( self ):
        for i, pFile in enumerate( self.pFiles ):
            if i in self.stensil:
                pFile.seek(0)
                data = DataReader.init_recipient()
                DataReader.read_results( pFile, data, self.mode )
                yield data

    def __exit__( self, *_ ):
        for pFile in self.pFiles:
            pFile.close()
            
        
