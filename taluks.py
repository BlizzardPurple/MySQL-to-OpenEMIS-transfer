#completed

import mysql.connector

class Taluk:
    def __init__(self, id, taluk_code, taluk_name, revenue_district_id, created_at, updated_at):
        self.id = id
        self.taluk_code = taluk_code
        self.taluk_name = taluk_name
        self.revenue_district_id = revenue_district_id
        self.created_at = created_at
        self.updated_at = updated_at

    def get_id(self):
        return self.id

    def get_taluk_code(self):
        return self.taluk_code

    def get_taluk_name(self):
        return self.taluk_name

    def get_revenue_district_id(self):
        return self.revenue_district_id

    def get_created_at(self):
        return self.created_at

    def get_updated_at(self):
        return self.updated_at


class Area:
    def __init__(self, id, code, name, area_level_id, created, modified):
        self.id = id
        self.code = code
        self.name = name
        self.area_level_id = area_level_id
        self.created = created
        self.modified = modified

    def get_id(self):
        return self.id

    def get_code(self):
        return self.code

    def get_name(self):
        return self.name

    def get_area_level_id(self):
        return self.area_level_id

    def get_created(self):
        return self.created

    def get_modified(self):
        return self.modified


# Connect to source and target databases
source_connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="password",
    database="sampoorna"
)

target_connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="password",
    database="sampoorna2"
)

# Create cursors for source and target databases
source_cursor = source_connection.cursor()
target_cursor = target_connection.cursor()

# Retrieve data from the source "taluks" table
source_cursor.execute("SELECT id, taluk_code, taluk_name, revenue_district_id, created_at, updated_at FROM taluks")
results = source_cursor.fetchall()

# Create a list of Taluk objects with the retrieved data
taluks = []
for result in results:
    taluk = Taluk(result[0], result[1], result[2], result[3], result[4], result[5])
    taluks.append(taluk)

# Transfer data to the target "areas" table with mapping
for taluk in taluks:
    id = taluk.get_id()
    code = taluk.get_taluk_code()
    name = taluk.get_taluk_name()
    area_level_id = taluk.get_revenue_district_id()  # Mapping to area_level_id
    created = taluk.get_created_at()  # Mapping to created
    modified = taluk.get_updated_at()  # Mapping to modified

    # Create an Area object with the mapped data
    area = Area(id, code, name, area_level_id, created, modified)

    # Insert the data into the target table
    target_cursor.execute(
        "INSERT INTO areas (id, code, name, area_level_id, created, modified) VALUES (%s, %s, %s, %s, %s, %s)",
        (area.get_id(), area.get_code(), area.get_name(), area.get_area_level_id(), area.get_created(), area.get_modified()))
    target_connection.commit()

# Close the cursors and connections
source_cursor.close()
target_cursor.close()
source_connection.close()
target_connection.close()

print("Data transfer complete!")

