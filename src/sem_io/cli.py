##MIT License
##
##Copyright (c) 2022 Thomas G. Woodcock
##
##Permission is hereby granted, free of charge, to any person obtaining a copy
##of this software and associated documentation files (the "Software"), to deal
##in the Software without restriction, including without limitation the rights
##to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
##copies of the Software, and to permit persons to whom the Software is
##furnished to do so, subject to the following conditions:
##
##The above copyright notice and this permission notice shall be included in all
##copies or substantial portions of the Software.
##
##THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
##IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
##FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
##AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
##LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
##OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
##SOFTWARE.

"""Command line interface."""

import argparse

from sem_io import __version__
from sem_io.metadata_extractor import SEMparams


def cli():
    """
    Command line interface.

    Calling "sem_io filename" at the command line, where "filename" is
    the full path to an SEM image recorded either with Zeiss SmartSEM
    or with Thermo Fisher Scientific xT, uses the SEMparams class to
    print the parameters extracted from the image header to the terminal.
    """
    d_0 = "Prints various parameters from the header of an SEM image"
    parser = argparse.ArgumentParser(description=d_0)
    q_0 = "full path to a .tif image produced by either the Zeiss SmartSEM"
    q_1 = " or the Thermo Fisher Scientific xT software"
    parser.add_argument("image_path", help=q_0 + q_1)
    parser.add_argument(
        "-v", "--version", action="version", version=f"%(prog)s {__version__}"
    )
    args = parser.parse_args()
    SEMparams(args.image_path)
