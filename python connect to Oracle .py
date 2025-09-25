import cx_Oracle
import csv
import os
import logging

# ----------------------------
# Logging Setup
# ----------------------------
logging.basicConfig(
    filename="oracle_extract.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# ----------------------------
# Oracle Database Connection
# ----------------------------
try:
    username = os.getenv("ORACLE_USER", "your_username")
    password = os.getenv("ORACLE_PASS", "your_password")
    dsn = "localhost/orclpdb"   # Example: "hostname:port/service_name"

    connection = cx_Oracle.connect(user=username, password=password, dsn=dsn)
    cursor = connection.cursor()
    logging.info("✅ Connected to Oracle Database successfully")

except Exception as e:
    logging.error(f"❌ Database connection failed: {e}")
    raise

# ----------------------------
# SQL Query
# ----------------------------
query = "SELECT * FROM employees"

try:
    cursor.execute(query)
    logging.info(f"Executed query: {query}")
except Exception as e:
    logging.error(f"❌ Query failed: {e}")
    raise

# ----------------------------
# Write Data to CSV
# ----------------------------
csv_file = "oracle_data.csv"

try:
    with open(csv_file, "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)

        # Write header
        header = [col[0] for col in cursor.description]
        writer.writerow(header)

        # Write data in chunks (better for large datasets)
        while True:
            rows = cursor.fetchmany(500)  # fetch 500 rows at a time
            if not rows:
                break
            writer.writerows(rows)

    logging.info(f"✅ Data exported successfully to {csv_file}")

except Exception as e:
    logging.error(f"❌ Failed to write data to CSV: {e}")
    raise

finally:
    # ----------------------------
    # Close connection
    # ----------------------------
    cursor.close()
    connection.close()
    logging.info("🔒 Database connection closed")
