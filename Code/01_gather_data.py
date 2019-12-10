#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Nov 24 20:23:15 2019

@author: jacquelinecolao
"""
#File Summary 
#In this file I gather data from the followthemoney API. First, I gather a list of LGBT interest groups 
#who have records on followthemoney. Then, I gather data on contributions made to party committees and candidates 
#by these interest groups and the total amount of political contributions made by these interest groups in a given year. 

#setup Github connection
pip install Gitpython
from git import Repo
repo = Repo("/Users/jacquelinecolao/Desktop/ps239t-final-project2")
assert not repo.bare

#setup    
from __future__ import division
import requests
import urllib
import json
import math
import time
import re
import pandas as pd

# set key
key= "dce40de1fddc85fd882cfb7e3c39d540"

# set base url
base_url="https://api.followthemoney.org/"

#Links for each page of LGBT interest groups
orgs_list_link1="https://api.followthemoney.org/?dt=1&d-et=3&d-cci=86&gro=d-eid&p=0&APIKey=dce40de1fddc85fd882cfb7e3c39d540&mode=json"
orgs_list_link2="http://api.followthemoney.org/?dt=1&d-et=3&d-cci=86&gro=d-eid&p=1&APIKey=dce40de1fddc85fd882cfb7e3c39d540&mode=json"
orgs_list_link3="http://api.followthemoney.org/?dt=1&d-et=3&d-cci=86&gro=d-eid&p=2&APIKey=dce40de1fddc85fd882cfb7e3c39d540&mode=json"
orgs_list_link4="http://api.followthemoney.org/?dt=1&d-et=3&d-cci=86&gro=d-eid&p=3&APIKey=dce40de1fddc85fd882cfb7e3c39d540&mode=json"
orgs_list_link5="http://api.followthemoney.org/?dt=1&d-et=3&d-cci=86&gro=d-eid&p=4&APIKey=dce40de1fddc85fd882cfb7e3c39d540&mode=json"

#put the links into one list
master_orgs_links = [orgs_list_link1, orgs_list_link2, orgs_list_link3, orgs_list_link4, orgs_list_link5]

#Grab the name and id number for each interest group
id=[]
name=[]
for x in master_orgs_links:
    r=requests.get(x)
    orgs_list_text=r.text
    id_data=json.loads(r.text)
    for i in range(len(id_data['records'])):
        id.append(id_data['records'][i]['Contributor']['id'])
        name.append(id_data['records'][i]['Contributor']['Contributor'])

#Put the name and id number into a dataset
data = {'Name':name , 'ID Number':id}
Interest_Group_ID_DF=pd.DataFrame(data)

#export the data to a csv
Interest_Group_ID_DF.to_csv(r"/Users/jacquelinecolao/Desktop/ps239t-final-project2/Data/Raw Data/Interest_Group_ID_List.csv",index=False)

#Getting Data for LGBT Interest Group contributions to Party Committees

#Create a link for each ID Number

#create an empty list to store the links
party_contribution_url_list=[]
#run a for loop to get links for each ID number (i.e. for each Interest Group)
for x in Interest_Group_ID_DF['ID Number']:
    #enter the proper search parameters for contributions to party committees
    key="dce40de1fddc85fd882cfb7e3c39d540"
    base_url="https://api.followthemoney.org/"
    search_params = {"dt":"1", "pt-pt":"1","d-eid":x,"gro":"y,pt-eid","APIKey":key,"mode":"json"}
    #get the URLs based on these search parameters
    r = requests.get(base_url, params=search_params)
    party_contribution_url_list.append(r.url)

#store the data from each link to use for creating the interest group variable
#create an empty list to store the data in 
store=[]
#run a for loop to gather data for each link 
for i in range(len(party_contribution_url_list)):
    #get the URLs
    r=requests.get(party_contribution_url_list[i])
    #get the text from these URLs
    text=r.text
    #convert text to a python dictionary
    data=json.loads(text)
    #store the dictionary for each link 
    store.append(data)

#pull the election year, party committee, and contribution total for each interest group, from the ID Number links
#create empty lists for each variable
election_year=[]
party_committee=[]
contribution_total=[]  
#use a for loop to get the json file for each link (repeat of what is in "store" - can do this more efficiently in the future, without repeating code)
for i in range(len(party_contribution_url_list)):
    r=requests.get(party_contribution_url_list[i])
    text=r.text
    data=json.loads(text)
    #run a for loop to get the data for each contribution given by a specific Interest Group
    for j in range(len(data['records'])):
        #set the value of each variable to 0 if there are no contributions to party committees
        if data['records'][0] == "No Records":
            election_year.append(0)
            party_committee.append(0)
            contribution_total.append(0)
        #if there are contributions to party committees, grab the value of the variable
        else:
            election_year.append(data['records'][j]['Election_Year']['Election_Year'])
            party_committee.append(data['records'][j]['Party_Committee']['Party_Committee'])
            contribution_total.append(data['records'][j]['Total_$']['Total_$'])

#create an interest group variable that lists the interest group the amount of times there is a contribution by that interest group to a committee
#create an empty list for the interest group names
interest_group=[]
#run a for loop for each name in the Interest Group ID dataframe
for x in Interest_Group_ID_DF['Name']:
    #run another for loop that connects the name of the Interest Group to the Party Committee data 
    for i in range(len(store)):
        #multiply the name by the number of party contributions given by that Interest Group
        interest_group.append([x]*len(store[i]['records']))

#The method above created a list within a list where every Interest Group name was repeated for the number of party contributions given by every Interest Group 
#Need to grab the list that corresponds to the number of contributions that specific interest group gave 
#create an empy list to store the proper number of Interest Group names
group=[]
i=0
#grab every 441st list within the interest_group list - these lists correspond properly to the number of contributions given by a specific Interest Group 
while i < len(interest_group):
    group.extend(interest_group[i])
    i = i + 441

#create a dataset with the variables
data = {'Interest Group': group, 'Year': election_year, 'Party Committee':party_committee,'Amount Contributed':contribution_total}
Interest_Group_PC_df=pd.DataFrame(data)  

#export the dataset to a csv
Interest_Group_PC_df.to_csv(r"/Users/jacquelinecolao/Desktop/ps239t-final-project2/Data/Raw Data/Interest Group Party Committee Donations.csv",index=False)

#Get Data for LGBT Interest Group contributions to Candidates 
#NOTE - I was only able to get this information for about half of the interest groups. The code takes a while to run and then gives an error about halfway through. I'm still figuring out what's going on.
  
#Get a list of all of the links corresponding to Interest Group contributions to candidates
#create an empty list to store the links 
candidate_contribution_url_list=[]
#create a for loop to create a link for each Interest Group ID number
for x in Interest_Group_ID_DF['ID Number']:
    #run a for loop to create a link corresponding to each page of results for a specific interest group
    for y in range(0,20):
        #enter the correct search parameters for contributions to candidates
        key="dce40de1fddc85fd882cfb7e3c39d540"
        base_url="https://api.followthemoney.org/"
        search_params = {"dt":"1","d-eid":x,"d-cci":"86","gro":"c-t-id","p":y,"APIKey":key,"mode":"json"}
        #create links based on these parameters
        r = requests.get(base_url, params=search_params)
        candidate_contribution_url_list.append(r.url)
 
#Get the data for each link and store altogether
#create an empy list to store the dictionaries
store_candidate=[]
#run a for loop to get the data for each link
for i in range(len(candidate_contribution_url_list)):
    #get the links
    r=requests.get(candidate_contribution_url_list[i])
    #get the text from the links
    text=r.text
    #convert the texts to a python dictionary
    data=json.loads(text)
    #store the dictionaries
    store_candidate.append(data)       

#Grab the variables of interest from the python dictionaries
#create empty lists for each variable
candidate_name=[]
state=[]
year=[]
party=[]
election_type=[]
incumbent=[]
won=[]
office=[]
contribution_total=[]
#run a for loop to grab the dictionary from the list it was stored in above 
for i in range(len(store_candidate)):
    #when grabbing the data from each page of results for an Interest Group, some pages I searched for did not exist.
    #these non-existent pages show up in the dictionary as "No Records"
    #this code essentially tells the overall for loop to ignore these pages
    for j in range(len(store_candidate[i]['records'])):
        if store_candidate[i]['records'][0] == "No Records":
            print("No Data")
        #if the page does exist, grab the value of the variable
        else:
            candidate_name.append(store_candidate[i]['records'][j]['Candidate']['Candidate'])
            state.append(store_candidate[i]['records'][j]['Election_Jurisdiction']['Election_Jurisdiction'])
            won.append(store_candidate[i]['records'][j]['Election_Status']['Election_Status'])
            election_type.append(store_candidate[i]['records'][j]['Election_Type']['Election_Type'])
            year.append(store_candidate[i]['records'][j]['Election_Year']['Election_Year'])
            party.append(store_candidate[i]['records'][j]['Specific_Party']['Specific_Party'])
            incumbent.append(store_candidate[i]['records'][j]['Incumbency_Status']['Incumbency_Status'])
            office.append(store_candidate[i]['records'][j]['Office_Sought']['Office_Sought'])
            contribution_total.append(store_candidate[i]['records'][j]['Total_$']['Total_$'])

#create an interest group variable that lists the interest group the amount of times there is a contribution by that interest group to a candidate
#create an empty list
interest_group=[]
#create a for loop to run through each Interest Group name
for x in Interest_Group_ID_DF['Name']:
    #create a for loop that connects the Interest Group name to the number of candidate contributions
    for i in range(len(store_candidate)):
        #only count pages that exist
        if store_candidate[i]['metaInfo']['paging']['maxPage'] == store_candidate[i]['metaInfo']['paging']['currentPage']:
            #multiply the interest group name by the number of records 
            interest_group.append([x]*int(store_candidate[i]['metaInfo']['paging']['totalRecords']))

#Get rid of the empty cells
interest_group=list(filter(None,interest_group))

#grab the interest groups from the list in a way that corresponds correctly to the rest of the data (ran into the same problem as with party committee contributions)
#create an empty list
group=[]
i=0
#grab every 215th list within the list 
while i < len(interest_group):
    group.extend(interest_group[i])
    i = i + 215

#Like I said above, the code only made it through about half of the groups 
#This code deletes the Interest Group names from the list who the code has not grabbed data for yet 
group=group[:6046]

#some variables were slightly larger than others (by 1-3 observations) due to errant text the code grabbed
#delete this text from each variable 
election_type=election_type[:6046]
candidate_name=candidate_name[:6046]
party=party[:6046]
state=state[:6046]
won=won[:6046]
year=year[:6046]

#create a dataset with the variables
data = {'Interest Group': group, 'Year': year, 'State':state, 'Candidate':candidate_name,'Election Outcome':won,'Election Type':election_type, 'Party':party, 'Incumbent':incumbent, 'Office':office, 'Contribution':contribution_total}
Interest_Group_Candidate_df=pd.DataFrame(data)  

#export the dataset to a csv
Interest_Group_Candidate_df.to_csv(r"/Users/jacquelinecolao/Desktop/ps239t-final-project2/Data/Raw Data/Interest Group Candidate Donations.csv",index=False)

 
#Get contribution totals per year for each Interest Group

#Store the data from each page of the dataset on the followthemoney website
#create an empty list
total_IC_data=[]
#run a for loop that goes through each page of the link that has the total contributions for each interest group
for y in range(0,12):
    #enter the search parameters for total contributions by interest groups
    key="dce40de1fddc85fd882cfb7e3c39d540"
    base_url="https://api.followthemoney.org/"
    search_params = {"dt":"1","d-et":"3","d-cci":"86","gro":"y,d-eid","p":y,"APIKey":key,"mode":"json"}
    #get the links
    r = requests.get(base_url, params=search_params)
    #get the text
    text=r.text
    #convert the text to a python dictionary
    data=json.loads(text)
    #store the dictionaries
    total_IC_data.append(data)

#grab the variables of interest from the dictionaries
#create empty lists for the variables
interest_group=[]
donation_year=[]
donation_amount=[]
#run a for loop that goes through each dictionary
for i in range(len(total_IC_data)):
    #create a for loop that goes through each variable in a given dictionary
    for j in range(len(total_IC_data[i]['records'])):
        #grab the variables of interest
        interest_group.append(total_IC_data[i]['records'][j]['Contributor']['Contributor'])
        donation_year.append(total_IC_data[i]['records'][j]['Election_Year']['Election_Year'])
        donation_amount.append(total_IC_data[i]['records'][j]['Total_$']['Total_$'])

#create a dataset with the variables
data_total_IC = {'Interest Group': interest_group, 'Year': donation_year, 'Amount Contributed': donation_amount}
total_IC_df=pd.DataFrame(data_total_IC)  

#export the dataset to a csv
total_IC_df.to_csv(r"/Users/jacquelinecolao/Desktop/ps239t-final-project2/Data/Raw Data/Interest Group Total Contributions.csv",index=False)

#upload to github
repo = Repo("/Users/jacquelinecolao/Desktop/ps239t-final-project2")
file_list = [
    '/Users/jacquelinecolao/Desktop/ps239t-final-project2/Data/Raw Data/Interest_Group_ID_List.csv',
    '/Users/jacquelinecolao/Desktop/ps239t-final-project2/Data/Raw Data/Interest Group Total Contributions.csv',
    '/Users/jacquelinecolao/Desktop/ps239t-final-project2/Data/Raw Data/Interest Group Candidate Donations.csv',
    '/Users/jacquelinecolao/Desktop/ps239t-final-project2/Data/Raw Data/Interest Group Party Committee Donations.csv',
    '/Users/jacquelinecolao/Desktop/ps239t-final-project2/Code/01_gather_data.py'
]
commit_message = 'upload raw datafiles'
repo.index.add(file_list)
repo.index.commit(commit_message)
origin = repo.remote('origin')
origin.push()

