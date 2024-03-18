import csv
import json
from sqlalchemy import create_engine, MetaData, Table, select, func, join

# Connect to the database
engine = create_engine("mysql+pymysql://codetest:swordfish@database/codetest")
connection = engine.connect()

metadata = MetaData(engine)

# Define the table structures
places_table = Table('places', metadata, autoload=True, autoload_with=engine)
people_table = Table('people', metadata, autoload=True, autoload_with=engine)

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
