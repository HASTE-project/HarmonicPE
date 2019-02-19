from harmonicPE.daemon import listen_for_tasks

import time
import subprocess
from os import environ

def busyfunction(busytime, cpulevel):
    p = subprocess.Popen(['lookbusy',
                          '--ncpus', environ.get("NUM_CORES", "1"),
                          '--cpu-util', cpulevel])
    time.sleep(busytime)
    p.terminate()
    p.communicate()
    del p

def process_data(data):
    # Format of binary message representing task for distributed execution is specific to your application.
    print('Busying the CPU...', flush=True)
    busytime = int(environ.get("BUSY_TIME", 60))
    cpulevel = environ.get("CPU_LEVEL", "20")
    # Busy CPU some time
    busyfunction(busytime, cpulevel)



# Start the daemon to listen for tasks:
listen_for_tasks(process_data)
