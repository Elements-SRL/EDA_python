# EDA_python
Implementation in python of the already existing software EDA.

## Installation

### Manual installation

#### Requirements
```
python >= 3.10
pip >= 22
```
#### Procedure
Download this repo, jump into it and run:
```
pip install -r src/requirements.txt 
```
Once installed export env variable:
##### Linux
```
export PYTHONPATH="$PYTHONPATH:path/to/your/project/EDA_python"
```
for example if you download this project in `/home/usr/something/ ` the command whould be:
```
 export PYTHONPATH="$PYTHONPATH:/home/usr/something/EDA_python"
```
##### Windows
Open cmd prompt
Move into EDA_python
```
cd path\to\EDA_python"
```
Set environment variable
```
set PYTHONPATH=%cd%
```
#### Launch it
Move into EDA_python and run
##### Linux
```
python src/main.py
```
##### Windows
```
py src\main.py
```

### Install release
Download the latest release, give it permission to execute and launch it.
