# Imports

import argparse
import functools
import json
import multiprocessing
import os
from pathlib import Path
import subprocess
import time

# Globals

BASE_PATH = Path(__file__).parent
ICONFOLDER = str(BASE_PATH / "icons")
ROOT_PATH = "/Users/cangyuanli/Documents/Projects/genfunc"
CORES = multiprocessing.cpu_count()

with open(BASE_PATH / "mapper.json") as f:
    mapper_dict = json.load(f)

with open(BASE_PATH / "ignorelist.txt", "r") as f:
    ignorelist = {line.strip() for line in f}

def replace_icon(root, path, key, iconfolder=ICONFOLDER):
    fullpath = os.path.join(root, path)
    iconpath = os.path.join(iconfolder, mapper_dict[key])

    subprocess.run(["fileicon", "set", fullpath, iconpath], stdout=subprocess.DEVNULL)

def replace_file_icon(file, root, dumb):
    if dumb == True:
        time_since_creation = 0
    elif dumb == False:
        time_created = os.path.getctime(os.path.join(root, file))
        time_since_creation = time.time() - time_created

    if time_since_creation < 100000: # 1 day in unix seconds + a little bit of padding
        filename, file_ext = os.path.splitext(file)
    
    if filename in mapper_dict:
        replace_icon(root=root, path=file, key=filename)

    if file_ext in mapper_dict:
        replace_icon(root=root, path=file, key=file_ext)

    return

def replace_all_icons(root_path=ROOT_PATH, dumb=True, cores=CORES):
    for root, dirs, files in os.walk(root_path, topdown=True):
        for dir in dirs:
            if dir in mapper_dict: # faster then mapper_dict.keys()
                replace_icon(root=root, path=dir, key=dir)
        
        # modifies directory list in place
        # this is needed for os.walk to ignore these directories
        # when visiting the subsequent subdirectories / files
        dirs[:] = [d for d in dirs if d not in ignorelist]

        func = functools.partial(replace_file_icon, root=root, dumb=True)
        
        with multiprocessing.Pool(processes=cores) as pool:
            pool.map(func, files)

    return None

def main():
    start = time.perf_counter()
    replace_all_icons()
    end = time.perf_counter()
    print(f"Finished in {round(end - start, 2)} seconds.")

if __name__ == "__main__":
    main()


