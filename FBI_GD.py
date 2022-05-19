import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

path  = 'C:/Users/Shopinverse/Desktop/Data_Science/ALX_Data_Analyst/1_Intro_DA/Project/FBI_Gun_Data/'

gun_df = pd.read_excel(path+'ncis-and-census-data/gun_data.xlsx')
census_df = pd.read_csv(path+'ncis-and-census-data/US_Census_Data.csv')

# Print out the first 5 rows of the gun data
gun_df.head()
# Print out the Last 5 rows of the gun data
gun_df.tail()
# Print out the first 5 rows of the census data
census_df.head()
# Print out the Last 5 rows of the census data
census_df.tail()
# number of samples in gun data
gun_df.shape
# number of samples in census data
census_df.shape

# For the Census data:
# Firstly, we see that we have lots of missing values at the tail of the census data. We are going to solve this by removing any row that has more than 10 missing values.
# Secondly, we make the *Fact* coloumn the row name/index and remove fact note coloumn
# Thirdly, we also see that the features are on the rows. To ensure that we have the same data type on each coloumn we need to transpose the table.

# removing any row that has more than 10 missing values
census_df = census_df[census_df.isnull().sum(axis=1) < 10]
census_df.tail()
# make the *Fact* coloumn the row name/index and remove fact note coloumn
census_df.set_index('Fact', inplace = True)
census_df.drop(['Fact Note'], axis=1, inplace = True)
census_df.head()
# Transpose the census table
census_df = census_df.T
# select relevant columns
#census_df.drop(['Fact Note'], axis=1, inplace = True)
#census_df.drop(census_df.iloc[:, [1,7,9,14,36,48,50]],axis = 1)
#census_df[census_df.iloc[:, [1,7,9,14,36,48,50]]]
#census_df.iloc[:, [1,7,9,14,36,48,50]].columns.value_counts().sum()
census_df = census_df.iloc[:, [0,6,8,13,35,47,49]]

new_col_names = ['population_estimate', 'perc_under_18', 'perc_over_65', 
                 'perc_black', 'perc_Bdeg', 'median_household_income' , 
                 'perc_poverty']
census_df.columns = new_col_names

# For the Gun Data:
# we are going to concentrate our analysis on background checks initiated by an official prior to the issuance of hand guns and long guns only.
# Hence we will remove every colomn expect for 'month', 'state', 'handgun', 'long_gun'.
#gun_df.drop(gun_df.iloc[:, 9:],axis = 1, inplace = True)
gun_df.drop(gun_df.columns.difference(['month', 'state', 'handgun', 'long_gun']), axis = 1, inplace=True)
#rename handgun coloumn for consistensy
gun_df.rename(columns={ "handgun":  "hand_gun"}, inplace=True)
#get a column for the totals
gun_df['total'] = gun_df['hand_gun'] + gun_df['long_gun']

