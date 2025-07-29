from typing import Self, Callable
import array
import itertools


#class Tensor:
#    def dim( l : list, d : list = [] ): 
#        if len(l):
#            if  isinstance( l[0], list ):
#                return Tensor.dim( l[0], d + [len(l)] )
#        return d + [ len( l ) ]
#    
#    def get( l : list, i : list[int] ):
#        if len(i) > 1:
#            return Tensor.get( l[i[0]], i[1:] )
#        return l[i[0]]
#    
#    def index( dim : list[int] ):
#        _sum_ = lambda a,b : lambda *i: a(*i) + b(*i)
#        def _sum( l : list ):
#            if len( l ) > 1:
#                return _sum_( l[0], _sum( l[1:] ) )
#            return l[0]
#        
#        def create_lambda( i, d ):
#            return lambda *index : d * index[i]
#        
#        coeff = [1]
#        for d in reversed( dim ):
#            coeff = [coeff[0]*d] + coeff
#
#        return _sum( [ create_lambda( i, c ) for i, c in enumerate( coeff[1:] ) ] )
#
#    def array( l : list, dim : list ):
#        return array.array( "d", [ Tensor.get( l, i ) for i in itertools.product( *[ range(d) for d in dim ] )] )
#
#    def __init__(self, X : list[ list[ float ] ]):
#        self.d = Tensor.dim( X )
#        self.X = Tensor.array( X, self.d )
#        self.i = Tensor.index( self.d )
#    
#    def __getitem__(self, i : tuple[int]):
#        return self.X[ self.i( *i ) ]
#
#    def __iter__(self):
#        for i in itertools.product( *[ range(d) for d in self.d ] ):
#            yield i, self[*i]
#
#    def __str__(self):
#        c = [ 0 for _ in range( len(self.d) - 1 ) ]
#        s = ""
#        for i, v in self:
#            for j, k in enumerate(c):
#                if i[j] != k:
#                    s += "\n"; c[j] = i[j]
#                
#            s += f"{v} "
#        return s

def checkDimDecorator( method : Callable ):
    def wrapper( A, B ):
        if A.d == B.d:
            return method( A, B )
        else:
            raise Exception( f"Incompatible dimenions A ({A.d}) and B ({B.d})" )
    return wrapper

def checkDimDecoratorVector( method : Callable ):
    def wrapper( A, B ):
        if A.d == B.d or A.d == (B.d[1], B.d[0]):
            return method( A, B )
        else:
            raise Exception( f"Incompatible dimenions A ({A.d}) and B ({B.d})" )
    return wrapper

def checkNumberDecorator( method : Callable ):
    def wrapper( A, B : float | int ):
        if isinstance( B, int ) or isinstance( B, float ):
            B = Matrix( B, A.d )
        return method( A, B )
    return wrapper

class AbstractMatrix:
    def __init__( self, X : array.array, dim : tuple[int,int] ):
        self.X = X
        self.d = dim
        self.i = lambda *i: self.d[1]*i[0] + i[1]        
    
    def __setitem__(self, indices : tuple[int] | tuple[slice], val : float | Self ):
        if isinstance( indices, tuple ):
            i,j = indices
            if isinstance( i, int ) and isinstance( j, int ):
                self.X[ self.i( i,j ) ] = val
            elif isinstance( i, int ) and isinstance( j, slice ):
                J = range( *j.indices( self.d[1] ) )
                for j, x in zip( J, val.X ):
                    self.X[ self.i( i,j ) ] = x
            elif isinstance( i, slice ) and isinstance( j, int ):
                I = range( *i.indices( self.d[0] ) )
                for i, x in zip( I, val.X ):
                    self.X[ self.i( i,j ) ] = x
            elif isinstance( i, slice ) and isinstance( j, slice ):
                I = range( *i.indices( self.d[0] ) )
                J = range( *j.indices( self.d[1] ) )
                for i, vi in zip( I, range( val.d[0] ) ):
                    for j, vj in zip( J, range( val.d[1] ) ):
                        self.X[ self.i( i,j ) ] = val[vi,vj]
                

    def __getitem__(self, indices : tuple[int] | tuple[slice] ):
        if isinstance( indices, tuple ):
            i,j = indices
            if isinstance( i, int ) and isinstance( j, int ):
                return self.X[ self.i( i,j ) ]
            elif isinstance( i, int ) and isinstance( j, slice ):
                J = range( *j.indices( self.d[1] ) )
                return AbstractMatrix( array.array( "d", [ self.X[ self.i( i,k ) ] for k in J ] ), ( 1, len(J) ) )
            elif isinstance( i, slice ) and isinstance( j, int ):
                I = range( *i.indices( self.d[0] ) )
                return AbstractMatrix( array.array( "d", [ self.X[ self.i( k,j ) ] for k in I ] ), ( len(I), 1 ) )
            elif isinstance( i, slice ) and isinstance( j, slice ):
                I = range( *i.indices( self.d[0] ) )
                J = range( *j.indices( self.d[1] ) )
                return AbstractMatrix( array.array( "d", [ self.X[ self.i( k,l ) ] for k in I for l in J ] ), ( len(I), len(J) ) )

    def __iter__(self):
        for i in range( self.d[0] ):
            for j in range( self.d[1] ):
                yield (i,j), self[i,j]

    def __str__(self):
        s = ""
        for i in range( self.d[0] ):
            s += " ".join( [ "{0:.2f}".format( self[i,j] ).rjust(8) for j in range( self.d[1] ) ] ) + "\n"
        return s
                
    @checkNumberDecorator
    @checkDimDecorator
    def __add__( A : Self, B : Self ):
        return AbstractMatrix( array.array( "d", [  a+b for a,b in zip( A.X, B.X ) ] ), A.d )
    
    @checkNumberDecorator
    @checkDimDecorator
    def __sub__( A : Self, B : Self ):
        return AbstractMatrix( array.array( "d", [  a-b for a,b in zip( A.X, B.X ) ] ), A.d )
    
    def __neg__( A : Self ):
        return AbstractMatrix( array.array( "d", [  -a for a in A.X ] ), A.d )
    
    @checkNumberDecorator
    @checkDimDecorator
    def __mul__( A : Self, B : Self ):
        return AbstractMatrix( array.array( "d", [  a*b for a,b in zip( A.X, B.X ) ] ), A.d )
    
    def __radd__( A : Self, B : Self ):
        return B + A
    
    def __rmul__( A : Self, B : Self ):
        return B * A
    
    @checkDimDecoratorVector
    def __pow__( A : Self, B : Self ):
        return sum( [ a*b for a,b in zip( A.X, B.X ) ] )

    def __matmul__( A : Self, B : Self ):
        if A.d[1] == B.d[0]:
            index = lambda i,j: B.d[1]*i + j
            X = array.array( "d", [ 0 for _ in range( A.d[0] * B.d[1] ) ] )
            for i in range( A.d[0] ):
                a = A[i,:]
                for j in range( B.d[1] ):
                    X[index(i,j)] = a ** B[:,j]
            return AbstractMatrix( X, ( A.d[0], B.d[1] ) )
        else:
            raise Exception( f"Incompatible matrix dimensions A{A.d}, B{B.d}" )
    
    def T( A : Self ):
        return AbstractMatrix( array.array( "d", [ A[i,j] for j in range( A.d[1] ) for i in range( A.d[0] ) ] ), (A.d[1], A.d[0]) )


#class ConstantMatrix( AbstractMatrix ):
#    def __init__(self, val, dim):
#        X = array.array( "d", [ val for _ in range( dim[0] ) for _ in range( dim[1] ) ] )
#        super().__init__(X, dim)

class Matrix( AbstractMatrix ):
    def __init__(self,
                 X : list[ list[ float ] ] | list[ float ] | float | array.array,
                 dim : tuple[int] = None ):
        
        if isinstance( X, list ) and len( X ) :
            if isinstance( X[0], list ) and len( X[0] ):
                d = ( len(X), len(X[0]) )
                X = array.array( "d", [ X[i][j] for i in range( d[0] ) for j in range( d[1] ) ] )
            else:
                d = ( len(X), 1 )
                X = array.array( "d", X )
        elif isinstance( X, float ):
            if isinstance( dim, tuple ) and len( dim ) == 2:
                d = dim
                X = array.array( "d", [ X for _ in range( dim[0] ) for _ in range( dim[1] ) ] )

        
        super().__init__( X, d )

class Vector( AbstractMatrix ):
    def __init__(self, X : list[float] | float | array.array, dim : int = None ):
        if isinstance( X, list ) and len( X ):
            X = array.array( "d", X )
            d = (len(X), 1)
        elif isinstance( X, float ) and isinstance( dim, int ):
            X = array.array( "d", [ X for _ in range( dim ) ] )
            d = (dim, 1)

        super().__init__( X, d )
    
    def __setitem__(self, i : int | slice, val : float | Self ):
        if isinstance( i, tuple ): i,_ = i
        super().__setitem__( (i,0), val )
                
    def __getitem__(self, i : int | slice ):
        if isinstance( i, tuple ): i,_ = i
        return super().__getitem__( (i,0) )

    #def __str__(self):
    #    return "\n".join( [ "{0:.2f}".format( self[i] ).rjust(8) for i in range( self.d[0] ) ] ) + "\n"


def LUFactorization( A : Matrix ):

    if A.d[0] == A.d[1]: n = A.d[0]
    else: raise Exception( f"Matrix A is not square {A.d}" )

    L = Matrix( 0.0, A.d )
    U = Matrix( 0.0, A.d )

    for i in range(n):
        for j in range(i, n):
            U[i,j] = A[i,j] - L[i,:i] ** U[:i,j]

        for j in range(i, n):
            if (i == j): L[i,i] = 1.0
            else: L[j,i] = (A[j,i] - L[j,:i] ** U[:i,i]) / U[i,i]
    return L, U

def Lsolve(L : Matrix, b : Vector):
    n,_ = L.d
    x   = Vector( 0.0, n )
    for i in range(n):
        x[i] = b[i] - L[i,:i] ** x[:i]
    return x

def Usolve(U : Matrix, b : Vector):
    n,_ = U.d
    x   = Vector( 0.0, n )
    for i in reversed(range(n)):
        x[i] = ( b[i] - ( U[i,i+1:n] ** x[i+1:n] ) ) / U[i,i]
    return x

def LUsolve( A : Matrix, b : Vector ):
    L,U = LUFactorization( A )
    y = Lsolve( L, b )
    x = Usolve( U, y )
    return x

mat = [[2, -1, -2],
       [-4, 6, 3],
       [-4, -2, 8]]
A = Matrix( mat )
b = Vector( [1,2,3] )

x = LUsolve( A, b )



