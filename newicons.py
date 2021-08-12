import json
import os
from pathlib import Path
import subprocess

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


def main(replace_all=False):
    for root, dirs, files in os.walk(root_path, topdown=True):
        for dir in dirs:
            if dir in mapper_dict: # faster then mapper_dict.keys()
                replace_icon(root=root, path=dir, key=dir)
        
        dirs[:] = [d for d in dirs if d not in ignorelist] # don't go through some folders
        
        for file in files:
            if replace_all == True:
                output = 'NO'
            elif replace_all == False:
                output = subprocess.run(['fileicon', 'test', file], capture_output=True).stdout.decode('utf8')

            if 'NO' in output:
                filename, file_ext = os.path.splitext(file)
                
                if filename in mapper_dict:
                    replace_icon(root=root, path=file, key=filename)

                if file_ext in mapper_dict:
                    replace_icon(root=root, path=file, key=file_ext)


if __name__ == '__main__':
    main(replace_all=True)


