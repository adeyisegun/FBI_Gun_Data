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
census_df = census_df.iloc[:, [0,6,8,13,19,35,47,49]]

new_col_names = ['pop_est', '%_under_18', '%_over_65', 
                 '%_black','%_white', '%_degree', 'median_household_income' , 
                 '%_poverty']
census_df.columns = new_col_names
# Check for missing values
census_df.isnull().sum()

# convert data types
census_df.info()
census_df.describe()
census_df['pop_est'] = census_df['pop_est'].str.replace(',','').astype(int)

census_df['median_household_income'] = census_df['median_household_income'].str.replace('$','')
census_df['median_household_income'] = census_df['median_household_income'].str.replace(',','').astype(int)

cols = ['%_under_18', '%_over_65', '%_black', '%_white','%_degree','%_poverty']
for c in cols:
    census_df[c] = census_df[c].str.replace('%','').astype(float)
    census_df[c] = census_df[c].apply(lambda x: x*100 if x < 1 else x)

# For the Gun Data:
# we are going to concentrate our analysis on background checks initiated by an official prior to the issuance of hand guns and long guns only.
# Hence we will remove every colomn expect for 'month', 'state', 'handgun', 'long_gun'.
gun_df.drop(gun_df.columns.difference(['month', 'state', 'handgun', 'long_gun']), axis = 1, inplace=True)
#rename handgun coloumn for consistensy
gun_df.rename(columns={ "handgun":  "hand_gun"}, inplace=True)
# Check for missing values
gun_df.isnull().sum()
# deal with null values - drop rows with null value
gun_df.dropna(axis = 0, inplace=True)
# Check for missing values
gun_df.isnull().sum()

# convert data types
gun_df.info()
gun_df['month'] = pd.to_datetime(gun_df.month)
gun_df['month'] = gun_df['month'].dt.to_period('M')

gun_df['hand_gun'] = gun_df['hand_gun'].astype(int)
gun_df['long_gun'] = gun_df['long_gun'].astype(int)
gun_df.info()

gun_df.describe()

#get a column for the totals
gun_df['total'] = gun_df['hand_gun'] + gun_df['long_gun']



################Explore
gun_df.groupby('month')['total'].mean().plot(kind = 'line')

gun_df.groupby('state')['total'].mean().plot(kind = 'bar')

groupby_state = gun_df.groupby('state').mean()
top_states = groupby_state.query('total > total.mean()')
top_states.groupby('state')['total'].mean().plot(kind = 'bar')

census_df['pop_est'].plot(kind = 'bar')

census_df['pop_est'].sort_values(ascending=False).plot(kind = 'bar')


gun_df.query('state == "California"').plot(x='month', y= 'total', kind = 'line');

census_df.query('pop_est > pop_est.mean()')
census_df.pop_est.mean()

# merge (gun_df.groupby('state').mean())  and (census_df)

state_df = gun_df.query('month.dt.year >= 2015').groupby('state').mean()

merged_df = pd.merge(state_df,census_df, left_on='state', right_index=True, how='inner')
merged_df.rename(columns={ "total":  "gun_checks_mean"}, inplace=True)
merged_df['gun_checks_prop'] = merged_df.gun_checks_mean/merged_df.pop_est

merged_df.plot(x='%_black', y= 'gun_checks_prop', kind = 'scatter');
merged_df.plot(x='%_white', y= 'gun_checks_prop', kind = 'scatter');
merged_df.plot(x='%_poverty', y= 'gun_checks_prop', kind = 'scatter');
merged_df.plot(x='%_degree', y= 'gun_checks_prop', kind = 'scatter');
merged_df.plot(x='%_under_18', y= 'gun_checks_prop', kind = 'scatter');
merged_df.plot(x='%_over_65', y= 'gun_checks_prop', kind = 'scatter');
merged_df.plot(x='median_household_income', y= 'gun_checks_prop', kind = 'scatter');


merged_df['long_gun_prop'] = merged_df.long_gun/merged_df.pop_est

merged_df.plot(x='%_under_18', y= 'long_gun_prop', kind = 'scatter')
plt.title('Some Title')
plt.xlabel('Some X Label')
plt.ylabel('Some Y Label');


# Looks like the

#  Use this, and more code cells, to explore your data. Don't forget to add

> **Tip**: Once you are satisfied with your work, you should save a copy of the report in HTML or PDF form via the **File** > **Download as** submenu. Before exporting your report, check over it to make sure that the flow of the report is complete. You should probably remove all of the "Tip" quotes like this one so that the presentation is as tidy as possible. Congratulations!
   Markdown cells to document your observations and findings.






# What is the overall trend of gun purchases?
gun_df.groupby('month')['total'].mean().plot(kind = 'line')

# Which states are the top five highest in total background checks for issuance (1998-2017) of hand guns & long guns?
gun_df.groupby('state')['total'].sum().nlargest(5).plot(kind = 'bar')
