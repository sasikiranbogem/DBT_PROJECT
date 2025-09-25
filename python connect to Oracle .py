import cx_Oracle
import csv

# ----------------------------
# Oracle Database Connection
# ----------------------------
username = "your_username"
password = "your_password"
dsn = "localhost/orclpdb"   # Example: "hostname:port/service_name"
port = 1521                 # Default Oracle port

# Connect to Oracle
connection = cx_Oracle.connect(user=username, password=password, dsn=dsn)
cursor = connection.cursor()

# ----------------------------
# SQL Query
# ----------------------------
query = "SELECT * FROM employees"   
cursor.execute(query)

# ----------------------------
# Write Data to CSV
# ----------------------------
csv_file = "oracle_data.csv"

with open(csv_file, "w", newline="") as file:
    writer = csv.writer(file)

    # Write header
    header = [col[0] for col in cursor.description]
    writer.writerow(header)

    # Write data rows
    for row in cursor:
        writer.writerow(row)

print(f"✅ Data exported successfully to {csv_file}")

# ----------------------------
# Close connection
# ----------------------------
cursor.close()
connection.close()
