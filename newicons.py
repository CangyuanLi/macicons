# Imports

import argparse
import concurrent.futures
import functools
import json
import os
from pathlib import Path
import subprocess
import time

# Globals

BASE_PATH = Path(__file__).parent
ICONFOLDER = str(BASE_PATH / "icons")
ROOT_PATH = "/Users/cangyuanli/Documents/Projects/genfunc"

with open(BASE_PATH / "mapper.json") as f:
    mapper_dict = json.load(f)

with open(BASE_PATH / "ignorelist.txt", "r") as f:
    ignorelist = {line.strip() for line in f}

def walk_directory(root_path=ROOT_PATH):
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

def replace_icon(filepath, dumb, iconfolder=ICONFOLDER):
    if dumb == True:
        time_since_creation = 0
    elif dumb == False:
        time_created = os.path.getctime(filepath)
        time_since_creation = time.time() - time_created

    if time_since_creation < 100000: # 1 day in unix seconds + a little bit of padding
        basename = os.path.basename(filepath)
        filename, file_ext = os.path.splitext(basename)

    if file_ext in mapper_dict:
        iconpath = os.path.join(iconfolder, mapper_dict[file_ext])
        subprocess.run(["fileicon", "set", filepath, iconpath], stdout=subprocess.DEVNULL)
    elif filename in mapper_dict:
        iconpath = os.path.join(iconfolder, mapper_dict[filename])
        subprocess.run(["fileicon", "set", filepath, iconpath], stdout=subprocess.DEVNULL)

    return None

def replace_all_icons(filelist, dumb=True):
    func = functools.partial(replace_icon, dumb=dumb)

    with concurrent.futures.ThreadPoolExecutor() as pool:
        pool.map(func, filelist)

    return None

def main():
    start = time.perf_counter()
    lst = walk_directory()
    replace_all_icons(lst)
    end = time.perf_counter()
    print(f"{end-start}")

if __name__ == "__main__":
    main()


