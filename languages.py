import mysql.connector

class Language:
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


class UserLanguage:
    def __init__(self, id, evaluation_date, language_id, listening, speaking, reading, writing, security_user_id,
                 modified_user_id, modified, created_user_id, created):
        self.id = id
        self.evaluation_date = evaluation_date
        self.language_id = language_id
        self.listening = listening
        self.speaking = speaking
        self.reading = reading
        self.writing = writing
        self.security_user_id = security_user_id
        self.modified_user_id = modified_user_id
        self.modified = modified
        self.created_user_id = created_user_id
        self.created = created

    def get_id(self):
        return self.id

    def get_evaluation_date(self):
        return self.evaluation_date

    def get_language_id(self):
        return self.language_id

    def get_listening(self):
        return self.listening

    def get_speaking(self):
        return self.speaking

    def get_reading(self):
        return self.reading

    def get_writing(self):
        return self.writing

    def get_security_user_id(self):
        return self.security_user_id

    def get_modified_user_id(self):
        return self.modified_user_id

    def get_modified(self):
        return self.modified

    def get_created_user_id(self):
        return self.created_user_id

    def get_created(self):
        return self.created


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

# Retrieve data from the source "languages" table
source_cursor.execute("SELECT id, created_at, updated_at FROM languages")
results = source_cursor.fetchall()

# Create a list of Language objects with the retrieved data
languages = []
for result in results:
    language = Language(result[0], result[1], result[2])
    languages.append(language)

# Transfer data to the target "user_languages" table and mapping type
for language in languages:
    language_id = language.get_id()
    created_at = language.get_created_at()
    updated_at = language.get_updated_at()

    # Create a UserLanguage object with the mapped data
    user_language = UserLanguage(language_id, None, language_id, None, None, None, None, None, None,
                                 None, None, created_at)

    # Insert the data into the target table
    target_cursor.execute("""
        INSERT INTO user_languages (id, evaluation_date, language_id, listening, speaking, reading, writing,
                                   security_user_id, modified_user_id, modified, created_user_id, created)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """, (
        user_language.get_id(),
        user_language.get_evaluation_date(),
        user_language.get_language_id(),
        user_language.get_listening(),
        user_language.get_speaking(),
        user_language.get_reading(),
        user_language.get_writing(),
        user_language.get_security_user_id(),
        user_language.get_modified_user_id(),
        user_language.get_modified(),
        user_language.get_created_user_id(),
        user_language.get_created()
    ))

# Commit the changes to the target database
target_connection.commit()

# Close the cursors and database connections
source_cursor.close()
target_cursor.close()
source_connection.close()
target_connection.close()

