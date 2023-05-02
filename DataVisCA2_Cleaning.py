#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px


# In[2]:


#reading the data and putting it into pandas dataframes
infections = pd.read_csv(r'C:\Users\shaqu\OneDrive\Desktop\Masters Course\DataVis\CA2\covid_all.csv')
vaccines = pd.read_csv(r'C:\Users\shaqu\OneDrive\Desktop\Masters Course\DataVis\CA2\covid_vaccines.csv')


# ---------------------------------------------------------------------------------------------------------------------------
# 
# 
# 
# Infections dataframe cleaning

# In[3]:


infections


# In[4]:


infections.dtypes


# In[5]:


infections.describe()


# In[6]:


#checking for null values in infections dataframe
infections.isnull().sum()


# In[7]:


#checking life expectancy column for null values to ascertain if null values are only present in certain data groups
infections[infections['life_expectancy'].isnull()]


# Kosovo life expectancy data is not available in the data , noted for future metrics. Cumlative sum should be used for this in future.

# In[8]:


#converting date and month_year to datetime objects
infections['date'] = pd.to_datetime(infections['date'])
infections['month_year'] = pd.to_datetime(infections['month_year'],format='%Y-%m').dt.to_period('M')


# In[9]:


infections.dtypes


# In[10]:


infections


# In[11]:


#checking for duplicate entries in infections
duplicate_entries = infections[infections.duplicated()]


# In[12]:


duplicate_entries


# No duplicate entries/rows in our dataset which is very good, there are duplicate values such as continent and so on but no row is an exact copy, ensures our date's dont overlap.

# In[13]:


#plotting_data = infections
#fig = px.box(plotting_data,x ='continent' , y="new_cases",hover_data=["date"])
#fig.show()


# Plotted the new cases data for a check on outliers to see if there was anything unusual with the numbers present, everything looks fine, with hover data on date the plot consumes a lot of processing power so im commenting it out as to not waste time when restarting the notebook kernal.

# ---------------------------------------------------------------------------------------------------------------------------
# 
# 
# 
# Vaccine dataframe cleaning

# In[14]:


vaccines


# In[15]:


vaccines.dtypes


# In[16]:


vaccines.describe()


# In[17]:


#checking for null values in vaccines
vaccines.isnull().sum()


# In[18]:


#checking for null values in people vaccinated to see whether the null values are for data missing or 0 values
vaccines[vaccines['people_vaccinated'].isnull()]


# In[19]:


#checking to confirm the nan entries are not just there for 0 vaccinated people but rather no data present
vaccines[vaccines['people_vaccinated'] == 0]


# When checking on vaccination data nan's we can see that there are many, however upon looking at the rows and values where vaccinatons are 0, we can see that the nan's should represent the days that nobody was vaccinated.

# In[20]:


# reformatting date and month_year to datetime objects
vaccines['date'] = pd.to_datetime(vaccines['date'])
vaccines['month_year'] = pd.to_datetime(vaccines['month_year'],format='%Y-%m').dt.to_period('M') 


# In[21]:


#checking to see if there are any duplicate rows
duplicate_entries_vaccines = vaccines[vaccines.duplicated()] 


# In[22]:


duplicate_entries_vaccines


# ---------------------------------------------------------------------------------------------------------------------------
# 
# Joining the two dataframes via date in order to have 1 proper dataframe upon which to easily graph/plot.

# In[23]:


# dropping duplicate and not useful columns
vaccines.drop(['location','iso_code','month_year','year','month','continent'],axis = 1, inplace = True) 


# In[24]:


# sorting the dataframes in order to merge by the date they share
infections = infections.sort_values('date')
vaccines = vaccines.sort_values('date') 


# In[25]:


# reformatting float numbers for visibility , no to the power of e' numbers
pd.options.display.float_format = '{:.0f}'.format 


# In[26]:


# merging the infections and vaccines on inner join with date
covid_data = pd.merge_asof(infections, vaccines, on='date') 

covid_data


# In[27]:


covid_data.dtypes # checking dtypes to ensure no duplicate comlumns after the merge


# In[28]:


covid_data.reset_index(drop=True) #resetting the index for clarity


# Important to note that the vaccine data records only start from 14th Dec 2020*

# In[ ]:


covid_data.to_csv(r'C:\Users\shaqu\OneDrive\Desktop\Masters Course\DataVis\CA2\covid_data.csv')  

