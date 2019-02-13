import pandas as pd
import argparse

from utilsDAWS import ops_file as rw

import sys
sys.path.append("..")
import config

# parameters ------------------------------------------------------
path = config.path_data                   # data file location
f_data = r"*.csv"                      # data filename pattern
f_result = r"combined.csv"
encoding_f = 'utf-8'
# ------------------------------------------------------ parameters

# the main function
if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument( '-d', "--data", help="Data filename pattern" )
    ap.add_argument( '-o', "--output", help="Name of the output file" )
    args = vars( ap.parse_args() )

    def val_err_msg( opt_name, msg="Value Error for opt" ):
        ap.error( "\n\n{}: {}!".format( msg, opt_name ) )

    ### setting the parameters
    f_data = f_data if( args[ 'data' ] == None ) else args[ 'data' ]
    f_result = f_result if( args[ 'output' ] == None ) else args[ 'output' ]

    rw.combine_csv_files( dir_files=path, files=f_data, dir_result=path, result=f_result, encode=encoding_f )