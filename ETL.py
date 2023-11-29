'''This script will be set to always running on our server. Will use it to pull in and wrangle the database data before outputting it again to our final table
that we will use for reporting'''

'''This script will be set to always running on our server. Will use it to pull in and wrangle the database data before 
outputting it again to our final table
that we will use for reporting'''

import pandas as pd
from sqlalchemy import URL, create_engine
import numpy as np

connection_string = URL.create(
  'postgresql',
  username='drewbeno1',
  password='CEBInvDq13or',
  host='ep-small-silence-60017904.us-east-2.aws.neon.tech',
  database='neondb',
)
engine = create_engine(connection_string)

# Define the SQL query to select data from the table
sql_query = "SELECT * FROM dataentry_pitch"

# Use pandas to read the SQL query result into a DataFrame
df = pd.read_sql_query(sql_query, engine)

"""This is where we will do our data wrangling. 
We will need to create extra columns for the following:
- Strike or Ball
- Swing or No Swing
- Free Base or Not Free Base
- Event or Not Event
- The count that the batter was in when the pitch was thrown
"""

# 1. Create strike or ball column
df['strike_ball'] = df['result'].apply(lambda x: 'Ball' if x in ['BALL', 'BB', 'HBP'] else 'Strike')

# 2. Create free_base columns 
df['free_base'] = df['result'].apply(lambda x: True if x in ['BB', 'HBP'] else False)

# 3. create swing measure column
result_mapping = {
    'BALL': ('No swing'),
    'HBP': ('No swing'),
    'K Looking': ('No swing'),
    'FB': ('Swing contact'),
    'SGL': ('Swing contact'),
    'DBL': ('Swing contact'),
    'TPL': ('Swing contact'),
    'HR': ('Swing contact'),
    'BIP OUT': ('Swing contact'),
    'K Swinging': ('Swing no contact'),
    'D3S': ('Swing no contact'),
    'ROE': ('Swing contact')
}

df['swing'] = df['result'].map(result_mapping).fillna(('not classified'))

# ####################### Count Tracker #############################
""" 
We will have to do a couple things to accomplish this task:
1. Create a strike and ball counter
2. Break this table into df2, insert a first row of 0-0 so everything moves down by one, the merge back together on index
  - this logic allows for the count to be recorded as the count that the batter was in as the pitch was thrown
"""

strike_counter = 0
ball_counter = 0  

events = ['SGL', 'DBL', 'TPL', 'HR', 'BIP OUT', 'HBP', 'D3S', 'ROE']

for index, row in df.iterrows():
    if row['strike_ball'] == 'Strike':
        strike_counter += 1
        if strike_counter >= 3 and row['result'] not in ['FB']:
            strike_counter = 0
            ball_counter = 0
        elif strike_counter >= 3:
            strike_counter = 2
    elif row['strike_ball'] == 'Ball':
        ball_counter += 1
        if ball_counter >= 4:
            ball_counter = 0
            strike_counter = 0
        elif ball_counter >= 4:
            ball_counter = 3

    df.at[index, 'ball_counter'] = ball_counter
    df.at[index, 'strike_counter'] = strike_counter


df['strike_counter'] = df['strike_counter'].astype(int) # Get rid of decimals
df['ball_counter'] = df['ball_counter'].astype(int)

df['count'] = df['ball_counter'].astype(str) + "-" + df['strike_counter'].astype(str)

df2 = df # Create a copy of the dataframe to work with. This df will be merged back in after adjustments

df2 = df2[['count']]

# Create a new DataFrame with the same columns as 'df2' and a single row with 'count' set to '0-0'. 
new_row = pd.DataFrame({'count': ['0-0']}, columns=df2.columns)

# Concatenate 'new_row' and 'df2' along the row axis (axis=0)
df2 = pd.concat([new_row, df2], ignore_index=True)

# Drop the last row
df2 = df2.iloc[:-1]

df = df.drop(columns={'ball_counter', 'strike_counter', 'count'})

# Merge the two dataframes back together
df = pd.merge(df, df2, left_index=True, right_index=True)


"""
This is where we write our dataframe back to the database as a new table to be reported on
"""

df.to_sql('dataentry_pitch2', engine, if_exists='replace', index=False)

engine.dispose()