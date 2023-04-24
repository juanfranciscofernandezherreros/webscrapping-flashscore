import csv
import glob
import mysql.connector
import os

if __name__ == '__main__':
    directories = ['../csv/basketball/summary/', '../csv/basketball/lineups/']
    
    for directory in directories:
        csv_files = glob.glob(os.path.join(directory, '*.csv'))

        for filepath in csv_files:
            if os.path.isfile(filepath):
                filename = os.path.basename(filepath)
                print(filename)
