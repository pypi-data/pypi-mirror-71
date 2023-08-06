# Osmapy - Python Editor for OpenStreetMap Data

![Logo](osmapy/assets/appicon.png)

May I introduce you to __Osmapy__, the Editor for [OpenStreetMap](https://www.openstreetmap.org) data written in Python.
This should become the new state of the art editor for OpenStreetMap.
In contrast to the other common OSM editors this editor is based on Python.
Python is modern, has a huge user base and is battery-included.
This allows everyone to contribute to this project.
Osmapy uses the widespread, powerful and freshly-looking Qt-framework.

*OpenStreetMap and the OpenStreetMap Logo are a trademarks of the OpenStreetMap Foundation, and are used with their permission. Osmapy is not endorsed by or affiliated with the OpenStreetMap Foundation.  
The Python Logo is a trademarks of the Python Software Foundation, and is used with their permission. Osmapy is not endorsed by or affiliated with the Python Software Foundation.*

![example](examples/example.png)

![example](examples/example2.png)

Currently Osmapy is more like a prove of concept than a full fledged editor.
But it can already be used to modify OSM nodes.

## Features
The following Features are already implemented:
 * Interface to Slippy Tiles
    * LiFo queue to load the most needed tiles first
    * Multiple workers to download tiles
    * Caching
    * Easy configuration to chose tile servers
 * Layers
    * Multi-Layer support
    * Change layer order by Drag'n'Drop
    * Change the opacity of layers
 * GPX files
    * GPX files are easily loaded by Drag'n'Drop
 * OSM objects modification
    * Create / Modify / Delete OSM nodes
    * Add / Change / Remove Tags
    * Precise node moving with the arrow keys
    * Upload your changes to the OSM server
 * Adaptive appearance
    * All the tool windows can be moved around freely
 * Easy configuration
    * Just one YAML file must be modified

## Installation

The editor can be easily installed using pip:
```
pip3 install osmapy
``` 

After installation run in the commandline:
```
osmapy
```

> :warning: **Windows**  
> Python must be added to your PATH variable. If you have not chosen to do this while the installation of Python.
> You have two options to achieve this:  
> 1. Re-run the Python installer, select Modify, go to the next tab and enable the option "Add Python to environment variables"
> 2. Manually modify the PATH variable and add the path where osmapy is installed. In the most cases that's something like
> `C:\Users\USERNAME\AppData\Local\Programs\Python\Python38-32\Scripts\`. 

> :warning: **Windows**  
> Maybe you have to install the [Build Tools for Visual Studio](https://visualstudio.microsoft.com/downloads/) on Windows.
> If the installation of Osmapy fails while installing numpy this is suggested by the error message.


## Development and Testing

Please use the [sandbox API](https://master.apis.dev.openstreetmap.org) for development and testing. You can set the API url in the configuration file.
```
osm_api_url: https://master.apis.dev.openstreetmap.org
```
    
## Small User Hints

 - Move around: Right mouse button + Mouse Move
 - Zooming: Mousewheel
 - After zooming in you can click on "Load Elements" to load the OSM elements in the visible area
 - Select Node with right click
 - Move selected Node with arrow keys
 - Remove OSM tag: click on the key of the tag
 - Drop GPX file into window to load it
 
# Contributing
All contributions are welcome!

# License
This software is released under the terms of the [GNU General Public License v3.0](LICENSE).
 
