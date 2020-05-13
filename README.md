# Braph-2.0-Python README

## Installation

Download or clone the repository from github.com. Make sure you have installed python 3.

### Ubuntu

Open a terminal window. Install Qt OpenGL for Python by typing:

    sudo apt install python3-pyqt5.qtopengl

#### Manual installation

Go to the top level folder of the project and install dependencies:

    pip3 install .

#### Installation script

You can also install the project by running the file install.sh, placed in the folder Braph-2.0-Python.
This will install the project's dependencies and place a shortcut to the program in your applications
directory. Note that this replaces only the manual installation, not the first step.

### Windows

Install Qt for python by typing the following command in PowerShell:

    pip3 install pyqt5

Go to the top level folder of the project and install dependencies:

    pip3 install .

### macOS

#### Manual installation

Go to the top level folder of the project and install dependencies by running the following command
in the terminal:

    pip3 install .

#### Installation script

You can also install the project by running the file install_macos.sh, placed in the folder Braph-2.0-Python.
This will install the project's dependencies.

## Run the program

To run the program, run the file braphy.sh, placed in the folder 'bin' in 'Braph-2.0-Python'.

## Development

You can also run the program from the terminal, by typing

    python3 braphy/gui/main_window.py

When developing the software, it is useful to add the Braph directory to your pythonpath.
On Ubuntu/macOS this is done by adding the following line

    export PYTHONPATH=[your braph directory]:$PYTHONPATH

e.g.

    export PYTHONPATH=~/git/Braph-2.0-Python:$PYTHONPATH

at the bottom of your ~/.bashrc file (Ubuntu) or ~/.bash_profile (macOS).

On Windows this is done by adding the pythonpath to your environment variables list.

By doing so, you don't have to install the program after each
change.

### Tests

#### Unit Tests on Ubuntu

To run all tests:

    python3 -m unittest

To run a single test file:

    python3 -m unittest braphy.test.test_betweenness

To debug a test in Visual Studio Code:

1. Set appropriate breakpoints
1. Press F5
1. Select Module
1. Type for example braphy.test.test_distance

## Controlling the brain view

This section provides a guide for controlling the brain view. You can either change the point of
view by using the buttons in the toolbar, or you can use different shortcuts.

* Zoom in/out: use the scroll function
* Pan in x/y-plane: press and drag the scroll wheel
* Pan in x/z-plane: press and drag ctrl + the scroll wheel
* Rotate: press and drag left mouse click (Note that this is not available when a button in the toolbar is checked.)
* Select brain region: right click on brain region

