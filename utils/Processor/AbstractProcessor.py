class AbstractProcessor:
    def __init__(self, filename : str, filename_dimensions : str = "" ):
        self.filename   = filename
        self.filename_dimensions = filename_dimensions
        self.pFile      = None
        self.data       = None

    def init_recipient( pFile ):
        return [ { "data" : [], "min_d" : 0.0, "dim" : [] } ]

    def format_line( line : str, map = lambda x : x ):
        return [ map( l.replace( "\"", "" ).replace("\n","") ) for l in line.split( "," ) ]
    
    def read_dimensions( filename : str, data : list[dict] ):
        with open( filename, "r" ) as pFile:
            for n, line in enumerate( pFile.readlines() ):
                data[n]["dim"] = tuple( AbstractProcessor.format_line( line, map=float ) )

    def __enter__( self ):
        self.pFile = open( self.filename, "r" )
        self.data  = self.__class__.init_recipient( self.pFile )
        AbstractProcessor.read_dimensions( self.filename_dimensions, self.data )
        self.read_results()
        return self.data
    
    def __exit__( self, *_ ):
        self.pFile.close()

    def read_results( self ):
        pass