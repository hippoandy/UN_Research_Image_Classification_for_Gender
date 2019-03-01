from utilsDAWS import value as val
from utilsDAWS import file
from utilsDAWS import rw
from utilsDAWS.thread import work
from utilsDAWS.log import logger

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
cookie_path = r"{}/{}".format( config.path_data, config.f_cookie )
driver_path = ''
# ---------------------------------------- parameters

l = logger( fname='debug_scrape.log', mode='a+' )

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
    driver = Chrome( driver_path )
    driver.get( config.url_login )

    login_data = read_secret()
    for k in login_data.keys():
        box = driver.find_element_by_id( k )
        box.send_keys( login_data[ k ] )
    time.sleep( config.sleep_short )
    # login!
    btn = driver.find_element_by_id( 'login_btn' )
    btn.click()
    time.sleep( config.sleep_long )

    # dump the cookies
    pickle.dump( driver.get_cookies(), open( cookie_path, "wb" ) )

def creat_zombie( c ):
    print( f'''Processing: {c}''' )
    c = val.clean_str( c ).replace( ' ', '_' )
    driver = Chrome( driver_path )
    # first load a page
    driver.get( config.base_url )
    # then load the cookie
    cookies = pickle.load( open( cookie_path, "rb") )
    for cookie in cookies: driver.add_cookie( cookie )

    tars = []
    with open( r'{}/pages_{}.json'.format( config.path_data, c ), 'r' ) as f:
        urls = json.loads( f.read() )
        for u in urls:
            driver.get( u )
            time.sleep( config.sleep_long )
            soup = BeautifulSoup( driver.page_source, 'html5lib' )

            # imgs = soup.findAll( 'img', class_='ImageThumbnail-image' )
            imgs = soup.findAll( 'img', class_='info-card-media-user' )
            if( len( imgs ) == 0 ):
                l.commit( type='error', msg=f'Failed! Country: {c}, url: {u}' )
                break
            # store the image urls
            for e in imgs: tars.append( e[ 'src' ] )

    # commit the result to file
    rw.write_to_json( r'{}/{}'.format( config.path_data, 'imgs_{}.json'.format( c ) ), tars )
    # safely quit the driver
    driver.quit()

# the main function
if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument( '-r', "--recreate", required=False, type=int, help="Re-create the auth cookies, (0/1)" )
    ap.add_argument( '-c', "--concurrent", type=int, help="Number of concurrent workers" )
    args = vars( ap.parse_args() )

    def val_err_msg( opt_name, msg="Value Error for opt" ):
        ap.error( "\n\n{}: {}!".format( msg, opt_name ) )

    # error handling
    if( args[ 'recreate' ] < 0 or args[ 'recreate' ] > 2 ): val_err_msg( '-r/--recreate' )
    # setting the parameters
    concurrent = config.concurrent if( args[ 'concurrent' ] == None ) else args[ 'concurrent' ]

    # start the operation
    ''' set the driver path '''
    if( platform.system() == 'Windows' ): ### Windows
        driver_path = r'{}/chromedriver.exe'.format( config.path_driver )
    else: ### macOS or Linux
        driver_path = r'{}/chromedriver'.format( config.path_driver )

    ''' create credential cookies '''
    if( args[ 'recreate' ] or not file.is_file_exist( cookie_path ) ): login()

    ''' create page urls '''
    limit = 1000
    # create page urls
    for c in config.countries:
        urls = []
        c = val.clean_str( c )
        for i in range( 1, limit ):
            c = c.replace( ' ', '_' )
            urls.append( config.user_pages.format( c.lower(), i ) )
        rw.write_to_json( r'{}/{}'.format( config.path_data, f'pages_{c}.json' ), urls )
    # wait for the data to be successfully committed
    time.sleep( config.sleep_med )

    ''' start to scrape the user profile pictures '''
    work.trigger_worker( in_chunk=True,\
        data=config.countries, work_funct=creat_zombie, result_to_file=False,
        concurrent=concurrent, partition=concurrent, timeout=config.timeout )
