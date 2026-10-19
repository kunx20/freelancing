import csv

valid_records = []
seen_records = set()

with open("sales.csv", "r", newline="") as file:
    reader = csv.DictReader(file)

    for row in reader:
        product = (row.get("Product") or "").strip()
        quantity_text = (row.get("Quantity") or "").strip()
        price_text = (row.get("Price") or "").strip()

        # Check for missing values
        if not product or not quantity_text or not price_text:
            print("Incomplete record:", row)
            continue

        # Check whether quantity and price are numeric
        try:
            quantity = int(quantity_text)
            price = float(price_text)
        except ValueError:
            print("Invalid number:", row)
            continue

        # Check business rules
        if quantity <= 0 or price < 0:
            print("Invalid quantity or price:", row)
            continue

        # Detect exact duplicate records
        record_key = (product.lower(), quantity, price)

        if record_key in seen_records:
            print("Duplicate record:", row)
            continue

        seen_records.add(record_key)

        valid_records.append({
            "Product": product,
            "Quantity": quantity,
            "Price": price
        })

# Save validated records
with open("validated_sales.csv", "w", newline="") as file:
    fieldnames = ["Product", "Quantity", "Price"]

    writer = csv.DictWriter(file, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(valid_records)

print("\nValidation completed!")
print("Valid records:", len(valid_records))
print("Output saved to validated_sales.csv")