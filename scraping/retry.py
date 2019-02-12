import urllib.request
import os, glob
import json, re, textwrap
import pandas as pd
import argparse
import sys
sys.path.append( '..' )
import config

from utilsDAWS import ops_file as rw
from utilsDAWS import ops_data as ops
from utilsDAWS.ops_thread import worker
from utilsDAWS.ops_log import logger

# parameters ----------------------------------------
path = config.path_data
storage = r''
mid_path = config.path_img
f_data = r'debug.log'
f_log = r''
log = None

partition = config.partition
concurrent = config.concurrent
timeout = config.timeout
# ---------------------------------------- parameters

# function to download the files
def download( u ):
    if( 'unknown' in u ): return
    fname = re.search( r'[0-9]*.jpg$', u ).group( 0 )
    try: urllib.request.urlretrieve( u, r'{}{}'.format( storage, fname ) )
    except: log.commit( type='error', msg=f'Failed to obtain: {u}' )

# creates the worker class and performs action
def trigger( urls ):
    # create worker class
    W = worker( concurrent=concurrent, timeout=timeout, result_to_file=False )
    for i in range( 0, len(urls), partition ):
        if( i > len( urls) ): break
        tail = (i + partition)
        if( tail >= len(urls) ): tail = len(urls)
        # run by multi-threaded worker
        W.init()
        W.input( urls[ i:tail ] ).work_with( download ).run()

def parse_file( pattern ):
    urls = []
    for n in glob.glob( r'./{}'.format( pattern ) ):
        print( n )
        content = open( n, 'r' ).readlines()
        for l in content:
            try:    url = re.findall( r'https?://(?:[-\w.\/]|(?:%[\da-fA-F]{2}))+', l )[ 0 ]
            except: continue
            urls.append( ops.clean_str( url ) )
    return urls

# the main funcion
if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument( '-d', '--data', help='Data filename pattern' )
    ap.add_argument( '-l', '--log_file', required=True, help='filename for log file' )
    ap.add_argument( '-p', "--partition", type=int, help="Size of the group of input" )
    ap.add_argument( '-c', "--concurrent", type=int, help="Number of threads" )
    ap.add_argument( '-t', "--timeout", type=int, help="Timeout for url access" )
    args = vars( ap.parse_args() )

    def val_err_msg( opt_name, msg="Value Error for opt" ):
        ap.error( "\n\n{}: {}!".format( msg, opt_name ) )

    # error handling
    if( args[ 'partition' ] != None and args[ 'partition' ] <= 0 ): val_err_msg( '-p/--partition' )
    if( args[ 'concurrent' ] != None and args[ 'concurrent' ] <= 0 ): val_err_msg( '-c/--concurrent' )
    if( args[ 'timeout' ] != None and args[ 'timeout' ] <= 0 ): val_err_msg( '-t/--timeout' )
    if( args[ 'data' ] != None ): f_data = args[ 'data' ]

    ### setting the parameters
    log = logger( fname=args[ 'log_file' ] )
    # create storage folder if not exist
    storage = r'{}{}'.format( '../', mid_path )
    rw.mkdir_p( storage )
    # if not specified by user, use the default value
    partition = config.partition if( args[ 'partition' ] == None ) else args[ 'partition' ]
    concurrent = config.concurrent if( args[ 'concurrent' ] == None ) else args[ 'concurrent' ]
    timeout = config.timeout if( args[ 'timeout' ] == None ) else args[ 'timeout' ]

    # parse the data file
    urls = parse_file( f_data )
    # start the process
    trigger( urls )