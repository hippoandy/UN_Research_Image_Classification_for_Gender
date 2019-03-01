from utilsDAWS import value as val
from utilsDAWS import folder
from utilsDAWS.thread import work
from utilsDAWS.log import logger

import urllib.request
import argparse, os, glob
import json, re
import pandas as pd

import sys
sys.path.append( '..' )
import config

# parameters ----------------------------------------
storage = r'{}/{}'.format( '../', config.path_img )
f_log = r'debug.log'
# ---------------------------------------- parameters

l = logger( fname=f_log )

# function to download the files
def download( u ):
    if( 'unknown' in u ): return
    fname = re.search( r'[0-9]*.jpg$', u ).group( 0 )
    try: urllib.request.urlretrieve( u, r'{}{}'.format( storage, fname ) )
    except: l.commit( type='error', msg=f'Failed to obtain: {u}' )

# creates the worker class and performs action
def trigger( urls, \
    concurrent=config.concurrent, \
    partition=config.concurrent, \
    timeout=config.timeout ):
    work.trigger_worker( in_chunk=True,\
        data=urls, work_funct=download, result_to_file=False,
        concurrent=concurrent, partition=partition, timeout=timeout )

# parse the pre-processed json files
def parse_preprocess():
    urls = []
    for n in glob.glob( r'{}/{}'.format( config.path_data, r'imgs*.json' ) ):
        tmp = json.loads( open( n, 'r' ).read() )
        if( not val.empty_struct( tmp ) ): urls += tmp
    if( not val.empty_struct( urls ) ): return urls
    else:
        print( 'No URLs to download, terminated the program......' )
        sys.exit( 0 )

# retry failed urs
def retry( concurrent=config.concurrent, \
    partition=config.partition, \
    timeout=config.timeout ):
    urls = []
    for n in glob.glob( r'./{}'.format( f_log ) ):
        content = open( n, 'r' ).readlines()
        for l in content:
            try:    url = re.findall( r'https?://(?:[-\w.\/]|(?:%[\da-fA-F]{2}))+', l )[ 0 ]
            except: continue
            urls.append( val.clean_str( url ) )
    if( not val.empty_struct( urls ) ): return
    trigger( urls, concurrent, partition, timeout )

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

    # create storage folder if not exist
    folder.mkdir_p( storage )
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
            for n in glob.glob( r'{}/{}'.format( config.path_data, f_data ) ):
                df = pd.read_csv( n, header=0 )
                if( df_all == None ): df_all = df
                else: df_all.append( df )
        except:
            print( f'''Data file "{f_data}" not exists! Terminating the program......''' )
            sys.exit( 1 )
        if( not df_all.empty ): urls = df[ 'profile_logo' ].tolist()
        if( val.empty_struct( urls ) ): print( 'No URLs to download, terminating the program......' )
        else: trigger( urls, concurrent, partition, timeout )
    # using the already exist json file to perform downloads
    else: trigger( parse_preprocess(), concurrent, partition, timeout )

    # retry failed urls
    retry( concurrent, partition, timeout )