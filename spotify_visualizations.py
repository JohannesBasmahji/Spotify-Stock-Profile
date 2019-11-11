#!/usr/bin/env python
# coding: utf-8

# # Introduction
# 
# In this project, I will use programming language Python to visualize Spotify stock data.
# In finance, a _stock profile_ is a series of studies, visualizations, and analyses that dive into different aspects a publicly traded company's data. 
# 
# I will visualize data for whole quarters of 2018/2019. Specifically, and will creating the following visualizations:
# + The distribution of the stock prices for the past quarters
# + The actual vs. estimated earnings per share for the past quarters in 2018/2019
# + Spotify's earnings and revenue in the last quarters
# + A comparison of the Spotify Stock price vs the Dow Jones Industrial Average price in 2018/2019 
# 
# 
# During this project, I will analyze, prepare, and plot data. My visualizations can help asses the risk of the Spotify stock.
# 
# As the last step I will be creating a presentation to share.
# 
# Financial Data Source: [Yahoo Finance](https://finance.yahoo.com/quote/DATA/)

# ## Step 1
# 
# First I get my notebook ready for visualizing! Importing the modules that I be using in this project:

# In[1]:


from matplotlib import pyplot as plt
import pandas as pd
import seaborn as sns
import numpy as np


# ## Step 2

# Here I'm loading the datasets and inspect them.

# Loading **SPOT_monthly.csv** into a DataFrame called `spotify_stocks`. Then, inspect the DataFrame:
# 
# Note: In the Yahoo Data, `Adj Close` represents the adjusted close price adjusted for both dividends and splits. This means this is the true closing stock price for a given business day.

# In[2]:


spotify_stocks = pd.read_csv('SPOT_monthly.csv')
print(spotify_stocks)


# Loading **DJI.csv** into a DataFrame called `dowjones_stocks`. Then, inspect the DataFrame:

# In[3]:


dowjones_stocks = pd.read_csv('DJI.csv')
print(dowjones_stocks)


# Loading **SPOT_daily.csv** into a DataFrame called `spotify_stocks_daily`. Then, inspect the DataFrame's first 5 values:

# In[4]:


spotify_stocks_daily = pd.read_csv('SPOT_daily.csv')
print(spotify_stocks_daily.head())


# ## Step 3

# As I'm going to visualize stocks data in quarters, I will create a column called 'Quarter' in a new DataFrame based on `spotify_stocks_daily`:

# Before starting I will inspect the types of the columns in `spotify_stocks_daily`:

# In[5]:


print(spotify_stocks_daily.dtypes)


# The new column will be based on content from the 'Date' column, but not everything. 
# That's why I use splitting by character and picking out what I need:

# In[6]:


# Creating the temporary 'str_split' column
spotify_stocks_daily['str_split'] = spotify_stocks_daily.Date.str.split('-')

# Creating the temporary 'Year' column and fill it with the year string
spotify_stocks_daily['Year'] = spotify_stocks_daily.str_split.str.get(0)

# Creating the temporary 'Month' column and fill it with the motnh string
spotify_stocks_daily['Month'] = spotify_stocks_daily.str_split.str.get(1)

# Droping the 'str_split' column
spotify_stocks_daily = spotify_stocks_daily.drop(columns='str_split')


# The temporary 'Month' column is going to help me to put dates in right quarter:

# In[7]:


conditions = [
    (spotify_stocks_daily['Month'] == '01'),
    (spotify_stocks_daily['Month'] == '02'),
    (spotify_stocks_daily['Month'] == '03'),
    (spotify_stocks_daily['Month'] == '04'),
    (spotify_stocks_daily['Month'] == '05'),
    (spotify_stocks_daily['Month'] == '06'),
    (spotify_stocks_daily['Month'] == '07'),
    (spotify_stocks_daily['Month'] == '08'),
    (spotify_stocks_daily['Month'] == '09'),
    (spotify_stocks_daily['Month'] == '10'),
    (spotify_stocks_daily['Month'] == '11'),
    (spotify_stocks_daily['Month'] == '12')]
choices = ['Q1','Q1','Q1','Q2','Q2','Q2','Q3','Q3','Q3','Q4','Q4','Q4']

# Creating the temporary 'Q' column
spotify_stocks_daily['Q'] = np.select(conditions, choices, default='null')


# Where I'm creating the new column 'Quarter' based on the temporary columns 'Q' and 'Year':

# In[8]:


spotify_stocks_daily['Quarter'] = spotify_stocks_daily['Q'] + '-' + spotify_stocks_daily['Year']


# Finally I can create DataFrame called `spotify_stocks_quarterly`. And at the same time I can drop the tree temporary columns ('Year','Month','Q') before checking the new DataFrame:

# In[9]:


spotify_stocks_quarterly = spotify_stocks_daily.drop(columns=['Year','Month','Q'])
print(spotify_stocks_quarterly.head())


# ## Step 4
# 
# Now let's look at the column names of the DataFrame `spotify_stocks`: 

# In[10]:


print(spotify_stocks.head())


# The term `Adj Close` is a confusing term if you don't read the Yahoo Documentation. In Yahoo, `Adj Close` is documented as adjusted close price adjusted for both dividends and splits.
# 
# This means this is the column with the true closing price, so these data are very important.
# 
# I will us Pandas to change the name of of the column to `Adj Close` to `Price` so that it is easier to work with the data. 
# 
# I will also do this for the Dow Jones and Spotify Quarterly pandas dataframes as well.

# In[11]:


spotify_stocks.rename(columns = {'Adj Close' : 'Price'}, inplace=True)
dowjones_stocks.rename(columns = {'Adj Close' : 'Price'}, inplace=True)
spotify_stocks_quarterly.rename(columns = {'Adj Close' : 'Price'}, inplace=True)


# Running `spotify_stocks.head()` again to check if the column name has changed.

# In[12]:


print(spotify_stocks.head())


# Calling `.head()` on the DataFrame `dowjones_stocks` and `spotify_stocks_quarterly`.

# In[13]:


print(dowjones_stocks.head())
print(spotify_stocks_quarterly.head())


# ## Step 5
# 
# In this step, I will be visualizing the Spotify quarterly data! 
# 
# I want to get an understanding of the distribution of the Spotify quarterly stock prices for 2018/2019. Specifically, I want to see in which quarter stock prices flucutated the most. I will accomplish this using a violin plot with six violins, one for each business quarter:

# In[14]:


sns.set_style("whitegrid")
sns.set_palette("pastel")

ax = sns.violinplot()
sns.violinplot(x=spotify_stocks_quarterly.Quarter, y=spotify_stocks_quarterly.Price, data=spotify_stocks_quarterly)
ax.set_title('Distribution of 2018/2019 Spotify Stock Prices by Quarter')
plt.ylabel('Closing Stock Price (USD)')
plt.xlabel('Business Quarters in 2018/2019')
plt.savefig("Stock_Prices_by_Quarter.png")
plt.show()


# Let us find out the highest and lowest prices during this period:

# In[15]:


#Checking the max price:
stocks_price_max = spotify_stocks_quarterly.groupby('Quarter').Price.max().reset_index().sort_values(by='Price')
print(stocks_price_max)

#Checking the min price:
stocks_price_min = spotify_stocks_quarterly.groupby('Quarter').Price.min().reset_index().sort_values(by='Price')
print(stocks_price_min)


# The highest price during this period was in the Q3 2018 at 196,28 and lowest prices was in Q4 2018 at 106,84.

#  

# ## Step 6
# 
# Next, I will chart the performance of the earnings per share (EPS) by graphing the estimate Yahoo projected for the Quarter compared to the actual earnings for that quarters. I will accomplish this using a scatter chart:

# In[18]:


x_positions = [1, 2, 3, 4, 5]
chart_labels = ["3Q2018","4Q2018","1Q2019","2Q2019", "3Q2019"]
earnings_actual =[0.26, 2.6,-0.89,-0.46, 0.40]
earnings_estimate = [-0.42, -0.21,-0.40,-0.35, -0.31]
plt.scatter(x_positions, earnings_actual, color='red', alpha=0.5)
plt.scatter(x_positions, earnings_estimate, color='blue', alpha=0.5)
plt.legend(['Actual', 'Estimate'])
plt.xticks(x_positions, chart_labels)
plt.title('Earnings Per Share in Cents')

plt.savefig("earnings_per_share.png")
plt.show()


# In quarter 4 in 2018 the actual ernings out beated the estimated by far. For the next quarter 1 in 2019 the earnings dropped heavily.

#  

#  

# ## Step 7

# Next, I will visualize the earnings and revenue reported by Spotify by mapping two bars side-by-side.
# Plotting side-by-side bars in Matplotlib requires computing the width of each bar before hand:

# In[23]:


# The metrics below are in billions of dollars
revenue_by_quarter = [1.27, 1.35, 1.5, 1.51, 1.67, 1.73]
earnings_by_quarter = [-0.394, 0.043, 0.442, -0.142, -0.076, 0.241]
quarter_labels =["2Q-2018","3Q-2018","4Q-2018","1Q-2019","2Q-2019", "3Q-2019"]

# Revenue
n = 1  # This is our first dataset (out of 2)
t = 2 # Number of dataset
d = 6 # Number of sets of bars
w = 0.8 # Width of each bar
bars1_x = [t*element + w*n for element in range(d)]

plt.bar(bars1_x, revenue_by_quarter)

# Earnings
n = 2  # This is our second dataset (out of 2)
t = 2 # Number of dataset
d = 6 # Number of sets of bars
w = 0.8 # Width of each bar
bars2_x = [t*element + w*n for element in range(d)]


#yticks = [-0.4, 0, 0.4, 0.8, 1.2, 1.6]
#yticklabels = ['-0.4', '0', '0.4', '0.8', '1.2', '1.6']


yticks = [-0.4, -0.2, 0, 0.2, 0.4, 0.6, 0.8, 1.0, 1.2, 1.4, 1.6]
yticklabels = ['-0.4', '-0.2', '0', '0.2', '0.4', '0.6', '0.8', '1.0', '1.2', '1.4', '1.6']

plt.grid(b=None, which='both', axis='x')
plt.bar(bars2_x, earnings_by_quarter)

middle_x = [ (a + b) / 2.0 for a, b in zip(bars1_x, bars2_x)]
labels = ["Revenue", "Earnings"]

plt.legend(labels)
plt.title('Earnings and Revenue in billions')
plt.xticks(middle_x, quarter_labels)
plt.yticks(yticks, yticklabels)

plt.savefig("earnings_revenue.png")
plt.show()


# The Q3 and Q4 in 2018 and the Q3 in 2019 was the quarters without a loss. Let us calculate what percentage of the revenue constitutes the earnings:

# In[21]:


Q3_2018_percent_earning =  0.043 / 1.35 * 100
print(Q3_2018_percent_earning)

Q4_2018_percent_earning = 0.442 / 1.5 * 100
print(Q4_2018_percent_earning)

Q3_2019_percent_earning = 0.241 / 1.73 * 100
print(Q3_2019_percent_earning)


# ## Step 8
# 
# In this last step, I will compare Spotify stock to the Dow Jones Industrial Average in 2018/2019. I will accomplish this by plotting two line charts side by side in one figure:

# In[19]:


# Left plot Spotify
ax1 = plt.subplot(1, 2, 1)
plt.plot(spotify_stocks['Date'], spotify_stocks['Price'], color='mediumseagreen')
plt.title('Spotify')
plt.xlabel('2018               2019')
plt.ylabel('Stock Price')
ax1.set_xticks([0, 2, 4, 6, 8, 10, 12, 14, 16])
ax1.set_xticklabels(['04', '06', '08', '10', '12', '02', '04', '06', '08'], rotation=30)

# Right plot Dow Jones
ax2 = plt.subplot(1, 2, 2)
plt.plot(dowjones_stocks['Date'], dowjones_stocks['Price'], color='dodgerblue')
plt.title('Dow Jones')
plt.xlabel('2018               2019')
plt.ylabel('Stock Price')
ax2.set_xticks([0, 2, 4, 6, 8, 10, 12, 14, 16])
ax2.set_xticklabels(['04', '06', '08', '10', '12', '02', '04', '06', '08'], rotation=30)

plt.subplots_adjust(wspace= 0.5)

plt.savefig("spotify_downjones.png")
plt.show()


#  

# # Step 9
# 
# As this result, I'm have done a presentation, see file : 'Spotify Stock Profile 2018-2019.pdf'
# 
# The slideshow includes:
# 
# - A visualization of the distribution of the stock prices for Spotify 2018/2019
# - A visualization and a brief summary of their earned versus actual earnings per share
# - A visualization and a summary of Spotify stock and revenue for the past quarters and a summary
# - A visualization of Spotify stock against the Dow Jones stock (to get a sense of the market) in 2018/2019
