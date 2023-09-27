# sem_io

Provides some helper functions to extract and view parameters stored in the header of SEM images (.tif) recorded using either Zeiss SmartSEM or Thermo Fisher Scientific xT software.

This is a single Python module and can either be installed or easily incorporated into other projects (the license must be retained in this case).

<BR>

### Installation

Please clone/download the repository and install with pip

```bash
cd sem_io
pip install .
```

<BR>


### Usage

*Command line*

To print an overview of parameters from the image header in the console, at the command line, you can do:

```bash
sem_io path_to_my_image.tif
```

<BR>


*Python*

You can also import the module and use the functions directly in Python.

```python
>>> import sem_io
```

<BR>

To print an overview of parameters from the image header in the console:

```python
>>> my_params = sem_io.SEMparams("path_to_my_image.tif")
```

<BR>


If you just want to collect and store the parameters and not print them, you can do:

```python
>>> my_params = sem_io.SEMparams("path_to_my_image.tif", verbose=False)
```

<BR>


You can print ALL the header parameters to the console like this:

```python
>>> my_params.print_param_dict(my_params.params)
```

<BR>


You can print A SELECTION OF the header parameters (given in the class definition) to the console like this:

```python
>>> my_params.print_param_dict(my_params.params_grouped)
```

<BR>


Both my_params.params and my_params.params_groups are dictionaries and any parameter can be accessed, e.g.

```python
>>> date = my_params.params_grouped["General"]["Date"]
```

<BR>


Alternatively you can dump all the header parameters to a json file (optionally including a key giving the original image path) like this:

```python
>>> my_params.dump_params_to_json(my_params.params, "my_json_path.json", image_path=my_params.img_path)
```


<BR>

### Getting the Image Pixel Size and Adding a Scalebar

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

*Even Electron Channeling Patterns acquired in rocking beam mode are correctly handled by sem_io.SEMparams.get_image_pixel_size()*

<BR>


### Dependencies

* [Pillow](https://python-pillow.org/)

### General

* The selected parameters defined in the class definition of SEMparams form a subset of those available in the header of the .tif image. If you are interested in other parameters, the program can be easily customised - all the header parameters are extracted and are available as the "params" instance attribute.
* If there are any issues, please feel free to get in touch using the [issues mechanism](https://github.com/tgwoodcock/sem_io/issues)
