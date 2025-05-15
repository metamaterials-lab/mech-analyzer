from utils.Processor import Shimadzu, parse_data, CS_SHAPES

with Shimadzu( "./results/raw/muestra_15-1.csv", "./dimensions.csv" ) as data:
    parse_data( data, "./results/cured/result_probe_{}.csv", CS_SHAPES.CIRCLE )
        