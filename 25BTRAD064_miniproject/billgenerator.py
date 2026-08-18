# =====================================================================
# MINI PROJECT: AUTOMATED BILL GENERATOR
# Core Concepts: Variables, Datatype Casting, Arithmetic Operators, I/O
# =====================================================================

# 1. INPUT SECTION: Gather transaction details
print("=== WELCOME TO THE RETAIL POINT OF SALE (POS) SYSTEM ===")
customer_name = input("Enter Customer Name: ")
item_name = input("Enter Item Description: ")

# Cast inputs into numbers to enable mathematical operators
quantity = int(input("Enter Item Quantity: "))
price_per_item = float(input("Enter Price Per Item ($): "))
discount_percentage = float(input("Enter Discount Percentage (e.g., 10 for 10%): "))

# 2. OPERATORS & PROCESSING SECTION: Calculate totals
# Multiplicative evaluation for initial cost
subtotal = quantity * price_per_item

# Percent-to-decimal reduction mapping for the savings deduction
discount_amount = subtotal * (discount_percentage / 100)
discounted_subtotal = subtotal - discount_amount

# Standard tax application modifier (applied at 8%)
sales_tax = discounted_subtotal * 0.08
final_bill_amount = discounted_subtotal + sales_tax

# 3. OUTPUT SECTION: Format and print the document string
print("\n" + "="*40)
print("             OFFICIAL INVOICE            ")
print("="*40)
print(f"Customer Name     : {customer_name}")
print(f"Item Purchased    : {item_name}")
print(f"Quantity          : {quantity}")
print(f"Unit Price        : ${price_per_item:.2f}")
print("-"*40)
print(f"Gross Subtotal    : ${subtotal:.2f}")
print(f"Discount Applied  : -${discount_amount:.2f} ({discount_percentage}%)")
print(f"Sales Tax (8%)    : ${sales_tax:.2f}")
print("-"*40)
print(f"TOTAL AMOUNT DUE  : ${final_bill_amount:.2f}")
print("="*40)
print("Thank you for your business! Please come again.")
print("="*40)

