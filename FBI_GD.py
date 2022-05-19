import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

gun_df = pd.read_excel('ncis-and-census-data/gun_data.xlsx')
census_df = pd.read_csv('ncis-and-census-data/US_Census_Data.csv')

gun_df.head()
gun_df.tail()
census_df.head()
census_df.tail()


census_df = census_df[census_df.isnull().sum(axis=1) < 10]
census_df.tail()


# make the *Fact* coloumn the row name/index and remove fact note coloumn
census_df.set_index('Fact', inplace = True)
df_08.drop(['Unadj Cmb MPG'], 
             axis=1, inplace = True)
census_df.head()

# Transpose the census table
census_df.head()