from matplotlib import pyplot as plt

plt.rcParams.update({
    "font.family": "Cambria"
})

class Utils:
    def format_line( line : str ):
        return [ float(l) for l in line.split( "," ) ]
    
    def read_data( file : str ):
        eng_strain = []
        eng_stress = []
        real_strain = []
        real_stress = []
        with open( file, "r" ) as pFile:
            for line in pFile.readlines():
                e, s, re, rs = tuple( Utils.format_line( line ) )
                eng_strain.append( e )
                eng_stress.append( s )
                real_strain.append( re )
                real_stress.append( rs )
        return eng_strain, eng_stress,  real_strain, real_stress
    

    def plot( file : str, type : str = "real" ):
        e,s,re,rs = Utils.read_data( file )
        if type == "real":
            plt.plot( re,rs )
        elif type == "eng":
            plt.plot( e,s )

for i in range( 1, 6 ):
    Utils.plot( f"./process/result_probe_{i}.csv" )

plt.title( "Stress-strain curve 0°" )
plt.xlabel( "Strain" )
plt.ylabel( "Stress" )
plt.xlim( [0,0.05] )
plt.ylim( [0,60] )


plt.figure()

for i in range( 6, 11 ):
    Utils.plot( f"./process/result_probe_{i}.csv" )

plt.title( "Stress-strain curve 45°" )
plt.xlabel( "Strain" )
plt.ylabel( "Stress" )
plt.xlim( [0,0.05] )
plt.ylim( [0,60] )

plt.figure()

for i in range( 11, 16 ):
    Utils.plot( f"./process/result_probe_{i}.csv" )

plt.title( "Stress-strain curve 90°" )
plt.xlabel( "Strain" )
plt.ylabel( "Stress" )
plt.xlim( [0,0.07] )
plt.ylim( [0,50] )

plt.figure()

for i in range( 1, 16 ):
    Utils.plot( f"./process/result_probe_{i}.csv" )

plt.title( "Stress-strain curve" )
plt.xlabel( "Strain" )
plt.ylabel( "Stress" )
plt.xlim( [0,0.3] )
plt.ylim( [0,150] )
plt.show()
plt.show()
