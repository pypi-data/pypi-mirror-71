#!/usr/bin/env python3
#
# vamostool
#
# written by Christian Vogelgsang (chris@vogelgsang.org)

import sys
import os

from amitools.vamos.tools import *


def main():
    cfg_files = (
        # first look in current dir
        os.path.join(os.getcwd(), ".vamosrc"),
        # then in home dir
        os.path.expanduser("~/.vamosrc"),
    )
    tools = [PathTool(), TypeTool(), LibProfilerTool()]
    sys.exit(tools_main(tools, cfg_files))


if __name__ == "__main__":
    sys.exit(main())
