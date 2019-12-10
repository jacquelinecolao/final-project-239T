# 239T Final Project

## Short Description

Give a short, 1-2 paragraph description of your project. Focus on the code, not the theoretical / substantive / academic side of things.

## Dependencies

1. R, version 1.2.1335
2. Python 3.7, Anaconda distribution.

## Files

List all other files contained in the repo, along with a brief description of each one, like so:

### Data

polity.csv: The PolityVI dataset, available here: http://www.systemicpeace.org/inscrdata.html
nyt.csv: Contains data from the New York Times API collected via collect-nyt.ipynb . Includes information on all articles containing the term "Programmer Cat", 1980-2010.
analysis-dataset.csv: The final Analysis Dataset derived from the raw data above. It includes country-year values for all UN countries 1980-2010, with observations for the following variables:
ccode: Correlates of War numeric code for country observation
year: Year of observation
polity: PolityVI score
nyt: Number of New York Times articles about "Programmer Cat"

### Code

01_collect-nyt.py: Collects data from New York Times API and exports data to the file nyt.csv
02_merge-data.R: Loads, cleans, and merges the raw Polity and NYT datasets into the Analysis Dataset.
03_analysis.R: Conducts descriptive analysis of the data, producing the tables and visualizations found in the Results directory.

### Results

coverage-over-time.jpeg: Graphs the number of articles about each region over time.
regression-table.txt: Summarizes the results of OLS regression, modelling nyt on a number of covariates.
