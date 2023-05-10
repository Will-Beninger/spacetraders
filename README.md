# SpaceTraders Python API
## Overview:
Project goal is just to get a minimal working API working that can be used to loop certain function and automate task
## Dependencies:
- Using pandas module for displaying the json data in a tabular format
- requests module for interacting with API
- os module for home directory expansion & future file writing
- path module for reading/writing files
## Setup
- Create a .spacetraders/ directory in the home directory (~)
mkdir -p ~/.spacetraders/
Place a file called "token" in the directory and enter in your token for the game
echo -ne "<token here>" > ~/.spacetraders/token
## Use
Run from terminal:
python3 spacetraders.py
