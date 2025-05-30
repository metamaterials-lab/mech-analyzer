class Acum:
    def __init__(self, x : list[float], N : int):
        self.x = x
        self.N = N
        self.acum = 0

    def __call__(self, i):
        return self.x[i]

    def __iter__( self ):
        for i in range( len( self.x ) ):
            if not i % self.N:
                yield self(i)

class DownSampler:
    def __init__(self, z : tuple[ list[float], ... ], N : int = 500 ):
        self.z = tuple( [ Acum(c, N) for c in z ] )

    def __iter__(self):
        f = lambda x: "{:0.6f}".format( x )
        for z in zip( *self.z ):
            yield ",".join( [ f(c) for c in z ] )