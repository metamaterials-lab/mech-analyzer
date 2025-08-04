import os
import shutil

from utils.Processor.Experiments import EXPERIMENTS
from utils.Processor.ExperimentTypes import ExperimentTypes

def parse_data( data : list[dict], filename : str, cross_section_shape : int, experiment_type : int = ExperimentTypes.TENSILE ):

    dirname = os.path.dirname( filename )
    shutil.rmtree( dirname, True )
    os.makedirs( dirname )

    for i, entry in enumerate( data ):
        with open( filename.format( i + 1 ), "w" ) as pFile:
            exp = EXPERIMENTS( experiment_type, cross_section_shape, *entry["dim"] )
            for time, disp, force in entry["data"]:
                line_data = exp.StressStrain( time, disp, force )
                print( ",".join( [ f"{d}" for d in line_data ] ), file=pFile )        
