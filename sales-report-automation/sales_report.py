import csv

total_revenue = 0

with open("sales.csv", "r", newline="") as file:
    reader = csv.DictReader(file)

    for row in reader:
        quantity = int(row["Quantity"])
        price = float(row["Price"])
        revenue = quantity * price

        total_revenue += revenue

        print(row["Product"], "Revenue:", revenue)

print("Total Revenue:", total_revenue)
