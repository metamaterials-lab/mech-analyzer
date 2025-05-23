import os
import shutil
from math import pi, log

class CS_SHAPES:
    SQUARE = 1
    CIRCLE = 2

    square_area = lambda base: base**2
    circle_area = lambda diameter: pi * ( diameter / 2.0 )**2

    def Area( shape : int, *dimensions ):
        if shape == CS_SHAPES.SQUARE:
            return CS_SHAPES.square_area( *dimensions[:-1] ), dimensions[-1]
        elif shape == CS_SHAPES.CIRCLE:
            return CS_SHAPES.circle_area( *dimensions[:-1] ), dimensions[-1]

def parse_data( data : list[dict], filename : str, cross_section_shape : int ):

    dirname = os.path.dirname( filename )
    shutil.rmtree( dirname, True )
    os.makedirs( dirname )

    for i, entry in enumerate( data ):
        with open( filename.format( i + 1 ), "w" ) as pFile:
            area, height = CS_SHAPES.Area( cross_section_shape, *entry["dim"] )
            for time, disp, force in entry["data"]:
                eng_strain = disp / height
                eng_stress = force / area
                real_stress = eng_stress * ( 1 + eng_strain )
                real_strain = log( 1 + eng_strain )
                print( f"{eng_strain},{eng_stress},{real_strain},{real_stress}", file=pFile )        