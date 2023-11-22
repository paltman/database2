# database2
dataBase

Requirements -> django & psycopg2-binary

# had some trouble with the customuser. had to 
# 1. comment out all references to User
# 2. run python3 manage.py migrate auth zero to reset all the auth stuff 
# 3. run python3 manage.py migrate dataentry to migrate new customuser to database succesfully