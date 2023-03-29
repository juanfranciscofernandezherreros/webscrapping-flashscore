import csv
import glob

def read_csv_files(csv_files):
    all_data = []
    processed_rows = set() # To keep track of already processed rows
    
    for file in csv_files:
        print("File" + file)
        with open(file, newline='') as csvfile:
            reader = csv.reader(csvfile, delimiter=';', quotechar='"')
            next(reader) # Skip header row
            for row in reader:
                row_tuple = tuple(row) # Convert row to tuple for set comparison
                if row_tuple not in processed_rows: # Check if row is not already processed
                    all_data.append(row) # Add row to all_data
                    processed_rows.add(row_tuple) # Add row to processed rows set
    
    return all_data

if __name__ == '__main__':
    csv_files = glob.glob('spain_acb_*.csv')
    all_data = read_csv_files(csv_files)
