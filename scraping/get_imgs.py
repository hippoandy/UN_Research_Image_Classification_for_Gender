import wget
import os, glob
import json, re
import sys
sys.path.append( '..' )
import config
from utils import ops_data, ops_file

# parameters ----------------------------------------
path = config.path_data
mid_path = config.path_img
data_file = r'imgs_*.json'
# ---------------------------------------- parameters


# the main funcion
if __name__ == '__main__':
    # create storage folder if not exist
    storage = r'{}{}'.format( '../', mid_path )
    ops_file.mkdir_p( storage )

    for n in glob.glob( r'{}{}'.format( path, data_file ) ):
        urls = json.loads( open( n, 'r' ).read() )
        if( not ops_data.empty_struct( urls ) ):
            for u in urls:
                if( 'unknown' in u ): continue
                fname = re.search( r'[0-9]*.jpg$', u ).group( 0 )
                wget.download( u, out=r'{}{}'.format( storage, fname ) )
