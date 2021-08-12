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


for root, dirs, files in os.walk(root_path, topdown=True):
    dirs[:] = [d for d in dirs if d not in ignorelist]

    for dir in dirs:
        if dir in mapper_dict: # faster then mapper_dict.keys()
            dirpath = os.path.join(root, dir)
            iconpath = os.path.join(iconfolder, mapper_dict[dir])

            subprocess.run(['fileicon', 'set', dirpath, iconpath], stdout=subprocess.DEVNULL)
    
    dirs[:] = [d for d in dirs if not d.startswith('.')] # don't check hidden folders
    
    for file in files:
        filename, file_ext = os.path.splitext(file)
        
        if filename in mapper_dict:
            filepath = os.path.join(root, file)
            iconpath = os.path.join(iconfolder, mapper_dict[filename])

            subprocess.run(['fileicon', 'set', filepath, iconpath], stdout=subprocess.DEVNULL)

        if file_ext in mapper_dict:
            filepath = os.path.join(root, file)
            iconpath = os.path.join(iconfolder, mapper_dict[file_ext])

            subprocess.run(['fileicon', 'set', filepath, iconpath], stdout=subprocess.DEVNULL)