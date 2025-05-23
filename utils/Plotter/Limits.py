def find_max_less_than(data, threshold):
    max_val = data[0]
    i = 0
    for j, val in enumerate( data ):
        if val < threshold and val > max_val:
            max_val, i = val, j
    return i

class Limits:
    def __init__(self, xlimit : float = None, ylimit : float = None):
        self.xlimit = xlimit
        self.ylimit = ylimit

        self.xval = self.xlimit if not self.xlimit is None else 0
        self.yval = self.ylimit if not self.ylimit is None else 0
    
    def __call__( self, x, y ):
        if not self.xlimit is None and self.ylimit is None:
            i = find_max_less_than( x, self.xlimit )
            self.yval = max( max( y[:i] ), self.yval )
        elif self.xlimit is None and not self.ylimit is None:
            i = find_max_less_than( y, self.ylimit )
            self.xval = max( max( x[:i] ), self.xval )
        else:
            self.xval = max( max( x[:i] ), self.xval )
            self.yval = max( max( y[:i] ), self.yval )
    
    def eval( self ):
        return [ 0, self.xval ], [ 0, self.yval ]
    
    def x( self ):
        return self.eval()[0]

    def y( self ):
        return self.eval()[1]