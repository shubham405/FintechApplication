import csv

# Open the CSV file for reading
with open("transactions.csv", "r") as csv_file:
    csv_reader = csv.reader(csv_file)
    next(csv_reader)  # Skip the header row if it exists

    # Insert data into the SQLite table
    for row in csv_reader:
        insert_query = f"""
            INSERT INTO TRANSACTIONS (CC_NUM, First_Name, Last_Name,Trans_num,
            Trans_date,Trans_time,Unix_time,Category,
            Merchant,Amount,Merch_lat,Merch_long,Is_fraud
            )
            VALUES (?, ?, ?,?,?,?,?,?,?,?,?,?,?);
        """
        cursor_obj.execute(insert_query, row)