import os
import re

class DataReader:
    def __init__(self, dirname : str):
        self.dirname = dirname
        key_match = lambda filename : tuple( map( int, re.findall( "(\d+)", filename ) ) )[-1]
        self.files = [ filename for filename in sorted( next(os.walk( dirname ))[2], key=key_match ) ]
        self.pFiles = None
        self.data   = None

    def format_line( line : str, map = lambda x : x ):
        return [ map( l.replace( "\"", "" ) ) for l in line.split( "," ) ]

    def init_recipient( ):
        return {
            "engineer" : {
                "strain"  : [],
                "stress"  : []
            },
            "real" : {
                "strain" : [],
                "stress" : []
            }
        }
    
    def read_results( pFile, data : dict[str,dict[str,list]]  ):
        for line in pFile.readlines():
            es, eS, rs, rS = tuple( DataReader.format_line( line, float ) )
            data["engineer"]["strain"].append( es )
            data["engineer"]["stress"].append( eS )
            data["real"]["strain"].append( rs )
            data["real"]["stress"].append( rS )

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
                DataReader.read_results( pFile, data )    
                yield data

    def __exit__( self, *_ ):
        for pFile in self.pFiles:
            pFile.close()
            
        