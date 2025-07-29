import os
import shutil
from math import pi, log

class CS_SHAPES:
    SQUARE = 1
    CIRCLE = 2
    RECTANGLE = 3

    square_area = lambda base: base**2
    rectangle_area = lambda width, height: width * height
    circle_area = lambda diameter: pi * ( diameter / 2.0 )**2

    def Area( shape : int, *dimensions ):
        if shape == CS_SHAPES.SQUARE:
            return CS_SHAPES.square_area( *dimensions[:-1] ), dimensions[-1]
        elif shape == CS_SHAPES.CIRCLE:
            return CS_SHAPES.circle_area( *dimensions[:-1] ), dimensions[-1]
        elif shape == CS_SHAPES.RECTANGLE:
            return CS_SHAPES.rectangle_area( *dimensions[:-1] ), dimensions[-1]
        
class EXPERIMENT_TYPE:
    COMPRESSION = 1
    BENDING = 2

    def COMPRESSION_STRESS_STRAIN( height : float, area : float ):
        def wrap( time : float, disp : float, force : float ):
            eng_strain = disp / height
            eng_stress = force / area
            real_stress = eng_stress * ( 1 + eng_strain )
            real_strain = log( 1 + eng_strain )
            return (eng_strain, eng_stress), (real_strain, real_stress)
        return wrap
    
    def BENDING_STRESS_STRAIN( width : float, depth : float, length : float ):
        def wrap( time : float, disp : float, force : float ):
            eng_strain = 6 * disp * depth / ( length ** 2 )
            eng_stress = 3 * force * length / ( 2 * width * depth ** 2 )
            return (eng_strain, eng_stress), (eng_strain, eng_stress)
        return wrap

    def __init__(self, experiment : int, shape : int, *dimensions ):
        if experiment == EXPERIMENT_TYPE.COMPRESSION:
            area, height = CS_SHAPES.Area( shape, *dimensions )
            self.f = EXPERIMENT_TYPE.COMPRESSION_STRESS_STRAIN( height, area )
        elif experiment == EXPERIMENT_TYPE.BENDING:
            self.f = EXPERIMENT_TYPE.BENDING_STRESS_STRAIN( *dimensions )

    def StressStrain( self, time : float, disp : float, force : float ):
        return self.f( time, disp, force )


def parse_data( data : list[dict], filename : str, cross_section_shape : int, experiment_type : int = EXPERIMENT_TYPE.COMPRESSION ):

    dirname = os.path.dirname( filename )
    shutil.rmtree( dirname, True )
    os.makedirs( dirname )

    for i, entry in enumerate( data ):
        with open( filename.format( i + 1 ), "w" ) as pFile:
            exp = EXPERIMENT_TYPE( experiment_type, cross_section_shape, *entry["dim"] )
            for time, disp, force in entry["data"]:
                eng, real = exp.StressStrain( time, disp, force )
                eng_strain, eng_stress = eng
                real_strain, real_stress = real
                print( f"{eng_strain},{eng_stress},{real_strain},{real_stress}", file=pFile )        

            #area, height = CS_SHAPES.Area( cross_section_shape, *entry["dim"] )
            #for time, disp, force in entry["data"]:
            #    eng_strain = disp / height
            #    eng_stress = force / area
            #    real_stress = eng_stress * ( 1 + eng_strain )
            #    real_strain = log( 1 + eng_strain )
            #    print( f"{eng_strain},{eng_stress},{real_strain},{real_stress}", file=pFile )        