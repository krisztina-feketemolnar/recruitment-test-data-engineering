import csv
import json
from sqlalchemy import create_engine, MetaData, Table, select, func, join

# Connect to the database
engine = create_engine("mysql+pymysql://codetest:localhost@database/codetest")
connection = engine.connect()

metadata = MetaData(engine)

# Define the table structures
places_table = Table('places', metadata, autoload=True, autoload_with=engine)
people_table = Table('people', metadata, autoload=True, autoload_with=engine)

# Truncate the 'people' table before inserting new data
connection.execute(people_table.delete())

# Truncate the 'places' table before inserting new data
connection.execute(places_table.delete())

# Read the CSV data file into the 'people' table
with open('/data/people.csv') as csv_file:
    reader = csv.reader(csv_file)
    next(reader)  # Skip header
    for row in reader:
        connection.execute(people_table.insert().values(name=row[0]))

# Read the CSV data file into the 'places' table
with open('/data/places.csv') as csv_file:
    reader = csv.reader(csv_file)
    next(reader)  # Skip header
    for row in reader:
        connection.execute(places_table.insert().values(name=row[0]))

# Define the join condition
join_condition = people_table.columns.place_of_birth == places_table.columns.city

# Define the SQL query
query = select([places_table.columns.country, func.count(people_table.columns.place_of_birth)]) \
    .select_from(people_table.join(places_table, join_condition)) \
    .group_by(places_table.columns.country)

# Execute the query
result = connection.execute(query).fetchall()

# Output the query result to a JSON file
output_data = [{'country': row[0], 'count': int(row[1])} for row in result]
with open('/data/summary_output.json', 'w') as json_file:
    json.dump(output_data, json_file, separators=(',', ':'))

# Close the database connection
connection.close()


''' 
import csv
import json
import sqlalchemy
from sqlalchemy import func, select

# connect to the database
engine = sqlalchemy.create_engine("mysql://codetest:swordfish@database/codetest")
connection = engine.connect()

metadata = sqlalchemy.schema.MetaData(engine)

# make an ORM object to refer to the table
Places = sqlalchemy.schema.Table('places', metadata, autoload=True, autoload_with=engine)
People = sqlalchemy.schema.Table('people', metadata, autoload=True, autoload_with=engine)

# Truncate the 'people' table
connection.execute(People.delete())

# Truncate the 'places' table
connection.execute(Places.delete())

# read the CSV data file into the 'people' table
with open('/data/people.csv') as csv_file:
    reader = csv.reader(csv_file)
    next(reader)
    for row in reader:
        connection.execute(People.insert().values(name=row[0]))

# read the CSV data file into the 'places' table
with open('/data/places.csv') as csv_file:
    reader = csv.reader(csv_file)
    next(reader)
    for row in reader:
        connection.execute(Places.insert().values(name=row[0]))

# Define the join condition
join_condition = People.columns.place_of_birth == Places.columns.city

# Define the SQL query
query = select([Places.columns.country, func.count(People.columns.place_of_birth)]) \
    .select_from(People.join(Places, join_condition)) \
    .group_by(Places.columns.country)

# Execute the query
result = connection.execute(query).fetchall()

# Output the query result to a JSON file
output_data = [{'country': row[0], 'count': int(row[1])} for row in result]
with open('/data/summary_output.json', 'w') as json_file:
    json.dump(output_data, json_file, separators=(',', ':'))

# Close the database connection
connection.close()
'''