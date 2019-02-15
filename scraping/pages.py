from utilsDAWS import value as val
from utilsDAWS import rw

# from selenium import webdriver
from seleniumrequests import Chrome
from bs4 import BeautifulSoup

import pickle
import wget
import os, time
import json
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

import sys
sys.path.append( '..' )
import config

# url = config.base_url + 'freelancers/{}/all/{}'
url = config.base_url + 'search/users/any_skill/{}/{}/'

limit = 1000
f_result = 'pages_{}.json'

if __name__ == '__main__':
    # create page urls
    with open( config.path_countries, 'r' ) as f:
        countries = f.readlines()

        for c in countries:
            urls = []
            c = val.clean_str( c )
            for i in range( 1, limit ):
                c = c.replace( ' ', '_' )
                urls.append( url.format( c.lower(), i ) )
            rw.write_to_json( r'{}{}'.format( config.path_data, f_result.format( c ) ), urls )