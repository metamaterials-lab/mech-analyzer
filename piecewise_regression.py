import numpy as np
import matplotlib.pyplot as plt



TOL = 1e-5

def segmented_regression(
        x : np.ndarray,
        y : np.ndarray,
        psi0 : list[ float ]
    ):
    psi = np.array( psi0, dtype=np.float64 )
    N = len( psi )
    for i in range(100):

        X_ = [ np.ones_like( x ), x ]

        for p in psi:
            u = np.maximum(0, x - p)
            v = (x > p).astype(float)
            X_ += [ u, -v ]
        
        X = np.column_stack( X_ )
        c = np.linalg.lstsq( X, y )[0]

        psi0 = np.array( [ p + ( c[ 2*i+3 ] / c[ 2*i+2 ] ) if abs( c[2*i+2] ) > TOL*1e-3 else 0 for i, p in enumerate( psi ) ] )

        if all( [ abs( p0 - p ) < TOL for p0, p in zip( psi0, psi ) ] ): break
        
        psi = psi0

    beta = [ c[0], c[1] ]
    for j in range( N ):
        beta.append( c[2*j+2] )

    return psi, i+1, np.array( beta )


x = np.linspace(0, 10, 100)
y = np.piecewise(x, [
        x <= 2,
        (x > 2) * (x <=4),
        x > 4],
        [
        lambda x: 2 * x + 3,
        lambda x: -1.5 * x + 10,
        lambda x: 2*x - 3])
y += np.random.normal(scale=0.5, size=x.shape)

plt.scatter(x, y, s=10, alpha=0.7)
plt.title("Synthetic Data with One Breakpoint")
plt.xlabel("x")
plt.ylabel("y")
plt.grid(True)
plt.show()

psi, i, beta = segmented_regression( x,y, [1,2,3] )


X_ = [ np.ones_like( x ), x ]
for p in psi:
    X_.append( np.maximum(0, x - p) )
X = np.column_stack( X_ )

y_pred = X @ beta.T

plt.scatter(x, y, s=10, alpha=0.7, label='Data')
plt.plot(x, y_pred, color='red', label='Segmented Fit')
plt.legend()
plt.title("Segmented Regression with Muggeo's Algorithm")
plt.xlabel("x")
plt.ylabel("y")
plt.grid(True)
plt.show()

