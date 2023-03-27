# Imports

import concurrent.futures
import functools
import json
import os
from pathlib import Path
import time
import threading

import Cocoa
import tqdm

# Globals

BASE_PATH = Path(__file__).resolve().parents[1] / "macicons"
ICONFOLDER = BASE_PATH / "icons"

# Functions


def read_mapper(path: Path = BASE_PATH) -> dict[str, str]:
    with open(path / "data_files/mapper.json") as f:
        mapper_dict: dict = json.load(f)

    return mapper_dict


def read_ignorelist(path: Path = BASE_PATH) -> set[str]:
    with open(path / "data_files/ignorelist.txt", "r") as f:
        ignorelist = {line.strip() for line in f}

    return ignorelist


def initialize_images(mapper: dict, iconfolder: Path) -> dict:
    final_mapper = dict()
    for file_ext, icon_name in mapper.items():
        iconpath = iconfolder / icon_name
        final_mapper[file_ext] = Cocoa.NSImage.alloc().initWithContentsOfFile_(
            str(iconpath)
        )

    return final_mapper


def walk_directory(ignorelist: set[str], mapper_dict: dict, root_path: Path):
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
            image = mapper_dict[file_ext]
        elif filename in mapper_dict:
            image = mapper_dict[filename]
        else:
            return 0

        try:
            Cocoa.NSWorkspace.sharedWorkspace().setIcon_forFile_options_(
                image, str(filepath), 0
            )
        except ValueError:
            print(filepath)

        return 1

    return 0


def replace_all_icons(filelist: list[str], mapper_dict: dict, dumb: bool, nice: bool):
    func = functools.partial(
        replace_icon, mapper_dict=mapper_dict, dumb=dumb, nice=nice
    )

    # TODO: Fix multi-threaded version
    with tqdm.tqdm(total=len(filelist)) as pbar:
        with concurrent.futures.ThreadPoolExecutor(8) as pool:
            futures = [pool.submit(func, file) for file in filelist]

            total_changed = 0
            for future in concurrent.futures.as_completed(futures):
                total_changed += future.result()
                pbar.update(1)

    # total_changed = 0
    # for f in tqdm.tqdm(filelist):
    #     total_changed += func(f)

    return len(filelist), total_changed


def display_time(seconds):
    m, s = divmod(seconds, 60)
    h, m = divmod(m, 60)

    return f"{h} hours, {m} minutes, and {s:.2f} seconds"


# Main


def newicons(rootpath: Path, dumb: bool, nice: bool):
    start = time.perf_counter()

    if nice:
        os.nice(19)

    mapper_dict = initialize_images(read_mapper(), iconfolder=ICONFOLDER)
    ignorelist = read_ignorelist()
    lst = walk_directory(
        ignorelist=ignorelist, mapper_dict=mapper_dict, root_path=rootpath
    )
    # lst = lst[160:168]  # 160:170
    # print(lst)
    numfiles, num_changed = replace_all_icons(
        filelist=lst, mapper_dict=mapper_dict, dumb=dumb, nice=nice
    )

    end = time.perf_counter()
    print(
        f"Visited {numfiles} files and made {num_changed} changes in {display_time(end - start)}."
    )


def main():
    newicons("/users/cangyuanli/Documents/", dumb=True, nice=False)


if __name__ == "__main__":
    main()
