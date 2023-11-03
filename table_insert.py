import sqlite3


def create_connection(db_file):
    """create a database connection to the SQLite database
        specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Exception as e:
        print(e)
    return conn


connection_obj = create_connection("db.sqlite3")

# cursor object
cursor_obj = connection_obj.cursor()

# Creating table
table = """ CREATE TABLE IF NOT EXISTS TRANSACTIONS  (
            CC_NUM VARCHAR(255) NOT NULL,
            First_Name CHAR(50) NOT NULL,
            Last_Name CHAR(50),
            Trans_num VARCHAR(255),
            Trans_date DATETIME,
            Trans_time TEXT,
            Unix_time INT,
            Category TEXT,
            Merchant TEXT,
            Amount REAL,
            Merch_lat REAL,
            Merch_long REAL,
            Is_fraud INT
        ); """

cursor_obj.execute(table)

# import csv

# # Open the CSV file for reading
# with open("transactions.csv", "r") as csv_file:
#     csv_reader = csv.reader(csv_file)
#     next(csv_reader)  # Skip the header row if it exists

#     # Insert data into the SQLite table
#     for row in csv_reader:
#         insert_query = f"""
#             INSERT INTO TRANSACTIONS (CC_NUM, First_Name, Last_Name,Trans_num,
#             Trans_date,Trans_time,Unix_time,Category,
#             Merchant,Amount,Merch_lat,Merch_long,Is_fraud
#             )
#             VALUES (?, ?, ?,?,?,?,?,?,?,?,?,?,?);
#         """
#         cursor_obj.execute(insert_query, row)
#         #cursor_obj.commit()
cursor_obj.execute("SELECT * FROM TRANSACTIONS")

#Fetch all rows from the result
rows = cursor_obj.fetchall()

#Iterate through the rows and print the data
for row in rows:
    print(row[len(row)-1])
cursor_obj.close()
