'''This script will be set to always running on our server. Will use it to pull in and wrangle the database data before outputting it again to our final table
that we will use for reporting'''

'''This script will be set to always running on our server. Will use it to pull in and wrangle the database data before 
outputting it again to our final table
that we will use for reporting'''

import pandas as pd
from sqlalchemy import URL, create_engine

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

df2 = df.copy()
df2['test'] = 'yo'

df2.to_sql('dataentry_pitch2', engine, if_exists='replace', index=False)

engine.dispose()