
def find_product(products, name):
    """Return a product if its name exists; otherwise return None."""
    for product in products:
        if product["name"].casefold() == name.casefold():
            return product
    return None


def add_or_update_product(products):
    """Add a new product or update an existing product."""
    name = input("Enter product name: ").strip()

    if not name:
        print("Product name cannot be empty.")
        return

    try:
        quantity = int(input("Enter total quantity sold: "))
        price = float(input("Enter unit price (Rs.): "))

        if quantity < 0 or price < 0:
            print("Quantity and price cannot be negative.")
            return

    except ValueError:
        print("Invalid input. Enter a whole number for quantity and a number for price.")
        return

    existing = find_product(products, name)

    if existing:
        choice = input(
            "Product exists. Replace its quantity and price? (y/n): "
        ).strip().lower()

        if choice == "y":
            existing["quantity"] = quantity
            existing["price"] = price
            print("Product record updated successfully.")
        else:
            print("Update cancelled.")
    else:
        products.append({
            "name": name,
            "quantity": quantity,
            "price": price
        })
        print("Product added successfully.")


def display_records(products):
    """Display all product sales records."""
    if not products:
        print("No sales records available.")
        return

    print("\nSALES RECORDS")
    print("-" * 64)
    print("{:<20} {:>12} {:>14} {:>16}".format(
        "Product", "Qty Sold", "Unit Price", "Revenue (Rs.)"
    ))
    print("-" * 64)

    for product in products:
        revenue = product["quantity"] * product["price"]
        print("{:<20} {:>12} {:>14.2f} {:>16.2f}".format(
            product["name"],
            product["quantity"],
            product["price"],
            revenue
        ))

    print("-" * 64)


def show_sales_summary(products):
    """Calculate and display the sales summary."""
    if not products:
        print("No sales records available to summarize.")
        return

    total_quantity = sum(
        product["quantity"] for product in products
    )

    total_revenue = sum(
        product["quantity"] * product["price"]
        for product in products
    )

    highest_selling = max(
        products, key=lambda product: product["quantity"]
    )

    highest_revenue = max(
        products,
        key=lambda product: product["quantity"] * product["price"]
    )

    print("\nSALES SUMMARY")
    print("-" * 40)
    print("Number of products:", len(products))
    print("Total quantity sold:", total_quantity)
    print("Total revenue: Rs. {:.2f}".format(total_revenue))

    print("Highest-selling product by quantity: {} ({} units)".format(
        highest_selling["name"],
        highest_selling["quantity"]
    ))

    print("Product with highest revenue: {} (Rs. {:.2f})".format(
        highest_revenue["name"],
        highest_revenue["quantity"] * highest_revenue["price"]
    ))

    print("\nProduct-wise performance:")

    for product in sorted(
        products,
        key=lambda item: item["quantity"] * item["price"],
        reverse=True
    ):
        revenue = product["quantity"] * product["price"]
        print("- {}: {} units, revenue Rs. {:.2f}".format(
            product["name"],
            product["quantity"],
            revenue
        ))


def main():
    # Sample records for demonstration.
    products = [
        {"name": "Notebook", "quantity": 20, "price": 45.00},
        {"name": "Pen", "quantity": 50, "price": 10.00},
        {"name": "File", "quantity": 15, "price": 30.00}
    ]

    while True:
        print("\n===== SALES DATA ANALYZER =====")
        print("1. Add or update product")
        print("2. Display all sales records")
        print("3. Show sales summary")
        print("4. Exit")

        choice = input("Enter your choice (1-4): ").strip()

        if choice == "1":
            add_or_update_product(products)

        elif choice == "2":
            display_records(products)

        elif choice == "3":
            show_sales_summary(products)

        elif choice == "4":
            print("Thank you for using Sales Data Analyzer.")
            break

        else:
            print("Invalid choice. Please enter a number from 1 to 4.")


if __name__ == "__main__":
    main()
