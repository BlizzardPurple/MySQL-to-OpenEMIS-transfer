import mysql.connector

# Establish database connections for source and target
source_connection = mysql.connector.connect(host='localhost', user='root', password='password', database='sampoorna')
target_connection = mysql.connector.connect(host='localhost', user='root', password='password', database='sampoorna2')

# Create cursors for source and target databases
source_cursor = source_connection.cursor()
target_cursor = target_connection.cursor()

# Fetch data from the source "reports" table
source_cursor.execute("SELECT * FROM reports")
reports = source_cursor.fetchall()

# Transfer data to the target "report_cards" table and mapping type
for report in reports:
    report_id = report[0]
    name = report[1]
    created_at = report[3]
    updated_at = report[4]
    model = report[5]

    # Insert the data into the target table
    target_cursor.execute("""
        INSERT INTO report_cards (id, code, name, description, start_date, end_date, generate_start_date,
                                 generate_end_date, principal_comments_required, homeroom_teacher_comments_required,
                                 teacher_comments_required, excel_template_name, excel_template, pdf_page_number,
                                 academic_period_id, education_grade_id, modified_user_id, modified,
                                 created_user_id, created)
        VALUES (%s, NULL, %s, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, %s, NULL, %s)
    """, (
        report_id,
        name,
        created_at,
        updated_at
    ))

# Commit the changes to the target database
target_connection.commit()

# Close the cursors and database connections
source_cursor.close()
target_cursor.close()
source_connection.close()
target_connection.close()
