import json
import os
from pathlib import Path
import statistics
import subprocess
import time

# start = time.time()

# base_path = Path(__file__).parent
# iconfolder = str(base_path / 'icons')
# root_path = '/Users/cangyuanli/Documents/'

# with open(base_path / 'mapper.json') as f:
#     mapper_dict = json.load(f)

# with open(base_path / 'ignorelist.txt', 'r') as f:
#     ignorelist = {line.strip() for line in f}


# for root, dirs, files in os.walk(root_path, topdown=True):
#     dirs[:] = [d for d in dirs if d not in ignorelist]

#     for dir in dirs:
#         if dir in mapper_dict: # faster then mapper_dict.keys()
#             dirpath = os.path.join(root, dir)
#             iconpath = os.path.join(iconfolder, mapper_dict[dir])

#         print(dir)
    
#     dirs[:] = [d for d in dirs if not d.startswith('.')] # don't check hidden folders
    
#     for file in files:
#         filename, file_ext = os.path.splitext(file)
        
#         if filename in mapper_dict:
#             filepath = os.path.join(root, file)
#             iconpath = os.path.join(iconfolder, mapper_dict[filename])

#             print(filename)


#         if file_ext in mapper_dict:
#             filepath = os.path.join(root, file)
#             iconpath = os.path.join(iconfolder, mapper_dict[file_ext])

#             print(file_ext)

# end = time.time()

# print(f'{end - start}')


start = time.time()

base_path = Path(__file__).parent
iconfolder = str(base_path / 'icons')
root_path = '/Users/cangyuanli/Documents/'

with open(base_path / 'mapper.json') as f:
    mapper_dict = json.load(f)

with open(base_path / 'ignorelist.txt', 'r') as f:
    ignorelist = {line.strip() for line in f}


checktimes = []
for root, dirs, files in os.walk(root_path, topdown=True):
    dirs[:] = [d for d in dirs if d not in ignorelist]

    for dir in dirs:
        if dir in mapper_dict: # faster then mapper_dict.keys()
            dirpath = os.path.join(root, dir)
            iconpath = os.path.join(iconfolder, mapper_dict[dir])

            subprocess.run(['fileicon', 'set', dirpath, iconpath], stdout=subprocess.DEVNULL)
    
    dirs[:] = [d for d in dirs if not d.startswith('.')] # don't check hidden folders
    
    for file in files:
        checktimest = time.time()
        output = subprocess.run(['fileicon', 'test', file], capture_output=True).stdout.decode('utf8')
        checktimeend = time.time()

        checktimes.append(checktimeend - checktimest)

        if 'NO' in output:
            filename, file_ext = os.path.splitext(file)
            
            if filename in mapper_dict:
                filepath = os.path.join(root, file)
                iconpath = os.path.join(iconfolder, mapper_dict[filename])

                subprocess.run(['fileicon', 'set', filepath, iconpath], stdout=subprocess.DEVNULL)

            if file_ext in mapper_dict:
                filepath = os.path.join(root, file)
                iconpath = os.path.join(iconfolder, mapper_dict[file_ext])

                subprocess.run(['fileicon', 'set', filepath, iconpath], stdout=subprocess.DEVNULL)


print(statistics.mean(checktimes))

end = time.time()

print(f'{end - start}')



