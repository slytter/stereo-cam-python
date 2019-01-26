import os
from multiprocessing import Pool

processes = ('slave-cam.py', 'start.py')

def run_process(process):
	os.system('sudo python3.6 {}'.format(process))

pool = Pool(processes=2)
pool.map(run_process, processes)
