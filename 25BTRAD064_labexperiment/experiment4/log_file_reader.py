def read_log_file(filename):
    counts = {"ERROR": 0, "WARNING": 0, "INFO": 0}
 
    try:
        with open(filename, "r", encoding="utf-8") as file:
            for line in file:
                upper_line = line.upper()
                for keyword in counts:
                    if keyword in upper_line:
                        counts[keyword] += 1
 
        print("Log Summary")
        print("-----------")
        for keyword, count in counts.items():
            print(f"{keyword}: {count}")
 
    except FileNotFoundError:
        print(f"Error: The file '{filename}' was not found.")
    except OSError as error:
        print(f"Unable to read the file: {error}")
 
if __name__ == "__main__":
    read_log_file("application.log")
