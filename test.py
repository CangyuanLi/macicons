import argparse
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

parser = argparse.ArgumentParser()
parser.add_argument(
    dest='specified_types',
    nargs='*',
    type=str,
    default=None,
    help='A list of file extensions / names / folder names to check. Default is all in mapper.json.'
)
parser.add_argument(
    '-d',
    '--dumb',
    action = 'store_true',
    help='Removes check for existing custom icons. Slow for large amount of files.'
)
args = parser.parse_args()


def replace_icon(root, path, key):
    fullpath = os.path.join(root, path)
    iconpath = os.path.join(iconfolder, mapper_dict[key])

    subprocess.run(['fileicon', 'set', fullpath, iconpath], stdout=subprocess.DEVNULL)

def replace_all_icons(dumb):
    for root, dirs, files in os.walk(root_path, topdown=True):
        for dir in dirs:
            if dir in mapper_dict: # faster then mapper_dict.keys()
                replace_icon(root=root, path=dir, key=dir)
        
        dirs[:] = [d for d in dirs if d not in ignorelist] # don't go through some folders
        
        for file in files:
            if dumb == True:
                output = 'NO'
            elif dumb == False:
                output = subprocess.run(['fileicon', 'test', file], capture_output=True).stdout.decode('utf8')

            if 'NO' in output:
                filename, file_ext = os.path.splitext(file)
                
                if filename in mapper_dict:
                    replace_icon(root=root, path=file, key=filename)

                if file_ext in mapper_dict:
                    replace_icon(root=root, path=file, key=file_ext)

def replace_specified_icons(specified_types, dumb=False):
    for root, dirs, files in os.walk(root_path, topdown=True):
        for dir in dirs:
            if dir in specified_types and dir in mapper_dict:
                replace_icon(root=root, path=dir, key=dir)
        
        dirs[:] = [d for d in dirs if d not in ignorelist]
        files[:] = [f for f in files if f in specified_types]
        
        for file in files:
            if dumb == True:
                output = 'NO'
            elif dumb == False:
                output = subprocess.run(['fileicon', 'test', file], capture_output=True).stdout.decode('utf8')

            if 'NO' in output:
                filename, file_ext = os.path.splitext(file)
                
                if filename in mapper_dict:
                    replace_icon(root=root, path=file, key=filename)

                if file_ext in mapper_dict:
                    replace_icon(root=root, path=file, key=file_ext)

def main(specified_types=None, dumb=False):
    if specified_types is None:
        replace_all_icons(dumb=dumb)
        print('running base case')
    elif specified_types is not None:
        replace_specified_icons(args.specified_types, dumb=dumb)
        print('running specific case')

if __name__ == '__main__':
    main(specified_types=args.specified_types, dumb=args.dumb)




