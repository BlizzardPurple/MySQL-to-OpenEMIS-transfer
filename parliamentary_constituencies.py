import mysql.connector

class ParliamentaryConstituency:
    def __init__(self, id, name, state_id, created_at, updated_at):
        self.id = id
        self.name = name
        self.state_id = state_id
        self.created_at = created_at
        self.updated_at = updated_at

    def get_id(self):
        return self.id

    def get_name(self):
        return self.name

    def get_state_id(self):
        return self.state_id

    def get_created_at(self):
        return self.created_at

    def get_updated_at(self):
        return self.updated_at


class AreaLevel:
    def __init__(self, id, name, level, created, modified):
        self.id = id
        self.name = name
        self.level = level
        self.created = created
        self.modified = modified

    def get_id(self):
        return self.id

    def get_name(self):
        return self.name

    def get_level(self):
        return self.level

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

# Retrieve data from the source "parliamentary_constituencies" table
source_cursor.execute("SELECT id, name, state_id, created_at, updated_at FROM parliamentary_constituencies")
results = source_cursor.fetchall()

# Create a list of ParliamentaryConstituency objects with the retrieved data
parliamentary_constituencies = []
for result in results:
    parliamentary_constituency = ParliamentaryConstituency(result[0], result[1], result[2], result[3], result[4])
    parliamentary_constituencies.append(parliamentary_constituency)

# Transfer data to the target "area_levels" table with mapping
for parliamentary_constituency in parliamentary_constituencies:
    id = parliamentary_constituency.get_id()
    name = parliamentary_constituency.get_name()
    level = parliamentary_constituency.get_state_id()  # Mapping to level
    created = parliamentary_constituency.get_created_at()  # Mapping to created
    modified = parliamentary_constituency.get_updated_at()  # Mapping to modified

    # Create an AreaLevel object with the mapped data
    area_level = AreaLevel(id, name, level, created, modified)

    # Insert the data into the target table
    target_cursor.execute(
        "INSERT INTO area_levels (id, name, level, created, modified) VALUES (%s, %s, %s, %s, %s)",
        (area_level.get_id(), area_level.get_name(), area_level.get_level(), area_level.get_created(),
         area_level.get_modified())
    )
    target_connection.commit()

# Close the cursors and connections
source_cursor.close()
target_cursor.close()
source_connection.close()
target_connection.close()

print("Data transfer complete!")
