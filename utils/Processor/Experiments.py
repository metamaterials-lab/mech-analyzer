from math import pi, log
from utils.Processor.ExperimentTypes import ExperimentTypes

class CS_SHAPES:
    SQUARE = 1
    CIRCLE = 2
    RECTANGLE = 3

    square_area = lambda base: base**2
    rectangle_area = lambda width, height: width * height
    circle_area = lambda diameter: pi * ( diameter / 2.0 )**2

    @classmethod
    def Area( cls, shape : int, *dimensions ):
        if shape == CS_SHAPES.SQUARE:
            return CS_SHAPES.square_area( *dimensions[:-1] ), dimensions[-1]
        elif shape == CS_SHAPES.CIRCLE:
            return CS_SHAPES.circle_area( *dimensions[:-1] ), dimensions[-1]
        elif shape == CS_SHAPES.RECTANGLE:
            return CS_SHAPES.rectangle_area( *dimensions[:-1] ), dimensions[-1]
        return 1,1



class EXPERIMENTS:
    @classmethod
    def COMPRESSION_STRESS_STRAIN( cls, height : float, area : float ):
        def wrap( time : float, disp : float, force : float ):
            eng_strain = disp / height
            eng_stress = force / area
            real_stress = eng_stress * ( 1 + eng_strain )
            real_strain = log( 1 + eng_strain )
            return eng_strain, eng_stress, real_strain, real_stress
        return wrap
    
    @classmethod
    def BENDING_STRESS_STRAIN(cls, width : float, depth : float, length : float ):
        def wrap( time : float, disp : float, force : float ):
            D790_strain = 6 * disp * depth / ( length ** 2 )
            D790_stress = 3 * force * length / ( 2 * width * depth ** 2 )
            C3PB_strain = 6 * disp * depth / ( length ** 2 )
            C3PB_e = ( force * length ** 3 ) / ( 4 * disp * width * depth ** 3 + 1E-4 )
            return D790_strain, D790_stress, C3PB_strain, C3PB_e
        return wrap

    def __init__(self, experiment : int, shape : int, *dimensions ):
        if experiment == ExperimentTypes.TENSILE:
            area, height = CS_SHAPES.Area( shape, *dimensions )
            self.f = EXPERIMENTS.COMPRESSION_STRESS_STRAIN( height, area )
        elif experiment == ExperimentTypes.BENDING:
            self.f = EXPERIMENTS.BENDING_STRESS_STRAIN( *dimensions )

    def StressStrain( self, time : float, disp : float, force : float ):
        return self.f( time, disp, force )
