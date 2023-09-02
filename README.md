# My Master's Thesis

> A Clean LaTeX Style for Thesis Documents

This repository contains my master's thesis titled "Analyzing Bike Tracks Using Artificial Intelligence Algorithms" along with the code and scripts used in my research project.

## Thesis

The LaTeX source files for my thesis are located in the `thesis` directory. The main file is `my-thesis.tex`.

## Project

The Python code and Jupyter notebooks for my machine learning project are located in the `project` directory.

The main scripts are:

- `gpx_to_csv.py` - Script for loading, cleaning, and preprocessing the dataset and converting it into a CSV file
- `Implement_ML.ipynb` - Defines and trains the machine learning model

<!-- The `data` directory contains the raw and processed datasets used for this project. -->

## Usage

The Python scripts expect the data to be located in the `data` folder. To run the full pipeline:

1. Process data: `python gpx_to_csv.py`
2. Run the model: `python Implement_ML.ipynb`

## Requirements

The code was developed with Python 3.11 and requires the following packages:

- NumPy
- Pandas
- Scikit-Learn
- Matplotlib
- gpxpy

### Create the environment from the environment.yml file

```bash
conda env create -f environment.yml
```

### Activate the virtual environment

```bash
conda activate <ENV_NAME>
```

## Results

The key results of my project can be found in Chapter 4 of my thesis.

## References

See the Bibliography section in my thesis for a full list of references.

## How to Contribute

Contributions are welcome! If you'd like to contribute to this repository, please fork it, make your changes, and submit a pull request.

Here is a draft README.md file for your master's thesis GitHub repository:
