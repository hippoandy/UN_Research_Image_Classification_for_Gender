from seleniumrequests import Chrome
import pickle

import sys
sys.path.append( '..' )
import os, time
import argparse

import json
from bs4 import BeautifulSoup

import config
from utils import ops_data, ops_thread, ops_file
import scrape

# parameters ----------------------------------------
### Windows
path_driver = r'./chromedriver.exe'
### macOS or Linux
# path_driver = r'./chromedriver'

## account login
# login_data =  { 'username':'ycaho@ucdavis.edu', 'password':'Cepal2019' }
login_data =  { 'username':'BF20A3C0@mail.com', 'password':'CFA793D1' }

concurrent = config.concurrent
# ---------------------------------------- parameters


def login():
    driver = Chrome( path_driver )
    driver.get( r'{}{}'.format( config.base_url, 'login' ) )

    for k in login_data.keys():
        box = driver.find_element_by_id( k )
        box.send_keys( login_data[ k ] )
    time.sleep( config.sleep_short )
    # login!
    btn = driver.find_element_by_id( 'login_btn' )
    btn.click()
    time.sleep( config.sleep_long )

    return driver

def dump_cookies( driver ):
    pickle.dump( driver.get_cookies(), open( r"{}{}".format( config.path_data, config.f_cookie ), "wb" ) )

def creat_zombie( c ):
    print( "Doing: {}".format( c ) )
    c = ops_data.clean_str( c ).replace( ' ', '_' )

    def log( c, u ):
        ops_file.write_to_log_text( r'{}{}'.format( config.path_data, r'log_{}.txt'.format( c ) ), "{} stops at page {}".format( c, u ) )

    driver = Chrome( path_driver )
    # first load a page
    driver.get( config.base_url )
    # then load the cookie
    cookies = pickle.load( open( r"{}{}".format( config.path_data, config.f_cookie ), "rb") )
    for cookie in cookies: driver.add_cookie( cookie )

    tars = []
    with open( r'{}pages_{}.json'.format( config.path_data, c ), 'r' ) as f:
        urls = json.loads( f.read() )
        for u in urls:
            driver.get( u )
            time.sleep( config.sleep_long )
            soup = BeautifulSoup( driver.page_source, 'html5lib' )

            # imgs = soup.findAll( 'img', class_='ImageThumbnail-image' )
            imgs = soup.findAll( 'img', class_='info-card-media-user' )
            if( len( imgs ) == 0 ):
                log( c, u )
                break
            # store the image urls
            for e in imgs: tars.append( e[ 'src' ] )

    # commit the result to file
    ops_file.write_to_json( r'{}{}'.format( config.path_data, 'imgs_{}.json'.format( c ) ), tars )
    # safely quit the driver
    driver.quit()

def operation( recreate ):
    ''' create login cookies '''
    if( recreate ):
        driver = login()
        time.sleep( config.sleep_long )
        dump_cookies( driver )
        time.sleep( config.sleep_med )

    ''' start to scrape the user profile pictures '''
    worker = ops_thread.worker( concurrent=concurrent )
    with open( config.path_countries, 'r' ) as f:
        countries = f.readlines()

        # create the worker object
        for i in range( 0, len( countries ), concurrent ):
            if( i > len( countries ) ): break

            tail = (i + concurrent)
            if( tail >= len( countries ) ): tail = len( countries )

            worker.init()
            worker.work_with( creat_zombie ).input( countries[ i:tail ] ).run()

# the main funcion
if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument( '-r', "--recreate", required=True, type=int, help="Re-create the cookies?" )
    ap.add_argument( '-c', "--concurrent", type=int, help="Number of concurrent workers" )
    args = vars( ap.parse_args() )

    def val_err_msg( opt_name, msg="Value Error for opt" ):
        ap.error( "\n\n{}: {}!".format( msg, opt_name ) )

    # error handling
    if( args[ 'recreate' ] < 0 or args[ 'recreate' ] > 2 ): val_err_msg( '-r/--recreate' )

    ### setting the parameters
    concurrent = concurrent if( args[ 'concurrent' ] == None ) else args[ 'concurrent' ]

    # start the operation
    operation( args[ 'recreate' ] )
