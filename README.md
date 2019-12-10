# 239T Final Project

## Short Description

This project focuses on the independent variable of a larger project. This variable is interest group-party closeness. One way I am operationalizing this variable is the percent of political contributions given to party committees by an interest group. My main focus is on LGBT interest groups, and those are the groups that I collect data on for this project. 

I use the followthemoney API to gather political contribution data for 440 LGBT interest groups. First, I gathered the names and followthemoney ID numbers for all of the interest groups labeled as LGBT on the followthemoney website. Then, I gathered the names of party committees the interest group has donated to, the amount of this donation, and the year the donation was made. I also gathered the names of all of the candidates the interest group has donated to, the names of these candidates, the year the donation was made, as well as information about the type of election, whether the candidate won the election, and the party of the candidate. Lastly, I gathered the total amount of campaign contributions (defined as the amount donated to candidates plus the amount donated to party committees) in a given year for each interest group. 

Once I compiled these datasets, I was able to calculate the percent of campaign contributions given to party committees in a given year for each interest group. I graphed this percentage over time for 8 interest groups of interest, as well as graphed the total campaign contributions for these same interest groups, broken down by the amount given to party committees and the amount given to candidates. 

## Dependencies

1. R, version 1.2.1335
2. Python 3.7, Anaconda distribution.

## Files

### Data

#### Raw Data 

Interest Group Candidate Donations.csv: Contains data from the followthemoney API of LGBT interest group donations to candidates. 
Interest Group Party Committee Donations.csv: Contains data from the followthemoney API of LGBT interest group donations to party committees. 
Interest Group Total Contributions.csv: Contains data from the followthemoney API of the total campaign contributions given by LGBT interest groups, defined as the amount given to candidates plus the amount given to party committees.
Interest_Group_ID_List.csv: Contains data from the followthemoney API of the names of the all of the LGBT interest groups followthemoney has data on, as well as these groups' followthemoney ID numbers. 

#### Cleaned Data for Graphs 

Candidate and Party Contribution Data - Stacked Graph.csv: Contains data on LGBT interest group total donations to candidates in a given year, party committees in a given year, and the sum of both of these types of donations in a given year. This data is in the proper format to create a stacked bar graph in R. 
Party Committee Data with Total Contribution Variables.csv: Contains data on the sum of contributions given to candidates and party committees in a given year by an interest group, the amount donated to a specific party committee by an interest group in a given year, the total amount donated to party committees in a given year, and the percent of total contributions given to party committees in a given year by an interest group. 

### Code

01_gather_data.py: Collects data from the FollowTheMoney API and exports data to the files in the "Raw Data" folder. 
02_Data Cleaning Code.Rmd: Loads, cleans, and merges the files in the "Raw Data" folder into the files in the "Cleaned Data for Graphs" folder.
03_Data Visualization Code.Rmd: Loads the datasets in the "Cleaned Data for Graphs" folder and produces the visualizations found in the Results folder.

### Results

Messy Interest Group Line Graph.png: Graphs the percent of total contributions given to party committees across time for 8 interest groups - all on the same graph.
Facet Wrap Interest Group Line graph: Graphs the percent of total contributions given to party committees across time for 8 interest groups - each on a different graph.
Gay & Lesbian Advocates and Defenders Contributions.png: Graphs the total amount of campaign contributions given by Gay & Lesbian Advocates and Defenders across time, broken down by the amount given to candidates and the amount given to party committees.
Gay & Lesbian Victory Fund Contributions.png: Graphs the total amount of campaign contributions given by Gay & Lesbian Victory Fund across time, broken down by the amount given to candidates and the amount given to party committees.
Human Rights Campaign Contributions.png: Graphs the total amount of campaign contributions given by the Human Rights Campaign across time, broken down by the amount given to candidates and the amount given to party committees.
LPAC Contributions.png: Graphs the total amount of campaign contributions given by LPAC across time, broken down by the amount given to candidates and the amount given to party committees.
Log Cabin Republicans Contributions.png: Graphs the total amount of campaign contributions given by the Log Cabin Republicans across time, broken down by the amount given to candidates and the amount given to party committees.
National Gay & Lesbian Task Force Contributions.png: Graphs the total amount of campaign contributions given by National Gay & Lesbian Task Force across time, broken down by the amount given to candidates and the amount given to party committees.
Stonewall Democrats Contributions.png: Graphs the total amount of campaign contributions given by Stonewall Democrats across time, broken down by the amount given to candidates and the amount given to party committees.

