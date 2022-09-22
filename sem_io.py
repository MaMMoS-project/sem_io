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

"""
This module provides some helper functions to extract and view parameters
stored in the header of SEM images (.tif) recorded using the software
Zeiss SmartSEM V06.
"""

import os
import argparse

from PIL import Image

__version__ = "0.0.1"


class SEMparams():
    """
    Class to extract and hold SEM parameters from the .tif images
    output from the software Zeiss SmartSEM V06.
    """
    PARAM_NAMES = {"val_unit" : ["Image Pixel Size =",
                                 "Stage at X =",
                                 "Stage at Y =",
                                 "Stage at Z =",
                                 "Stage at R =",
                                 "Dwell Time =",
                                 "C3 Lens I =",
                                 "Cycle Time =",
                                 "Line Time =",
                                 "Stigmation X =",
                                 "Stigmation Y =",
                                 "Aperture Size =",
                                 "Aperture at X =",
                                 "Aperture at Y =",
                                 "Beam Shift X =",
                                 "Beam Shift Y =",
                                 "Gun Vacuum =",
                                 "System Vacuum =",
                                 "WD =",
                                 "Mag =",
                                 "Brightness =",
                                 "Contrast =",
                                 "Fil I =",
                                 "EHT ="
                                 ],

                   "string" : ["File Name =",
                               "Dyn.Focus =",
                               "BSD Gain =",
                               "Detector =",
                               "Store resolution =",
                               "Tilt Corrn. =",
                               "High Current =",
                               "Line Avg.Count =",
                               "Scan Speed =",
                               "Time :",
                               "Date :"
                               ]
                   }


    GROUPS = {"General" : ["File Name", "Date", "Time"],
              "SEM" : ["Gun Vacuum", "System Vacuum", "Fil I",
                       "Tilt Corrn.", "Dyn.Focus", "High Current", "EHT"],
              "Beam" : ["Aperture Size",
                        "Aperture at X", "Aperture at Y",
                        "Stigmation X", "Stigmation Y",
                        "Beam Shift X", "Beam Shift Y",
                        "C3 Lens I"],
              "Scanning" : ["Mag", "Cycle Time", "Scan Speed",
                            "Line Time", "Dwell Time", "Line Avg.Count"],
              "Image" : ["Detector", "Store resolution", "Image Pixel Size",
                         "Brightness", "Contrast", "BSD Gain"],
              "Stage" : ["Stage at X", "Stage at Y",
                         "Stage at Z", "Stage at R", "WD"]
              }


    @staticmethod
    def dwell_time_from_scan_speed(scan_speed):
        """
        This formula is taken from the table in help of the SEM software.
        It converts the scan speed (int, 1-15) into a dwell time for
        a pixel in seconds. This is necessary currently (21.11.2016) because
        the dwell time parameter in the image header is always 100 ns and
        this is wrong - it should vary with scan speed.
        """
        return 1.0E-7 * 2**(scan_speed-1)


    @staticmethod
    def get_val(j):
        """
        Takes the string which is everything after the '=' sign or
        ':' sign in one line of the image header, separates the string
        using a space, then returns a 2-tuple of the first element as
        a float and the rest of the original string as a str.

        Parameters
        ----------
        j : STR
             everything after the '=' sign or ':' sign in one
             line of the image header

        Returns
        -------
        tuple
            The first element is a float of the value of the parameter,
            the second element is a string which should correspond
            to the unit of the parameter.

        """
        return (float(j.split(" ")[0]), j.split(j.split(" ")[0])[1].strip())


    @staticmethod
    def read_image_header(image_path):
        """
        Takes a path to an SEM image (.tif) reads it using PIL.Image
        and extracts the header data in tag 34118. Raises exceptions
        if the path does not point to a .tif image or if the tag 34118
        is missing.

        Returns a list of strings corresponding to the lines of the header.

        Parameters
        ----------
        imagePath : STR
            Full path to an SEM image (.tif) recorded with Zeiss SmartSEM V06.

        Raises
        ------
        Exception
            If the image path does not point to a .tif file.

        Exception
            If the tag 34118 is missing from the .tif file.

        Returns
        -------
        sem_img_header : LIST
            A list of strings corresponding to the lines of the image header.

        """
        if not os.path.splitext(image_path)[-1] == ".tif":
            q_0 = "The image path must point to a .tif file."
            raise Exception("".join(["sem_io:", q_0])) from None

        try:
            with Image.open(image_path) as sem_img:
                sem_img_header = sem_img.tag[34118][0].split("\r\n")
        except KeyError:
            q_0 = "The image does not appear to be from the SmartSEM software"
            q_1 = ": Missing Tag 34118"
            raise Exception("".join(["sem_io: ", q_0, q_1])) from None

        return sem_img_header


    @staticmethod
    def extract_params(image_path):
        """
        Takes a path to an SEM image (.tif) reads it using PIL.Image
        and extracts the various useful parameters which are stored in
        the image header including: file name, stage X, Y, Z and R positions
        and the pixel size.

        The parameters extracted are defined in SEMparams.PARAM_NAMES

        The values extracted are returned as a dict.

        Parameters
        ----------
        imagePath : STR
            Full path to an SEM image (.tif) recorded with Zeiss SmartSEM V06.

        Returns
        -------
        params : DICT
            A dict where the keys are the names of the parameters and the
            values are either 2-tuples containing the value of the parameter
            and if applicable, the unit; or a string containing the parameter.

        """
        sem_img_header = SEMparams.read_image_header(image_path)

        params = {}
        v_u = list(SEMparams.PARAM_NAMES["val_unit"])
        strg = list(SEMparams.PARAM_NAMES["string"])


        while sum([len(g) for g in [v_u, strg]]) > 0:
            for i in sem_img_header:
                for nom in v_u:
                    if i[:len(nom)] == nom:
                        j = i[len(nom):].strip()
                        params[nom[:-2]] = SEMparams.get_val(j)
                        v_u.remove(nom)
                        break

                for nom in strg:
                    if i[:len(nom)] == nom:
                        params[nom[:-2]] = i[len(nom):].strip()
                        strg.remove(nom)
                        break

        s_sp = int(params["Scan Speed"][0])
        params["Dwell Time"] = (SEMparams.dwell_time_from_scan_speed(s_sp), 's')

        return params


    @staticmethod
    def get_image_pixel_size(image_path):
        """
        Bespoke method to get the value of the image pixel size
        and the corresponding unit from the header of an SEM image.

        Takes a path to an SEM image (.tif) reads it using PIL.Image
        and extracts the pixel size.

        Parameters
        ----------
        imagePath : STR
            Full path to an SEM image (.tif) recorded with Zeiss SmartSEM V06.

        Returns
        -------
        img_pix_size : TUPLE
            A 2-tuple containing the value of the image pixel size as
            a float and the unit as a string.

        """
        sem_img_header = SEMparams.read_image_header(image_path)

        nom = "Image Pixel Size ="

        for i in sem_img_header:
            if i[:len(nom)] == nom:
                j = i[len(nom):].strip()
                img_pix_size = SEMparams.get_val(j)
                break

        return img_pix_size


    @staticmethod
    def group_parameters(params):
        """
        Take the unsorted dict of the parameters extracted from the
        image header using extract_params() and group them according
        to the scheme defined in GROUPS. Return a dict of dict containing
        the grouped parameters.

        Parameters
        ----------
        params : DICT
            A dict of parameters extracted from an SEM image

        Returns
        -------
        params_grouped : DICT
            A dict of dicts containing the parameters grouped according
            to the scheme defined in GROUPS.

        """
        params_grouped = {key : {k : None for k in value} for (key, value) in
                          SEMparams.GROUPS.items()}

        for k in params_grouped:
            for j in params_grouped[k]:
                params_grouped[k][j] = params[j]

        return params_grouped


    @staticmethod
    def print_params(params_grouped):
        """
        Print all params in groups.
        """
        for i in params_grouped:
            print(i+" parameters:")
            for j in params_grouped[i]:
                print("\t"+j+" =", end=' ')
                if isinstance(params_grouped[i][j], str):
                    print(params_grouped[i][j], end=' ')
                else:
                    for k in enumerate(params_grouped[i][j]):
                        print(k[1], end=' ')
                print()
            print()



    def __init__(self, image_path, verbose=True):
        """
        Initialise with the path to a .tif image from the
        Zeiss SmartSEM V06 software.
        """
        self.image_path = image_path
        self.params = SEMparams.extract_params(self.image_path)

        try:
            self.params_grouped = SEMparams.group_parameters(self.params)
            if verbose:
                print("\nParameters extracted from the SEM image:")
                print(self.image_path+"\n")
                SEMparams.print_params(self.params_grouped)

        except KeyError:
            print("**Some parameters not found.**")
            print("Image: "+self.image_path)
            print("Printing those found (not ordered):")
            for i, j in self.params.items():
                print(i+" =", end=' ')
                if isinstance(j, str):
                    print(j, end=' ')
                else:
                    for k in enumerate(j):
                        print(k[1], end=' ')
                print()


    def get_parameter(self, name):
        """
        Return a single parameter with its unit, if applicable.
        """
        return self.params[name]


def main():
    """
    Command line entry point.

    Calling "sem_io filename" at the command line, where "filename" is
    the full path to an SEM image recorded with Zeiss SmartSEM V06,
    instantiates the SEMparams class and prints the parameters extracted
    from the image header to the terminal.

    Returns
    -------
    None.

    """
    d_0 = "Prints various parameters from the header of an SEM image"
    parser = argparse.ArgumentParser(description=d_0)
    q_0 = "full path to a .tif image produced by the Zeiss SmartSEM software"
    parser.add_argument("image_path", help=q_0)
    parser.add_argument('-v', '--version', action='version',
                        version=f'%(prog)s {__version__}')
    args = parser.parse_args()
    SEMparams(args.image_path)
