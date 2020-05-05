# Braph-2.0-Python README

## Installation

Make sure you have installed python 3.

### Ubuntu

Install Qt OpenGL for Python:

    sudo apt install python3-pyqt5.qtopengl

Go to the top level folder of the project and install dependencies:

    pip3 install .

When developing the software, it is useful to add the line

    export PYTHONPATH=~/git/Braph-2.0-Python:$PYTHONPATH

at the bottom of your ~/.bashrc file. By doing so, you don't have to install the program after each
change.

### Windows

Install Qt for python:

    pip3 install pyqt5

Go to the top level folder of the project and install dependencies:

    pip3 install .

### macOS

Go to the top level folder of the project and install dependencies:

    pip3 install .

## Run the program

To run the program, run

    python3 braphy/gui/main_window.py

## Tests

### Unit Tests on Ubuntu

To run all tests:

    python3 -m unittest

To run a single test file:

    python3 -m unittest braphy.test.test_betweenness

To debug a test in Visual Studio Code:

1. Set appropriate breakpoints
1. Press F5
1. Select Module
1. Type for example braphy.test.test_distance