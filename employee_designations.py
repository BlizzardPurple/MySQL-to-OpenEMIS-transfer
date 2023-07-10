import mysql.connector

class EmployeeDesignation:
    def __init__(self, id, created_at, updated_at):
        self.id = id
        self.created_at = created_at
        self.updated_at = updated_at

    def get_id(self):
        return self.id

    def get_created_at(self):
        return self.created_at

    def get_updated_at(self):
        return self.updated_at


class InstitutionStaffPositionProfile:
    def __init__(self, id, created, modified):
        self.id = id
        self.created = created
        self.modified = modified

    def get_id(self):
        return self.id

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

# Retrieve data from the source "employee_designations" table
source_cursor.execute("SELECT id, created_at, updated_at FROM employee_designations")
results = source_cursor.fetchall()

# Create a list of EmployeeDesignation objects with the retrieved data
employee_designations = []
for result in results:
    employee_designation = EmployeeDesignation(result[0], result[1], result[2])
    employee_designations.append(employee_designation)

# Transfer data to the target "institution_staff_position_profiles" table with mapping
for employee_designation in employee_designations:
    id = employee_designation.get_id()
    created = employee_designation.get_created_at()  # Mapping to created
    modified = employee_designation.get_updated_at()  # Mapping to modified

    # Create an InstitutionStaffPositionProfile object with the mapped data
    institution_staff_position_profile = InstitutionStaffPositionProfile(id, created, modified)

    # Insert the data into the target table
    target_cursor.execute(
        "INSERT INTO institution_staff_position_profiles (id, created, modified) VALUES (%s, %s, %s)",
        (institution_staff_position_profile.get_id(), institution_staff_position_profile.get_created(),
         institution_staff_position_profile.get_modified())
    )
    target_connection.commit()

# Close the cursors and connections
source_cursor.close()
target_cursor.close()
source_connection.close()
target_connection.close()

print("Data transfer complete!")
