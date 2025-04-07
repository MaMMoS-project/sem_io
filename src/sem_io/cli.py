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

"""Command line interface definition."""

import argparse
import glob
from pathlib import Path

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
    d_0 = "Prints and/or stores various parameters from the header of an SEM image."
    parser = argparse.ArgumentParser(description=d_0)

    path_help = (
        "full path(s) to any number of single .tif image(s) or "
        "folder(s) containing several .tif images. The images must "
        "have been produced by either the Zeiss SmartSEM or the "
        "Thermo Fisher Scientific xT software. In the case of folders, "
        "all the .tif images within each folder will be processed."
    )
    parser.add_argument("image_path", nargs="+", help=path_help)

    parser.add_argument(
        "-v", "--version", action="version", version=f"%(prog)s {__version__}"
    )
    dump_help = (
        "dump selected image metadata to json. One json file per image "
        "will be stored in the same directory as the image. "
        "The name of each json file is the corresponding image name "
        "(without the .tif extension) plus _metadata.json"
    )
    parser.add_argument(
        "-d",
        "--dump",
        action="store_true",
        help=dump_help,
    )

    parser.add_argument(
        "-s",
        "--silent",
        action="store_true",
        help="do not print output to terminal",
    )

    args = parser.parse_args()

    verbose = not args.silent

    if args.silent and not args.dump:
        err_msg = (
            "Printing and saving both suppressed (-s but no -d): " "nothing to do."
        )
        parser.error(err_msg)

    for p_img in args.image_path:
        p_img = Path(p_img)
        if p_img.is_file():
            s_p = SEMparams(p_img, verbose=verbose)
            if args.dump:
                fn = p_img.parent.joinpath(p_img.stem + "_metadata.json")
                s_p.dump_params_to_json(s_p.params_grouped, fn, image_path=None)
        else:
            all_tifs = glob.glob(p_img.joinpath("*.tif").as_posix())
            for i in all_tifs:
                s_p = SEMparams(i, verbose=verbose)
                if args.dump:
                    fn = s_p.img_path.parent.joinpath(
                        s_p.img_path.stem + "_metadata.json"
                    )
                    s_p.dump_params_to_json(s_p.params_grouped, fn, image_path=None)
