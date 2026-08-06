# Automated Bill Generator

A lightweight command-line Point of Sale (POS) application built in Python to process customer orders, compute custom item discounts, apply standard sales tax, and print an official formatted retail receipt.

## Features
* Interactive console input parsing for customer data and product specifications.
* Type casting inputs safely into appropriate numeric data formats (`int`, `float`).
* Automated math logic for subtotals, proportional percentage discounts, and fixed tax rates (8%).
* Clean formatted text layout mimicking a standard store receipt.

## Core Concepts Covered
* Python Input/Output handling (`input`, `print`)
* Explicit data type casting (`int()`, `float()`)
* Basic arithmetic operators (`*`, `-`, `+`, `/`)
* Formatted string literals (`f-strings`) for decimal alignment

## How to Run
1. Make sure you have [Python](https://python.org) installed on your system.
2. Clone this repository or download the script file.
3. Open your terminal or command prompt.
4. Run the script using the command:
   ```bash
   python main.py
   ```

## Example Usage
```text
=== WELCOME TO THE RETAIL POINT OF SALE (POS) SYSTEM ===
Enter Customer Name: Alice
Enter Item Description: Wireless Mouse
Enter Item Quantity: 2
Enter Price Per Item (\$): 25.00
Enter Discount Percentage (e.g., 10 for 10%): 10

========================================
         OFFICIAL INVOICE               
========================================
Customer Name : Alice
Item Purchased : Wireless Mouse
Quantity : 2
Unit Price : \$25.00
----------------------------------------
Gross Subtotal : \$50.00
Discount Applied : -\$5.00 (10.0%)
Sales Tax (8%) : \$3.60
----------------------------------------
TOTAL AMOUNT DUE : \$48.60
========================================
Thank you for your business! Please come again.
========================================
```
