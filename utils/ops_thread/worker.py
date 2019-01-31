

import threading
import queue

import textwrap
from traceback import format_exc

import wget

__all__ = [ 'worker' ]

# self-defined classes ---------------------------------------------
class worker():
    # constructor
    def __init__( self, name='worker', timeout=10, concurrent=30 ):
        self.name = name
        self.timeout = timeout
        self.concurrent = concurrent
        self.parse_funct = None
        self.obj_list = []
        self.job_queue = queue.Queue()
        self.lock = threading.Lock()
        self.finished = 0
        self._spawn()

    def init( self ):
        self.obj_list = []
        self.finished = 0

    def work_with( self, funct ):
        self.parse_funct = funct
        return self
    # set the data to be parsed
    def input( self, obj_list ):
        if( not self.obj_list ): self.obj_list = obj_list
        return self
    # ignitiate the thread
    def run( self ):
        print( textwrap.dedent( f'''
            Working on the given task......
                Number of items: {len( self.obj_list )}
        ''') )
        for obj in self.obj_list: self.job_queue.put( obj )
        self.job_queue.join()
        print( 'finished!' )
    # things for the thread to do
    def _job( self ):
        while True:
            obj = self.job_queue.get()
            try:
                self.parse_funct( obj )
                self.lock.acquire()
            except Exception as err:
                print( str(err) )
                self.lock.acquire()
            finally:
                self.finished += 1
                print(f'process: {100 * self.finished / len(self.obj_list):.2f}%', end='\r')
                self.lock.release()
                self.job_queue.task_done()
    # creating the threads
    def _spawn( self ):
        for _ in range( 0, self.concurrent ):
            t = threading.Thread( target=self._job )
            t.daemon = True
            t.start()
# --------------------------------------------- self-defined classes