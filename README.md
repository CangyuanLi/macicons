Unfortunately, outside of weird plist modifications, Mac does not currently support associating a file type with an icon other than the default one. There is an excellent command line tool found here https://github.com/mklement0/fileicon, which this project relies on, that can change the icon of a file. This is simply a wrapper around that, that loops through all your (desired) files.

# Usage:

## Requirements

A valid Python 3 installation.

## Installing

The easiest way is to install macicons from PyPI using pip:

```
pip install macicons
```

## Running

After installation, a macicons command should be exposed to anywhere on the command line.

```
macicons {start_directory}
```

will then begin from your specified start directory, defaulting to your home directory if not specified. By default, .git, venv, and node_modules are ignored, since they may contain a large number of files and slow down the script. In the future, a command to add directories to the ignorelist will be added.

# TODO:

* Allow custom ignorelist
* Allow custom file icons