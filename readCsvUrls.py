import csv
import mysql.connector
import searchUrls

def main(my_array):
    for item in my_array:
        print("Item" + item)
        searchUrls.get_hrefs(item,6,"a")
if __name__ == "__main__":
    sendArray = []
    main(sendArray)
