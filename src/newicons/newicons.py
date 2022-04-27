# Imports

import argparse
import concurrent.futures
import functools
import json
import os
from pathlib import Path
import subprocess
import threading
import time

# Globals

BASE_PATH = Path(__file__).parent
ICONFOLDER = str(BASE_PATH / "icons")
ROOT_PATH = "/Users/cangyuanli/Documents"

COUNTER = 0

# Parser

parser = argparse.ArgumentParser(description="Change file icons")
parser.add_argument(
    "rootpath",
    type=str,
    help="directory to start in"
)

parser.add_argument(
    "--dumb",
    action="store_true",
    required=False,
    help="If dumb, does not check the time file was created"
)

parser.add_argument(
    "--nice",
    action="store_true",
    required=False,
    help="If nice, sets script to low priority"
)

args = parser.parse_args()

# Functions

def read_mapper(path=BASE_PATH):
    with open(path / "mapper.json") as f:
        mapper_dict = json.load(f)

    return mapper_dict

def read_ignorelist(path=BASE_PATH):
    with open(path / "ignorelist.txt", "r") as f:
        ignorelist = {line.strip() for line in f}

    return ignorelist

def walk_directory(ignorelist, mapper_dict, root_path=ROOT_PATH):
    filelist = []
    for root, dirs, files in os.walk(root_path, topdown=True):
        for dir in dirs:
            if dir in mapper_dict:
                filelist.append(os.path.join(root, dir))

        # modifies directory list in place
        # this is needed for os.walk to ignore these directories
        # when visiting the subsequent subdirectories / files
        dirs[:] = [d for d in dirs if d not in ignorelist]
        filelist += [os.path.join(root, f) for f in files]

    return filelist

def replace_icon(filepath, dumb, nice, mapper_dict, iconfolder=ICONFOLDER):
    if nice is True:
        time.sleep(0.01)

    if dumb is True:
        time_since_creation = 0
    elif dumb is False:
        time_created = os.stat(filepath).st_birthtime
        time_since_creation = time.time() - time_created

    if time_since_creation < 90_000: # 1 day in unix seconds + a little bit of padding
        basename = os.path.basename(filepath)
        filename, file_ext = os.path.splitext(basename)

        if file_ext in mapper_dict:
            iconpath = os.path.join(iconfolder, mapper_dict[file_ext])
        elif filename in mapper_dict:
            iconpath = os.path.join(iconfolder, mapper_dict[filename])
        else:
            iconpath = None

        if iconpath is not None:
            subprocess.run(["fileicon", "set", filepath, iconpath], stdout=subprocess.DEVNULL)

            with threading.Lock():
                global COUNTER
                COUNTER += 1
    else:
        pass

    return None

def replace_all_icons(filelist, mapper_dict, dumb, nice):
    func = functools.partial(replace_icon, mapper_dict=mapper_dict, dumb=dumb, nice=nice)

    with concurrent.futures.ThreadPoolExecutor() as pool:
        pool.map(func, filelist)

    return len(filelist)

def display_time(seconds):
    m, s = divmod(seconds, 60)
    h, m = divmod(m, 60)

    return f"{h} hours, {m} minutes, and {s:.2f} seconds"

# Main

def main(rootpath=args.rootpath, dumb=args.dumb, nice=args.nice):
    start = time.perf_counter()

    if nice is True:
        os.nice(19)
        
    mapper_dict = read_mapper()
    ignorelist = read_ignorelist()
    lst = walk_directory(ignorelist=ignorelist, mapper_dict=mapper_dict, root_path=rootpath)
    numfiles = replace_all_icons(filelist=lst, mapper_dict=mapper_dict, dumb=dumb, nice=nice)

    end = time.perf_counter()
    print(f"Visited {numfiles} files and made {COUNTER} changes in {display_time(end - start)}.")

if __name__ == "__main__":
    main()
