import mysql.connector

class Bank:
    def __init__(self, id, name, created_at, updated_at):
        self.id = id
        self.name = name
        self.created_at = created_at
        self.updated_at = updated_at

    def get_id(self):
        return self.id

    def get_name(self):
        return self.name

    def get_created_at(self):
        return self.created_at

    def get_updated_at(self):
        return self.updated_at


class BanksTable:
    def __init__(self, bankID, bankName, entry_created_at, entry_updated_at):
        self.bankID = bankID
        self.bankName = bankName
        self.bankLocation = None
        self.bankStake = None
        self.entry_created_at = entry_created_at
        self.entry_updated_at = entry_updated_at

    def get_bankID(self):
        return self.bankID

    def get_bankName(self):
        return self.bankName

    def get_bankLocation(self):
        return self.bankLocation

    def get_bankStake(self):
        return self.bankStake

    def get_entry_created_at(self):
        return self.entry_created_at

    def get_entry_updated_at(self):
        return self.entry_updated_at

    def data_BanksTable(self):
        return ( self.get_bankID(),self.get_bankName(),self.get_bankLocation(),self.get_bankStake(),self.get_entry_created_at(),self.get_entry_updated_at())

    add_BanksTable = """
        INSERT INTO banksTable (bankID, bankName, bankLocation, bankStake, entry_created_at, entry_updated_at)
        VALUES (%s, %s, %s, %s, %s, %s)
    """

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

# Retrieve data from the source "banks" table
source_cursor.execute("SELECT id, name, created_at, updated_at FROM banks")
results = source_cursor.fetchall()

# Create a list of Bank objects with the retrieved data
banks = []
for result in results:
    bank = Bank(result[0], result[1], result[2], result[3])
    banks.append(bank)

# Transfer data to the target "banksTable" table and mapping type
for bank in banks:
    bankID = bank.get_id()
    bankName = bank.get_name()
    entry_created_at = bank.get_created_at()
    entry_updated_at = bank.get_updated_at()

    # Create a BanksTable object with the mapped data
    banks_table = BanksTable(bankID, bankName, entry_created_at, entry_updated_at)

    # Insert the data into the target table
    target_cursor.execute(banks_table.add_BanksTable, banks_table.data_BanksTable())
    target_connection.commit()

# Close the cursors and connections
source_cursor.close()
target_cursor.close()
source_connection.close()
target_connection.close()

print("Data transfer complete!")
