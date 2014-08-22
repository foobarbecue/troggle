from django.conf import settings
import csv, datetime

def addCSVToTimeSeries(pathToCSV):
    with open (pathToCSV) as timeSeries:
        timeSeriesReader=csv.reader(timeSeries)
        for dataPoint in timeSeries:
                print [datetime.datetime.strptime(dataPoint[1],'%Y-%m-%d %H:%M:%S'), datapoint[2].split(' ')