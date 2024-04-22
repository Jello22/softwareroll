# softwareroll
Generic software rollout utility in Python using UNC paths can easily be changed to have the script sit in a folder with along with the required files
example.  If you are going to do that consider compressing the dependencies.
Script Folder
|
|
|
|------>Dependeceny folder(s)
script.py(or.exe)

Package it up for easy use 
pyinstaller --windowed script.py
