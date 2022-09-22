# sem_io

Provides some helper functions to extract and view parameters stored in the header of SEM images (.tif) recorded using the software Zeiss SmartSEM V06.

This is a single Python module and can either be installed or easily incorporated into other projects (the license must be retained in this case).

### Installation

Please clone/download the repository and install with pip

```bash
cd sem_io
pip install .
```

### Usage

*Command line*

To print an overview of parameters from the image header in the console, at the command line, you can do:

```bash
sem_io path_to_my_image.tif
```

*Python*

You can also import the module and use the functions directly in Python.

```python
>>> import sem_io
```

To print an overview of parameters from the image header in the console:

```python
>>> my_params = sem_io.SEMparams("path_to_my_image.tif")
```

If you just want to collect and store the parameters and not print them, you can do:

```python
>>> my_params = sem_io.SEMparams("path_to_my_image.tif", verbose=False)
```

Then, to extract a particular parameter, you can then do:

```python
>>> my_params.get_parameter("Aperture Size")
(120.0, 'µm')
>>> my_params.get_parameter("Date")
'25 Nov 2020'
```

Parameters with a value and a unit are returned as a 2-Tuple. Other parameters are returned as a string.

All the functions are staticmethods, so you don't need to instantiate the SEMparams class at all. For example, there is a bespoke function for getting the image pixel size and its unit in one line of code:

```python
>>> pixel_size, unit = sem_io.SEMparams.get_image_pixel_size("path_to_my_image.tif")
```

This is useful if you want to plot the SEM image using [matplotlib](https://matplotlib.org/) and add a scalebar with the correct dimensions using [matplotlib-scalebar](https://github.com/ppinard/matplotlib-scalebar). Here's the whole process as an example:

```python
>>> import matplotlib.pyplot as plt
>>> from matplotlib_scalebar.scalebar import ScaleBar
>>> import sem_io
>>> my_image = plt.imread("path_to_my_image.tif")
>>> fig, ax = plt.subplots()
>>> ax.imshow(my_image, cmap='gray')
>>> pixel_size, unit = sem_io.SEMparams.get_image_pixel_size("path_to_my_image.tif")
>>> my_scalebar = ScaleBar(pixel_size, units=unit, location='lower right', scale_loc='top')
>>> ax.add_artist(my_scalebar)
```

### Dependencies

* [Pillow](https://python-pillow.org/)

### General

* The parameters defined in SEMparams form a subset of those available in the header of the .tif image. If you are interested in other parameters, the program can be easily customised.
* If there are any issues, please feel free to get in touch using the [issues mechanism](https://github.com/tgwoodcock/sem_io/issues)
