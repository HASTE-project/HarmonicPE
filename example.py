from harmonicPE.daemon import listen_for_tasks
import json
import time
import subprocess
from os import environ
import uuid
from PIL import Image
import os, io


def busyfunction(busytime):
    p = subprocess.Popen(['python', './dummyload.py'])
    time.sleep(busytime)
    p.terminate()
    p.communicate()
    del p

def old_process_data(data):
    # Format of binary message representing task for distributed execution is specific to your application.
    print('Busying the CPU...\n', flush=True)
    busytime = int(environ.get("BUSY_TIME", 60))
    # Busy CPU some time
    busyfunction(busytime)

def get_metadata_and_data(message_bytes):

    sep_point = message_bytes.find(b';')
    b_metadata = message_bytes[0:sep_point-1]
    b_data = message_bytes[sep_point+2:]
    return b_metadata, b_data

def process_data(message_bytes):
    # Format of binary message representing task for distributed execution is specific to your application.
    print('message was bytes: ' + str(len(message_bytes)), flush=True)
    b_metadata, b_data = get_metadata_and_data(message_bytes)

    image_file =  b_data

    metadata_str = b_metadata.decode('utf-8')
    metadata = json.loads(metadata_str)
    not_unique_id = 1
    uuid_local_dir = None
    local_file = None
    path_to_data_file = None
    path_to_dir = None
    while not_unique_id:
        uuid_local_dir = str(uuid.uuid1())
        local_file = metadata['name']
        cwd = os.getcwd()
        path_to_dir = cwd+'/'+uuid_local_dir
        path_to_data_file = cwd+'/'+uuid_local_dir+'/'+local_file
        if not os.path.exists(path_to_dir):
            os.makedirs(path_to_dir)
            if not os.path.exists(path_to_data_file):
                image = Image.open(io.BytesIO(image_file))
                image.save(path_to_data_file)
                not_unique_id = 0
                break
        else:
            continue
    status, output = subprocess.getstatusoutput('cellprofiler -p Salman_CellProfiler_cell_counter_no_specified_folders.cpproj -i '+ path_to_dir + ' &> /dev/null')
    if status == 0:
        subprocess.getstatusoutput('rm -r '+path_to_dir)
        print("image analysis complete!")
    else:
        pass

# Start the daemon to listen for tasks:
listen_for_tasks(process_data)
