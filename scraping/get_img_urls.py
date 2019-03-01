from utilsDAWS import value as val
from utilsDAWS import rw
from utilsDAWS.thread import work

from seleniumrequests import Chrome
from bs4 import BeautifulSoup
import pickle
import os, time
import argparse
import json
import platform

import sys
sys.path.append( '..' )
import config

# parameters ----------------------------------------
concurrent = config.concurrent

driver_path = ''
# ---------------------------------------- parameters

def read_secret():
    f = open( r'../{}'.format( 'secret.key' ) )
    for l in f.readlines():
        if( 'username' in l ):
            username = val.clean_str( l.replace( 'username:', '' ).strip() )
        elif( 'password' in l ):
            password = val.clean_str( l.replace( 'password:', '' ).strip() )
    return {
        'username': username,
        'password': password,
    }

def login():
    if( platform.system() == 'Windows' ): ### Windows
        driver_path = r'{}/chromedriver.exe'.format( config.path_driver )
    else: ### macOS or Linux
        driver_path = r'{}/chromedriver'.format( config.path_driver )

    driver = Chrome( driver_path )
    driver.get( r'{}{}'.format( config.base_url, 'login' ) )

    login_data = read_secret()
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
    c = val.clean_str( c ).replace( ' ', '_' )

    def log( c, u ):
        rw.write_to_log_text( r'{}{}'.format( config.path_data, r'log_{}.txt'.format( c ) ), "{} stops at page {}".format( c, u ) )

    driver = Chrome( driver_path )
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
    rw.write_to_json( r'{}{}'.format( config.path_data, 'imgs_{}.json'.format( c ) ), tars )
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
    countries = open( config.path_countries, 'r' ).readlines()
    work.trigger_worker( in_chunk=False,\
        data=countries, work_funct=creat_zombie, result_to_file=False,
        concurrent=len(countries), partition=len(countries), timeout=config.timeout )

# the main funcion
if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument( '-r', "--recreate", required=True, type=int, help="Re-create the auth cookies, (0/1)" )
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
