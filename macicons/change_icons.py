# Imports

import concurrent.futures
import functools
import json
import os
from pathlib import Path
import time

import Cocoa
import tqdm

# Globals

BASE_PATH = Path(__file__).resolve().parents[0]
ICONFOLDER = str(BASE_PATH / "icons")

# Functions


def read_mapper(path: Path = BASE_PATH):
    with open(path / "data_files/mapper.json") as f:
        mapper_dict = json.load(f)

    return mapper_dict


def read_ignorelist(path: Path = BASE_PATH):
    with open(path / "data_files/ignorelist.txt", "r") as f:
        ignorelist = {line.strip() for line in f}

    return ignorelist


def walk_directory(ignorelist: list[str], mapper_dict: dict, root_path: Path):
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


def replace_icon(
    filepath: Path,
    dumb: bool,
    nice: bool,
    mapper_dict: dict,
    iconfolder: str = ICONFOLDER,
):
    if nice is True:
        time.sleep(0.01)

    if dumb is True:
        time_since_creation = 0.0
    elif dumb is False:
        time_created = os.stat(filepath).st_birthtime
        time_since_creation = time.time() - time_created

    if time_since_creation < 90_000:  # 1 day in unix seconds + a little bit of padding
        basename = os.path.basename(filepath)
        filename, file_ext = os.path.splitext(basename)

        if file_ext in mapper_dict:
            iconpath = os.path.join(iconfolder, mapper_dict[file_ext])
        elif filename in mapper_dict:
            iconpath = os.path.join(iconfolder, mapper_dict[filename])
        else:
            return 0

        image = Cocoa.NSImage.alloc().initWithContentsOfFile_(iconpath)
        Cocoa.NSWorkspace.sharedWorkspace().setIcon_forFile_options_(
            image, str(filepath), 0
        )
        # ValueError: NSInvalidArgumentException - -[__NSCFArray objectAtIndex:]: index (1196314760) beyond bounds (52)

        return 1

    return 0


def replace_all_icons(filelist: list[str], mapper_dict: dict, dumb: bool, nice: bool):
    func = functools.partial(
        replace_icon, mapper_dict=mapper_dict, dumb=dumb, nice=nice
    )

    with tqdm.tqdm(total=len(filelist)) as pbar:
        with concurrent.futures.ThreadPoolExecutor() as pool:
            futures = [pool.submit(func, file) for file in filelist]

            total_changed = 0
            for future in concurrent.futures.as_completed(futures):
                total_changed += future.result()
                pbar.update(1)

    for f in filelist:
        func(f)

    return len(filelist), total_changed


def display_time(seconds):
    m, s = divmod(seconds, 60)
    h, m = divmod(m, 60)

    return f"{h} hours, {m} minutes, and {s:.2f} seconds"


# Main


def newicons(rootpath: Path, dumb: bool, nice: bool):
    start = time.perf_counter()

    if nice is True:
        os.nice(19)

    mapper_dict = read_mapper()
    ignorelist = read_ignorelist()
    lst = walk_directory(
        ignorelist=ignorelist, mapper_dict=mapper_dict, root_path=rootpath
    )
    numfiles, num_changed = replace_all_icons(
        filelist=lst, mapper_dict=mapper_dict, dumb=dumb, nice=nice
    )

    end = time.perf_counter()
    print(
        f"Visited {numfiles} files and made {num_changed} changes in {display_time(end - start)}."
    )
