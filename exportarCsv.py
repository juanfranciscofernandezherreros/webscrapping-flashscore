import csv

def exportarCsv(player_data, header, filename):
    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([header])
        for data in player_data:
            writer.writerow(data)
