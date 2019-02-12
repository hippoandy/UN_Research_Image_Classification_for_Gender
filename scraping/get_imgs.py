import urllib.request
import os, glob
import json, re, textwrap
import pandas as pd
import argparse
import sys
sys.path.append( '..' )
import config
from utils import ops_file as rw
from utils import ops_data as ops
from utils.ops_thread import worker
from utils.ops_log import logger

# parameters ----------------------------------------
path = config.path_data
storage = ""
mid_path = config.path_img
f_data = r''
f_urls = r'imgs*.json'

partition = config.partition
concurrent = config.concurrent
timeout = config.timeout
# ---------------------------------------- parameters

l = logger()

# function to download the files
def download( u ):
    if( 'unknown' in u ): return
    fname = re.search( r'[0-9]*.jpg$', u ).group( 0 )
    try: urllib.request.urlretrieve( u, r'{}{}'.format( storage, fname ) )
    except: l.commit( type='error', msg=f'Failed to obtain: {u}' )

# creates the worker class and performs action
def trigger( urls ):
    # create worker class
    W = worker( concurrent=concurrent, timeout=timeout )
    for i in range( 0, len(urls), partition ):
        if( i > len( urls) ): break
        tail = (i + partition)
        if( tail >= len(urls) ): tail = len(urls)
        # run by multi-threaded worker
        W.init()
        W.input( urls[ i:tail ] ).work_with( download ).run()

# parse the pre-processed json files
def parse_preprocess():
    urls = []
    for n in glob.glob( r'{}{}'.format( path, f_urls ) ):
        tmp = json.loads( open( n, 'r' ).read() )
        if( not ops.empty_struct( tmp ) ): urls += tmp
    # starting the download
    if( not ops.empty_struct( urls ) ): return urls
    else:
        print( 'No URLs to download, terminated the program......' )
        sys.exit( 0 )
        
# the main funcion
if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument( '-u', "--use_data", required=True, type=int, help="Load data file for URLs? (0/1)" )
    ap.add_argument( '-p', "--partition", type=int, help="Size of the group of input" )
    ap.add_argument( '-c', "--concurrent", type=int, help="Number of threads" )
    ap.add_argument( '-t', "--timeout", type=int, help="Timeout for url access" )
    args = vars( ap.parse_args() )

    def val_err_msg( opt_name, msg="Value Error for opt" ):
        ap.error( "\n\n{}: {}!".format( msg, opt_name ) )

    # error handling
    if( args[ 'use_data' ] < 0 or args[ 'use_data' ] > 2 ): val_err_msg( '-u/--use_data' )
    if( args[ 'partition' ] != None and args[ 'partition' ] <= 0 ): val_err_msg( '-p/--partition' )
    if( args[ 'concurrent' ] != None and args[ 'concurrent' ] <= 0 ): val_err_msg( '-c/--concurrent' )
    if( args[ 'timeout' ] != None and args[ 'timeout' ] <= 0 ): val_err_msg( '-t/--timeout' )

    ### setting the parameters
    # create storage folder if not exist
    storage = r'{}{}'.format( '../', mid_path )
    rw.mkdir_p( storage )
    # if not specified by user, use the default value
    partition = config.partition if( args[ 'partition' ] == None ) else args[ 'partition' ]
    concurrent = config.concurrent if( args[ 'concurrent' ] == None ) else args[ 'concurrent' ]
    timeout = config.timeout if( args[ 'timeout' ] == None ) else args[ 'timeout' ]

    if( args[ 'use_data' ] ):
        # open data file to create the img URLs
        # please enter the f_data pattern:
        f_data = input( "Enter the file name: " )
        df_all = None
        try:
            for n in glob.glob( r'{}/{}'.format( path, f_data ) ):
                df = pd.read_csv( n, header=0 )
                if( df_all == None ): df_all = df
                else: df_all.append( df )
        except:
            print( textwrap.dedent(f'''
                Data file "{f_data}" not exists!
                Terminated the program!
            '''))
            sys.exit( 1 )
        if( not df_all.empty ): urls = df[ 'profile_logo' ].tolist()
        if( ops.empty_struct( urls ) ): print( 'No URLs to download, terminated the program......' )
        else: trigger( urls )
    # using the already exist json file to perform downloads
    else: trigger( parse_preprocess() )