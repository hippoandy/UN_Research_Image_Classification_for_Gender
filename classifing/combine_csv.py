import csv, glob
import pandas as pd
import argparse
import os

import sys
sys.path.append("..")
import config

# parameters ------------------------------------------------------
path = config.path_data                   # data file location
f_data = r"*.csv"                      # data filename pattern
f_result = r"combined.csv"
encoding_f = 'utf-8'
# ------------------------------------------------------ parameters

def operation():
    list_ = []
    for n in glob.glob( r'{}{}'.format( path, f_data ) ):
        if( 'err' in str(n) ): continue # prevent from reading the log files

        df = pd.read_csv( n, header=0, encoding=encoding_f )
        list_.append( df )

    df = pd.concat( list_, axis=0, ignore_index=True )
    df = df.drop( columns=[ 'path' ] )
    df.to_csv( '{}{}'.format( path, f_result ), encoding=encoding_f, index=False )

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

    # delete old combined result data
    pre = r'{}{}'.format( path, f_result )
    if( os.path.isfile( pre ) ): os.remove( pre )

    # start the operation
    operation()