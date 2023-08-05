# amitools - various AmigaOS tools for other platforms

- written by Christian Vogelgsang <chris@vogelgsang.org>
- under the GNU Public License V2

## Introduction

`amitools` is a collection of Python 3 tools that I've written to work with
*Amiga OS* binaries and files on Mac OS X and all other *nix-like platforms
supporting Python. Windows might work as
well, but is heavily untested. However, patches are welcome.

I focus with my tools on classic Amiga setups, i.e. a 680x0 based system with
Amiga OS 1.x - 3.x running on it. However, this is an open project, so you can
provide other Amiga support, too.

The tools are mostly developer-oriented, so a background in Amiga programming
will be very helpful.

## Prerequisites

- Python >= ```3.5```
- pip

### Optional Packages

- [lhafile - FS Edition][1]: required to use ```.lha``` file scanner
- [cython][7]: (version >= **0.25**) required to rebuild the native module

### Install pip

First make sure to have the Python package installer ```pip```:

#### macOS

On macOS you have multiple ways of installing ```pip```:

#### System Python

```bash
sudo easy_install pip
```

#### Homebrew Package Manager

With the [Homebrew][3] package manager (```pip``` is included in the ```python3``` package):

```bash
brew install python
```

#### Linux/Ubuntu

On Linux Ubuntu use the provided packages ```python-pip```

```bash
sudo apt-get install python-pip
```

#### Centos

To get pip run:

```bash
curl "https://bootstrap.pypa.io/get-pip.py" -o "get-pip.py"
python get-pip.py
```

#### Windows with Visual Studio

- Install the latest native Windows Python >= 3.4 from [python.org][6]
- There is a special Edition for Visual Studio available that allows
  to compile Python 3.x modules: Install [VCpython3][5]
- Open the Command Shell of the Compiler and run

```bash
cd C:\Python3x\Scripts
pip install amitools
```

#### Windows with MSYS2

- (I use the mingw gcc compiler here to build the extension)
- On Windows with [MSYS2][4] (use x86_64 version if possible):
  - Install with exe installer
  - Initial update is done with: (Open shell first)

```bash
pacman -Sy
pacman --needed -S bash pacman msys2-runtime
```

- Now close shell and re-open a new dev shell (```MinGW-w64 Win64 Shell```)

```bash
pacman -Su
pacman -S mingw-w64-x86_64-python2-pip mingw-w64-x86_64-gcc git make
```

[1]: https://github.com/FrodeSolheim/python-lhafile
[2]: https://www.macports.org
[3]: https://brew.sh
[4]: https://github.com/msys2/msys2/wiki
[5]: https://www.microsoft.com/en-gb/download/details.aspx?id=44266
[6]: https://www.python.org
[7]: https://cython.org

## Installation

### The Easy Way for Users

```bash
pip install amitools
```

Note:

- on Linux/macOS may use ``sudo`` to install for all users
- requires a host C compiler to compile the extension.

### Developers

- Follow this route if you want to hack around with the amitools codebase
- Clone the Git repo: [amitools@git](https://github.com/cnvogelg/amitools)
- Ensure to have Cython (version >= **0.25**) installed:

```bash
sudo pip install cython
```

You have multiple variants to install the tools with Python's `setuptools`:

- **Global Install** is available for all users of your system and needs root privileges

```bash
sudo python setup.py install
```

- **User Install** is available for your user only but does not require special privileges

```bash
python setup.py install --user
```

- **Developer Setup** only links this code into your installation and allows
   you to change/develop the code and test it immediately. (I prefer user install here)

```bash
python setup.py develop --user
```

- **Run In Place** allows you to run the binaries directly from the `bin` directory
   without any installation. You need `make` only to build the native library
   of vamos:

```bash
python setup.py build_ext -i
```

or if you have installed `GNU make` simply use:

```bash
make
```

## Contents

The new Documentation of `amitools` is hosted on [readthedocs][8]

### Tools

- [vamos](docs/vamos.md) **V)irtual AM)iga OS**

  vamos allows you to run command line (CLI) Amiga programs on your host
  Mac or PC. vamos is an API level Amiga OS Emulator that replaces exec
  and dos calls with its own implementation and maps all file access to
  your local file system.

- [xdftool][9]

  Create and modify ADF or HDF disk image files.

- [xdfscan][10]

  Scan directory trees for ADF or HDF disk image files and verify the contents.

- [rdbtool][11]

  Create or modify disk images with Rigid Disk Block (RDB)

- [romtool][12]

  A tool to inspect, dissect, and build Amiga Kickstart ROM images to be
  used with emulators, run with soft kickers or burned into flash ROMs.

- hunktool

  The hunktool uses amitools' hunk library to load a hunk-based amiga
  binary. Currently, its main purpose is to display the contents of the
  files in various formats.

  You can load hunk-based binaries, libraries, and object files. Even
  overlayed binary files are supporte.

- typetool

  This little tool is a companion for vamos. It allows you to dump and get
  further information on the API C structure of AmigaOS used in vamos.

- fdtool

  This tool reads the fd (function description) files Commodore supplied for
  all of their libraries and dumps their contents in different formats
  including a code structure used in vamos.

  You can query functions and find their jump table offset.

[8]: https://amitools.readthedocs.io/
[9]: https://amitools.readthedocs.io/en/latest/tools/xdftool.html
[10]: https://amitools.readthedocs.io/en/latest/tools/xdfscan.html
[11]: https://amitools.readthedocs.io/en/latest/tools/rdbtool.html
[12]: https://amitools.readthedocs.io/en/latest/tools/romtool.html

### Python Libraries

- Hunk library ```amitools.binfmt.hunk```

  This library allows to read Amiga OS loadSeg()able binaries and represent
  them in a python structure. You could query all items found there,
  retrieve the code, data, and bss segments and even relocate them to target
  addresses

- ELF library ```amitools.binfmt.elf```

  This library allows to read a subset of the ELF format mainly used in
  AROS m68k.

- .fd File Parser ```amitools.fd```

  Parse function descriptions shipped by Commodore to describe the Amiga APIs

- OFS and FFS File System Tools ```amitools.fs```

  Create or modify Amiga's OFS and FFS file system structures

- File Scanners ```amitools.scan```

  I've written some scanners that walk through file trees and retrieve the
  file data for further processing. I support file trees on the file system,
  in lha archives or in adf/hdf disk images
