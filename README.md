# EDA_python
Implementation in python of the already existing software EDA.

## Installation
### Install release
Download the latest release compatible with your system, give it permission to execute and launch it by simply double clicking on it.

### Manual installation

#### Requirements
```
python >= 3.10
pip >= 22
git
```
#### Procedure
Download or clone this repo, jump into it and run:
##### Linux
```
cd EDA_python
pip install -r src/requirements.txt
```
Once installed export env variable:
```
export PYTHONPATH="$PYTHONPATH:path/to/your/project/EDA_python"
```
for example if you download this project in `/home/usr/something/ ` the command whould be:
```
 export PYTHONPATH="$PYTHONPATH:/home/usr/something/EDA_python"
```
Launch it
```
python src/main.py
```
##### Windows
Open cmd prompt
Move into EDA_python
```
cd path\to\EDA_python"
```
Install the dependencies
```
py -m pip install -r src\requirements.txt 
```
Set environment variable
```
set PYTHONPATH=%cd%
```
Launch it
```
py src\main.py
```
