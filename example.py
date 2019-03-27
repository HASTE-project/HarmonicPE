from harmonicPE.daemon import listen_for_tasks

import time
import subprocess
from os import environ

def busyfunction(busytime):
    p = subprocess.Popen(['python', './dummyload.py'])
    time.sleep(busytime)
    p.terminate()
    p.communicate()
    del p

def process_data(data):
    # Format of binary message representing task for distributed execution is specific to your application.
    print('Busying the CPU...\n', flush=True)
    busytime = int(environ.get("BUSY_TIME", 60))
    # Busy CPU some time
    busyfunction(busytime)



# Start the daemon to listen for tasks:
listen_for_tasks(process_data)
