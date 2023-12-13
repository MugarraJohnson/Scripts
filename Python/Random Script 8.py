import re

def logs():
    result = []
    with open('D:\\logdata.txt', "r") as file:  # Use double backslashes
        for line in file:
            # Define a regular expression pattern to match log entries
            pattern = r'(?P<host>[\d\.]+)\s+(?P<user_name>[\w-]+|-)\s+(?P<time>\[[^\]]+\])\s+"(?P<request>[A-Z]+[^"]+)"'
            
            # Use the re.match() function to match log entries in each line
            match = re.match(pattern, line)
            if match:
                log_dict = match.groupdict()
                result.append(log_dict)
                
    return result

# Call the function and get the list of dictionaries
log_entries = logs()

# Print the number of log entries
print("Number of log entries:", len(log_entries))


# If the count is not 979, you can check the first few entries for discrepancies
for i, entry in enumerate(log_entries[:10]):
    print(f"Entry {i + 1}: {entry}")

def logs():
    result = []
    with open(r'D:\logdata.txt', "r") as file:  # Use a raw string (prefix with 'r')
        for line in file:
            # Define a regular expression pattern to match log entries
            pattern = r'(?P<host>[\d\.]+)\s+(?P<user_name>[\w-]+|-)\s+(?P<time>\[[^\]]+\])\s+"(?P<request>[A-Z]+[^"]+)"'
            
            # Use the re.match() function to match log entries in each line
            match = re.match(pattern, line)
            if match:
                log_dict = match.groupdict()
                result.append(log_dict)
                
    return result

# Call the function and get the list of dictionaries
log_entries = logs()

# Print the number of log entries
print("Number of log entries:", len(log_entries))




import re

def logs():
    result = []
    with open('D:\\logdata.txt', "r") as file:
        for line in file:
            # Define a regular expression pattern to match the log entries
            pattern = r'(?P<host>[\d\.]+) - (?P<user_name>[\w-]+) \[(?P<time>[^\]]+)\] "(?P<request>[^"]+)"'
            
            # Use the re.search() function to find log entries in each line
            match = re.search(pattern, line)
            if match:
                log_dict = match.groupdict()
                result.append(log_dict)
                
    return result

# Call the function and get the list of dictionaries
log_entries = logs()

# Print the number of log entries
print("Number of log entries:", len(log_entries))

