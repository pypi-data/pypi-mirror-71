#!/usr/bin/env python3
#
# vamospath [options] <path>
#
# a tool to convert between AmigaOS and native paths
#

import sys
import os

from amitools.vamos.tools import tools_main, PathTool


def main():
    cfg_files = (
        # first look in current dir
        os.path.join(os.getcwd(), ".vamosrc"),
        # then in home dir
        os.path.expanduser("~/.vamosrc"),
    )
    tools = [PathTool()]
    sys.exit(tools_main(tools, cfg_files))


if __name__ == "__main__":
    sys.exit(main())
