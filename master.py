import os                                                                       
from multiprocessing import Pool                                                
                                                                                
                                                                                
processes = ('start.py', 'slave-cam.py')                                
                                                  
                                                                                
def run_process(process):                                                             
    os.system('python3.6 {}'.format(process))                                       
                                                                                
                                                                                
pool = Pool(processes=2)                                     
pool.map(run_process, processes)   