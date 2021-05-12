# cablegate-cia-analysis
Analysis of cablegate data with the implication of names present with CIA files.

## 1 - Download data

#### corresponding folder: ./1-download-data

`python download-data/run.py`

A part of the raw data files are in ./data-sample/ folder.

To download the different files, you have to run the 'run.py' file.  

## 2 - Convert data 

#### corresponding folder: ./2-convert-data

To convert the different files, you have to run the 'run.py' file.  

## 3 - Extract data

#### corresponding folder: ./3-extract-data

To extract data from the different files, you have to run the 'run.py' file.  



## 4 - Data Analysis

#### corresponding folder: ./4-data-analysis

To generate maps you need to use geopands. To avoid conflicts between the versions of the packages it is better to recreate a Python environment.

`conda create -n geo-env
conda activate geo-env
conda config --env --add channels conda-forge
conda config --env --set channel_priority strict
conda install python=3 geopandas`

Some maps examples in html format are available in ./4-data-analysis/map folder.
