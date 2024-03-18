import csv
from datetime import datetime

def saveDataToCsv(filePath, allData):
    stringData = ""
    currentTime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    for data in allData:
        stringData += data + ","

    with open(filePath, 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([stringData, currentTime])