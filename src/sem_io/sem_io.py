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
stored in the header of SEM images (.tif) recorded using either the software
Zeiss SmartSEM or the software Thermo Fisher Scientific xT.
"""

import os
import argparse
import json
import math

from PIL import Image

__version__ = "0.1.0"


class SEMparams():
    """
    Class to extract and hold SEM parameters from the header of
    a .tif image output from either the software Zeiss SmartSEM
    or the software Thermo Fisher Scientific xT.
    """
    TAGS = {"Zeiss" : 34118,
            "ThermoFisher" : 34682
            }

    ZEISS_PARAM_LOCS = {'Dwell Time': 'DP',
                        'Dyn.Focus': 'DP',
                        'BSD Gain': 'DP',
                        'Detector': 'DP',
                        'Store resolution': 'DP',
                        'Tilt Corrn.': 'DP',
                        'High Current': 'DP',
                        'Scan Speed': 'DP',
                        'Image Pixel Size': 'AP',
                        'Stage at X': 'AP',
                        'Stage at Y': 'AP',
                        'Stage at Z': 'AP',
                        'Stage at R': 'AP',
                        'C3 Lens I': 'AP',
                        'Cycle Time': 'AP',
                        'Line Time': 'AP',
                        'Stigmation X': 'AP',
                        'Stigmation Y': 'AP',
                        'Aperture Size': 'AP',
                        'Aperture at X': 'AP',
                        'Aperture at Y': 'AP',
                        'Beam Shift X': 'AP',
                        'Beam Shift Y': 'AP',
                        'Gun Vacuum': 'AP',
                        'System Vacuum': 'AP',
                        'WD': 'AP',
                        'Mag': 'AP',
                        'Brightness': 'AP',
                        'Contrast': 'AP',
                        'Fil I': 'AP',
                        'EHT': 'AP',
                        'Line Avg.Count': 'AP',
                        'Time': 'AP',
                        'Date': 'AP',
                        'File Name': 'SV'
                        }



    ZEISS_GROUPS = {"General" : ["File Name", "Date", "Time"],
                    "SEM" : ["Gun Vacuum", "System Vacuum", "Fil I",
                             "Tilt Corrn.", "Dyn.Focus", "High Current", "EHT"
                             ],
                    "Beam" : ["Aperture Size",
                              "Aperture at X", "Aperture at Y",
                              "Stigmation X", "Stigmation Y",
                              "Beam Shift X", "Beam Shift Y",
                              "C3 Lens I"
                              ],
                    "Scanning" : ["Mag", "Cycle Time", "Scan Speed",
                                  "Line Time", "Dwell Time", "Line Avg.Count"
                                  ],
                    "Image" : ["Detector", "Store resolution", "Image Pixel Size",
                               "Brightness", "Contrast", "BSD Gain"
                               ],
                    "Stage" : ["Stage at X", "Stage at Y",
                               "Stage at Z", "Stage at R", "WD"
                               ]
                    }


    TF_PARAM_LOCS = {'Date' : "[User]",
                     'Time' : "[User]",
                     'User' : "[User]",
                     'SystemType' : "[System]",
                     'HV' : '[Beam]',
                     'Spot' : '[Beam]',
                     'StigmatorX' : '[Beam]',
                     'StigmatorY' : '[Beam]',
                     'BeamShiftX' : '[Beam]',
                     'BeamShiftY' : '[Beam]',
                     'ScanRotation' : '[Beam]',
                     'ApertureDiameter' : '[EBeam]',
                     'HFW' : '[EBeam]',
                     'VFW' : '[EBeam]',
                     'WD' : '[EBeam]',
                     'BeamCurrent' : '[EBeam]',
                     'TiltCorrectionIsOn' : '[EBeam]',
                     'DynamicFocusIsOn' : '[EBeam]',
                     'UseCase' : '[EBeam]',
                     'SourceTiltX' : '[EBeam]',
                     'SourceTiltY' : '[EBeam]',
                     'StageX' : '[EBeam]',
                     'StageY' : '[EBeam]',
                     'StageZ' : '[EBeam]',
                     'StageR' : '[EBeam]',
                     'StageTa' : '[EBeam]',
                     'EmissionCurrent' : '[EBeam]',
                     'TiltCorrectionAngle' : '[EBeam]',
                     'PreTilt' : '[EBeam]',
                     'AngularFieldWidth' : '[EBeam]',
                     'AngularPixelWidth' : '[EBeam]',
                     'ElectronChannelingPatternIsOn' : '[EBeam]',
                     'ModeOn' : '[EBeamDeceleration]',
                     'LandingEnergy' : '[EBeamDeceleration]',
                     'ImmersionRatio' : '[EBeamDeceleration]',
                     'StageBias' : '[EBeamDeceleration]',
                     'Dwelltime' : '[Scan]',
                     'PixelWidth' : '[Scan]',
                     'Average' : '[Scan]',
                     'Integrate' : '[Scan]',
                     'FrameTime' : '[Scan]',
                     'LineTime' : '[EScan]',
                     'SpecTilt' : '[Stage]',
                     'ResolutionX' : '[Image]',
                     'ResolutionY' : '[Image]',
                     'ChPressure' : '[Vacuum]',
                     'SpecimenCurrent' : '[Specimen]',
                     'Number' : '[Detectors]',
                     'Name' : '[Detectors]',
                     'Mode' : '[Detectors]',
                     'Contrast' : '#spec#',
                     'Brightness' : '#spec#',
                     'Signal' : '#spec#',
                     'Setting' : '#spec#',
                     'MinimumDwellTime' : '#spec#',
                     'DataBarSelected' : '[PrivateFei]',
                     'DatabarHeight' : '[PrivateFei]'
                     }

    TF_GROUPS = {"General" : ["Date", "Time", "User", "SystemType"],
                 "SEM" : ["HV", "ChPressure", "EmissionCurrent"],
                 "Beam" : ["ApertureDiameter", "Spot", "BeamCurrent",
                           "SpecimenCurrent",
                           "StigmatorX", "StigmatorY",
                           "BeamShiftX", "BeamShiftY", "UseCase",
                           "SourceTiltX", "SourceTiltY"
                           ],
                 "Beam Deceleration" : ["ModeOn", "LandingEnergy",
                                        "ImmersionRatio", "StageBias"],
                 "Scanning" : ["FrameTime", "LineTime",
                               "Dwelltime", "Average", "Integrate",
                               "ScanRotation", "TiltCorrectionIsOn",
                               "TiltCorrectionAngle", "DynamicFocusIsOn",
                               "PreTilt", "SpecTilt", "MinimumDwellTime"
                               ],
                 "Detector" : ["Number", "Name", "Mode",
                               "Contrast", "Brightness", "Signal",
                               "Setting"
                               ],
                 "Image" : ["ResolutionX", "ResolutionY", "PixelWidth",
                            "HFW", "VFW", "ElectronChannelingPatternIsOn",
                            "AngularPixelWidth", "AngularFieldWidth",
                            "DataBarSelected", "DatabarHeight"
                            ],
                 "Stage" : ["StageX", "StageY", "StageZ", "StageR",
                            "StageTa", "WD"
                            ]
                 }


    @staticmethod
    def dwell_time_from_scan_speed(scan_speed):
        """
        Calculates a dwell time in seconds from the scan speed
        used to acquire the image.

        Relevant for Zeiss SmartSEM image headers.

        This formula is taken from the table in help of the
        Zeiss SmartSEM software. It converts the scan speed (int, 1-15)
        into a dwell time of the beam on a pixel in seconds.
        This is necessary currently (21.11.2016) because the dwell
        time parameter in the image header is always 100 ns and
        this is wrong - it should vary with scan speed.


        Parameters
        ----------
        scan_speed : INT
            The scan speed (1-15) which was used to acquire the
            image.

        Returns
        -------
        FLOAT
            The calculated dwell time in seconds.

        """
        return 1.0E-7 * 2**(scan_speed-1)


    @staticmethod
    def get_val(j):
        """
        Takes the string which is everything after the '=' sign or
        ':' sign in one line of the image header, separates the string
        using a space, then returns a 2-tuple of the first element as
        a float and the rest of the original string as a str.

        Relevant for Zeiss SmartSEM image headers.


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
    def get_image_type_and_header(image_path):
        """
        Checks that the image_path points to a .tif file and
        raises an exception if not. Then looks for the tags
        34118 and 34682 in the file and returns a string
        specifying if the image was generated using the software
        from Zeiss (tag 34118) or Thermo Fisher Scientific
        (tag 34682). The image header string under the corresponding
        tag is also returned. Raises an exception if neither tag is
        found, or if both tags are found.


        Parameters
        ----------
        imagePath : STR
            Full path to an SEM image (.tif) recorded with either
            Zeiss SmartSEM V06 or Thermo Fisher Scientific xT.

        Raises
        ------
        Exception
            If the image path does not point to a .tif file.

        Exception
            If both tags 34118 and 34682 are missing from the .tif file,
            indicating that it was not generated by either Zeiss
            SmartSEM or by Thermo Fisher Scientific xT.

        Exception
            If both tags 34118 and 34682 are present in the .tif file,
            the image type is indeterminate.

        Returns
        -------
        img_type : str
            Either "Zeiss" or "ThermoFisher" indicating from which
            manufacturer the image stems.
        img_header : str
            String containing the data from the image header.

        """
        if not os.path.splitext(image_path)[-1] == ".tif":
            q_0 = "The image path must point to a .tif file."
            raise Exception("".join(["sem_io:", q_0])) from None

        n_matches = 0
        with Image.open(image_path) as sem_img:
            for t, v in SEMparams.TAGS.items():
                if v in sem_img.tag:
                    img_type = t
                    img_header = sem_img.tag[v][0].strip()
                    n_matches += 1

        if n_matches == 0:
            q_0 = "The image does not appear to be from either"
            q_1 = " or ".join(SEMparams.TAGS.keys()) + " software. Missing tags"
            q_2 = " and ".join(str(i) for i in SEMparams.TAGS.values()) + "."
            raise Exception(" ".join(["sem_io:", q_0, q_1, q_2])) from None

        if n_matches > 1:
            q_0 = f"Unclear image type: {n_matches} of tags"
            q_1 = " and ".join(str(i) for i in SEMparams.TAGS.values())
            q_2 = "are present in this file."
            raise Exception(" ".join(["sem_io:", q_0, q_1, q_2])) from None

        return img_type, img_header


    @staticmethod
    def extract_params_Zeiss(image_header):
        """
        Extracts all parameters stored in the header of images
        produced using the Zeiss SmartSEM software. The parameters
        are returned as a dict which contains the keys "DP", "AP" and
        "SV", under which the parameters are grouped as further dicts.
        In the sub-dicts, the key is a string giving the parameter name
        and the value is a the parameter string. This can either be
        a value and a unit or a text string.

        Parameters
        ----------
        image_header : STR
            Str containing the image header read from tag 34118 of
            a .tif file from the Zeiss SmartSEM software.

        Returns
        -------
        params : DICT
            a dict which contains the keys "DP", "AP" and
            "SV", under which the parameters are grouped as further dicts.
            In the sub-dicts, the key is a string giving the parameter name
            and the value is the parameter string. This can either be
            a value and a unit or a text string.

        """
        img_hdr = image_header.split("\r\n")

        idx = [i for i, item in enumerate(img_hdr[:-1]) if item[0].isalpha()][0]

        locs = range(idx+1, len(img_hdr), 2)

        params = {"DP" : {}, "AP" : {}, "SV" : {}}
        for i in locs:
            t = img_hdr[i].find("=")
            if t != -1:
                k, v = img_hdr[i].split("=")
                grp = img_hdr[i - 1][:2]
                params[grp][k.strip()] = v.strip()
            else:
                t = img_hdr[i].find(":")
                if t != -1:
                    k = img_hdr[i][:t]
                    v = img_hdr[i][t + 1:]
                    grp = img_hdr[i - 1][:2]
                    params[grp][k.strip()] = v.strip()


        s_sp = int(params["DP"]["Scan Speed"])
        dw_t = SEMparams.dwell_time_from_scan_speed(s_sp)
        params["DP"]["Dwell Time"] = f"{dw_t:.5e} s"

        if "V05" in params["SV"]["Version"]:
            pix_size = params["AP"].pop("Pixel Size")
            params["AP"]["Image Pixel Size"] = pix_size

        return params


    @staticmethod
    def extract_params_ThermoFisher(image_header):
        """
        Extracts all parameters stored in the header of images
        produced using the ThermoFisher xT software. The parameters
        are returned as a dict whose keys represent various groups.
        Under the group keys, the parameters are stored as further
        dicts. In the sub-dicts, the key is a string giving the
        parameter name and the value is a the parameter string.
        This can either be a value (no units are given in the
        header but the values appear to correspond to SI units)
        or a text string.

        Note: currently (26/09/2023 with software version 23.3.1.22195)
        the groups following [HiResIllumination] are not properly
        separated with a double space: "\r\n\r\n". THis appears
        to be a bug in the software. This is why the extra fudge
        is needed here to extract those last few groups properly.


        Parameters
        ----------
        image_header : STR
            Str containing the image header read from tag 34682 of
            a .tif file from the Thermo Fisher Scientific
            software xT.

        Returns
        -------
        params : DICT
            a dict whose keys represent various groups of parameters.
            Under the group keys, the parameters are stored as further
            dicts. In the sub-dicts, the key is a string giving the
            parameter name and the value is a the parameter string.
            This can either be a value (no units are given) or a
            text string.

        """
        params = {}

        groups = image_header.split("\r\n\r\n")

        for g in groups:
            if not g[:19] == '[HiResIllumination]':
                p = g.split("\r\n")
                params[p[0]] = {}
                for i in p[1:]:
                    j = i.split("=")
                    params[p[0]][j[0].strip()] = j[1].strip()
            else:
                idx = [i for i, j in enumerate(g) if j == "["]
                g_s = [g[i:j].split("\r\n") for i, j in zip(idx, idx[1:]+[None])]
                for m in g_s:
                    params[m[0]] = {}
                    for n in m[1:]:
                        if len(n) > 0:
                            t = n.split("=")
                            params[m[0]][t[0].strip()] = t[1].strip()

        return params


    @staticmethod
    def get_image_pixel_size(image_path):
        """
        Bespoke method to get the value of the image pixel size
        and the corresponding unit from the header of an SEM image.

        If the image is an Electron Channeling Pattern acquired with
        the Thermo Fisher Scientific xT software, it will be calibrated
        in degrees rather than metres. This function returns the pixel
        size in degrees and the unit 'deg', in that case.


        Parameters
        ----------
        imagePath : STR
            Full path to an SEM image (.tif) recorded with either
            Zeiss SmartSEM or Thermo Fisher Scientific xT
            software.

        Returns
        -------
        img_pix_size : TUPLE
            A 2-tuple containing the value of the image pixel size as
            a float and the unit as a string.

        """
        img_type, img_header = SEMparams.get_image_type_and_header(image_path)

        if img_type == "Zeiss":
            params = SEMparams.extract_params_Zeiss(img_header)
            img_pix_size = SEMparams.get_val(params["AP"]["Image Pixel Size"])

        elif img_type == "ThermoFisher":
            params = SEMparams.extract_params_ThermoFisher(img_header)
            if "ElectronChannelingPatternIsOn" in params["[EBeam]"]:
                if params["[EBeam]"]["ElectronChannelingPatternIsOn"] == "On":
                    img_pix_size = (math.degrees(float(params["[EBeam]"]["AngularPixelWidth"])), "deg")
                else:
                    img_pix_size = (float(params["[Scan]"]["PixelWidth"]), "m")
            else:
                img_pix_size = (float(params["[Scan]"]["PixelWidth"]), "m")

        return img_pix_size


    @staticmethod
    def group_parameters_Zeiss(params):
        """
        Take the dict of the parameters extracted from the image header
        using extract_params_Zeiss() and regroup selected params according
        to the scheme defined in ZEISS_GROUPS. Return a dict of dicts
        containing the regrouped selected parameters.

        Parameters
        ----------
        params : DICT
            A dict of parameters extracted from an SEM image
            using extract_params_Zeiss()

        Returns
        -------
        params_grouped : DICT
            A dict of dicts containing selected parameters grouped
            according to the scheme defined in ZEISS_GROUPS.

        """
        params_grouped = {key : {k : '' for k in value} for (key, value) in
                          SEMparams.ZEISS_GROUPS.items()}

        for k in params_grouped:
            for j in params_grouped[k]:
                g = SEMparams.ZEISS_PARAM_LOCS[j]
                try:
                    params_grouped[k][j] = params[g][j]
                except KeyError:
                    pass

        return params_grouped


    @staticmethod
    def group_parameters_ThermoFisher(params):
        """
        Take the dict of the parameters extracted from the image header
        using extract_params_ThermoFisher() and regroup selected params
        according to the scheme defined in TF_GROUPS. Return a dict of
        dicts containing the regrouped selected parameters.

        Parameters
        ----------
        params : DICT
            A dict of parameters extracted from an SEM image
            using extract_params_ThermoFisher()

        Returns
        -------
        params_grouped : DICT
            A dict of dicts containing selected parameters grouped
            according to the scheme defined in TF_GROUPS.

        """
        params_grouped = {key : {k : '' for k in value} for (key, value) in
                          SEMparams.TF_GROUPS.items()}

        for k in params_grouped:
            for j in params_grouped[k]:
                g = SEMparams.TF_PARAM_LOCS[j]
                if g == "#spec#":
                    g = f"[{params['[Detectors]']['Name']}]"
                try:
                    params_grouped[k][j] = params[g][j]
                except KeyError:
                    pass

        return params_grouped

    @staticmethod
    def print_param_dict(p_dict):
        """
        Print a dict of params grouped under keys to stdout.


        Parameters
        ----------
        p_dict : DICT
            Either:
            A dict containing selected parameters grouped under
            various categories. This dict is created by either
            SEMparams.group_parameters_Zeiss() or
            SEMparams.group_parameters_ThermoFisher(). The groups
            and parameters are defined as class attributes of the
            SEMparams class.

            Or:
            A dict containing ALL the parameters in the header
            read by SEMparams.extract_params_Zeiss() or
            SEMparams.extract_params_ThermoFisher()

        Returns
        -------
        None.

        """
        for i in p_dict:
            print(f"{i} parameters:")
            for j, k in p_dict[i].items():
                print(f"\t{j} = {k}")
            print()


    @staticmethod
    def dump_params_to_json(p_dict, filename, image_path=None):
        """
        Take a dict containing either the parameters extracted
        from the image header (by either
        SEMparams.extract_parameters_Zeiss() or
        SEMparams.extract_parameters_ThermoFisher()) or a selection
        of parameters grouped into different categories (by either
        SEMparams.group_parameters_Zeiss() or
        SEMparams.group_parameters_ThermoFisher()) and dump these to
        a json file with the path filename. Optionally add
        the full path to the original image to the json.

        Parameters
        ----------
        p_dict : DICT
            Either the parameters extracted
            from the image header (by either
            SEMparams.extract_parameters_Zeiss() or
            SEMparams.extract_parameters_ThermoFisher()) or a selection
            of parameters grouped into different categories (by either
            SEMparams.group_parameters_Zeiss() or
            SEMparams.group_parameters_ThermoFisher())
        filename : STR
            Full path to the destination json file.
        image_path : None or STR, optional
            Setting this parameter to a string results in this string
            being written to the json output under the key
            "Original image path". The default is None.

        Returns
        -------
        None.

        """
        p_d = p_dict.copy()

        if isinstance(image_path, str):
            p_d["Original image path"] = image_path

        with open(filename, "w") as f:
            json.dump(p_d, f, indent=2)




    def __init__(self, image_path, verbose=True):
        """
        Initialise with the path to a .tif image from either the
        Zeiss SmartSEM or with Thermo Fisher Scientific xT software.
        Extract and store params and, optionally, print selected
        parameters to the screen.

        Parameters
        ----------
        imagePath : STR
            Full path to an SEM image (.tif) recorded with either
            Zeiss SmartSEM or Thermo Fisher Scientific xT.
        verbose : BOOL, optional
            If True, selected parameters will be printed to stdout
            in groups. The parameters and groups chosen are defined
            as class attributes. The default is True.

        Returns
        -------
        None.

        """
        self.img_path = image_path
        self.img_type, self.img_header = SEMparams.get_image_type_and_header(image_path)

        if self.img_type == "Zeiss":
            self.params = SEMparams.extract_params_Zeiss(self.img_header)
            self.params_grouped = SEMparams.group_parameters_Zeiss(self.params)
            self.software_version = self.params["SV"]["Version"]

        elif self.img_type == "ThermoFisher":
            self.params = SEMparams.extract_params_ThermoFisher(self.img_header)
            self.params_grouped = SEMparams.group_parameters_ThermoFisher(self.params)
            self.software_version = self.params["[System]"]["Software"]

        if verbose:
            print(f"\nParameters extracted from the SEM image: {self.img_path}\n")
            SEMparams.print_param_dict(self.params_grouped)


    def __repr__(self):
        """String representation."""
        r_1 = f"{self.__class__.__name__}:"
        r_2 = f"Image path: {self.img_path}"
        r_3 = f"Image type: {self.img_type}"
        r_4 = f"Software version: {self.software_version}"
        return "\n\t".join([r_1, r_2, r_3, r_4])




def main():
    """
    Command line entry point.

    Calling "sem_io filename" at the command line, where "filename" is
    the full path to an SEM image recorded either with Zeiss SmartSEM
    or with Thermo Fisher Scientific xT, uses the SEMparams class to
    print the parameters extracted from the image header to the terminal.

    Returns
    -------
    None.

    """
    d_0 = "Prints various parameters from the header of an SEM image"
    parser = argparse.ArgumentParser(description=d_0)
    q_0 = "full path to a .tif image produced by either the Zeiss SmartSEM"
    q_1 = " or the Thermo Fisher Scientific xT software"
    parser.add_argument("image_path", help=q_0+q_1)
    parser.add_argument('-v', '--version', action='version',
                        version=f'%(prog)s {__version__}')
    args = parser.parse_args()
    SEMparams(args.image_path)
