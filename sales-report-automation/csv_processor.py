
import csv

with open("sales.csv", "r", newline="") as file:
    reader = csv.DictReader(file)

    for row in reader:
        quantity = row["Quantity"]
        price = row["Price"]

        if not quantity or not price:
            print("Incomplete record:", row)
            continue

        quantity = int(quantity)
        price = float(price)

        revenue = quantity * price

        print(row["Product"], "Revenue:", revenue)