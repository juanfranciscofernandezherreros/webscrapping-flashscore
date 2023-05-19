import os
import csv

# Define the root directory where you want to start searching for CSV files
root_directory = 'csv/basketball'

# List to store the data from all CSV files
all_data = []

# List to store the file names
file_names = []

# Recursively traverse the directory tree
for root, dirs, files in os.walk(root_directory):
    for file in files:
        if file.endswith('.csv'):  # Check if the file is a CSV file
            file_path = os.path.join(root, file)  # Get the absolute file path

            # Read the CSV file and store the data in a list of lists
            with open(file_path, newline='') as csv_file:
                reader = csv.reader(csv_file)
                file_data = [row for row in reader]
                all_data.extend(file_data)

            # Store the file name
            file_names.append(file)

# Access the data from all CSV files
for file_name, row in zip(file_names, all_data):
    print("File:", file_name)
    # Print values of each row
    for value in row:
        print(value)
    print("---------")
