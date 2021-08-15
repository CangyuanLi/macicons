import argparse
import json
import os
from pathlib import Path
import subprocess
import time

base_path = Path(__file__).parent
iconfolder = str(base_path / 'icons')
root_path = '/Users/cangyuanli/Documents/'

with open(base_path / 'mapper.json') as f:
    mapper_dict = json.load(f)

with open(base_path / 'ignorelist.txt', 'r') as f:
    ignorelist = {line.strip() for line in f}

def replace_icon(root, path, key):
    fullpath = os.path.join(root, path)
    iconpath = os.path.join(iconfolder, mapper_dict[key])

    subprocess.run(['fileicon', 'set', fullpath, iconpath], stdout=subprocess.DEVNULL)

def replace_all_icons(dumb):
    changes = 0
    for root, dirs, files in os.walk(root_path, topdown=True):
        for dir in dirs:
            if dir in mapper_dict: # faster then mapper_dict.keys()
                replace_icon(root=root, path=dir, key=dir)
                changes += 1
        
        dirs[:] = [d for d in dirs if d not in ignorelist] # don't go through some folders
        
        for file in files:
            if dumb == True:
                time_since_creation = 0
            elif dumb == False:
                time_created = os.path.getctime(os.path.join(root, file))
                time_since_creation = time.time() - time_created

            if time_since_creation < 100000: # 1 day in unix seconds + a little bit of padding
                filename, file_ext = os.path.splitext(file)
                
                if filename in mapper_dict:
                    replace_icon(root=root, path=file, key=filename)
                    changes += 1

                if file_ext in mapper_dict:
                    replace_icon(root=root, path=file, key=file_ext)
                    changes += 1

    return changes

def main():
    start = time.time()
    changes = replace_all_icons(dumb=False)
    end = time.time()
    print(f'Made {changes} changes in {round(end - start, 2)} seconds.')

if __name__ == '__main__':
    main()


