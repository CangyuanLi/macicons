import os
from pathlib import Path
import subprocess
import time
import timeit

import Cocoa
import cutils

BASE_PATH = Path(__file__).resolve().parents[1]

def set_icon():
    subprocess.run(
        ["fileicon", "set", BASE_PATH / "setup.py", BASE_PATH / "macicons/icons/python.png"], 
        stdout=subprocess.DEVNULL
    )

def check_icon():
    subprocess.run(
        ["fileicon", "test", BASE_PATH / "setup.py"], 
        stdout=subprocess.DEVNULL
    )

def set_icon_cocoa():
    filepath = str(BASE_PATH / "macicons/icons/python.png")
    _set = str(BASE_PATH / "setup.py")
    image = Cocoa.NSImage.alloc().initWithContentsOfFile_(filepath)
    Cocoa.NSWorkspace.sharedWorkspace().setIcon_forFile_options_(image, _set, 0)

def check_time():
    time_created = os.stat(BASE_PATH / "setup.py").st_birthtime
    time_since_creation = time.time() - time_created

def main():
    cutils.time_func(set_icon_cocoa, iterations=20)
    cutils.time_func(set_icon, iterations=20)
    # cutils.time_func(check_icon, iterations=20)
    # cutils.time_func(check_time, iterations=20)


if __name__ == "__main__":
    main()
