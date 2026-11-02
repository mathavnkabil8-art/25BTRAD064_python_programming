import csv
 
INPUT_FILE = "employees.csv"
OUTPUT_FILE = "payroll_summary.csv"
DEDUCTION_RATE = 0.10
 
def process_payroll():
    total_gross = 0.0
    total_deductions = 0.0
    total_net = 0.0
 
    try:
        with open(INPUT_FILE, "r", newline="", encoding="utf-8") as infile:
            reader = csv.DictReader(infile)
            with open(OUTPUT_FILE, "w", newline="", encoding="utf-8") as outfile:
                fields = ["employee_id", "name", "basic_salary",
                          "gross_salary", "deductions", "net_salary"]
                writer = csv.DictWriter(outfile, fieldnames=fields)
                writer.writeheader()
 
                for row in reader:
                    try:
                        basic = float(row["basic_salary"])
                        allowance = float(row["allowance"])
                        if basic < 0 or allowance < 0:
                            print("Skipping negative salary for", row["name"])
                            continue
                    except (ValueError, KeyError):
                        print("Skipping invalid employee record.")
                        continue
 
                    gross = basic + allowance
                    deductions = gross * DEDUCTION_RATE
                    net = gross - deductions
 
                    writer.writerow({
                        "employee_id": row["employee_id"],
                        "name": row["name"],
                        "basic_salary": f"{basic:.2f}",
                        "gross_salary": f"{gross:.2f}",
                        "deductions": f"{deductions:.2f}",
                        "net_salary": f"{net:.2f}"
                    })
                    total_gross += gross
                    total_deductions += deductions
                    total_net += net
 
        print(f"Total gross salary: {total_gross:.2f}")
        print(f"Total deductions: {total_deductions:.2f}")
        print(f"Total net salary: {total_net:.2f}")
        print(f"Payroll saved to {OUTPUT_FILE}")
 
    except FileNotFoundError:
        print(f"Error: {INPUT_FILE} was not found.")
 
if __name__ == "__main__":
    process_payroll()
