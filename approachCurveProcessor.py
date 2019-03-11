import os
import matplotlib.pyplot as plotter
import pandas as pd
from string import digits

def Main():

    probeTipDiameter = 25;

    dirpaths, fileNames, filepaths = GetFilepathArray(os.getcwd(), ['csv'])

    if len(filepaths) != 0:

        for path in filepaths:
            with open(path) as file:
                rawData = file.readlines()

        data = []

        for line in rawData:
            data.append(line.split(', '))

        dataTable = DataTable(data)

        distanceData = dataTable.getColumn(dataTable.headers[1])[1:]
        currentData = dataTable.getColumn(dataTable.headers[2])[1:]

        curveStartIndexs = []

        for i in range(0, len(distanceData)):
            if float(distanceData[i]) == 0:
                curveStartIndexs.append(i)

        distanceArrays = []
        currentArrays = []
        approachDistances = []

        indexRange = curveStartIndexs[1] - curveStartIndexs[0]

        # stores the separate approach curves in to different arrays
        for i in range(0, len(curveStartIndexs)):
            distanceArrays.append(distanceData[curveStartIndexs[i]:(curveStartIndexs[i] + indexRange)])
            currentArrays.append(currentData[curveStartIndexs[i]:(curveStartIndexs[i] + indexRange)])

        # collects the approach distances of each curve (these should be the same)
        for curve in distanceArrays:
            approachDistances.append(min([float(i) for i in curve]))

        file = open('parsedApproachCurve.csv', 'w')

        lines = []
        titleLine = ''
        headerLine = ''

        for curveIndex in range(0, len(distanceArrays)):
            distanceHeader = dataTable.headers[1]
            currentHeader = dataTable.headers[2]

            titleLine += 'Curve, ' + str(curveIndex) + ', , , , '
            headerLine += distanceHeader + ', ' + currentHeader + ', norm distance, norm current, , '

        titleLine += '\r'
        headerLine += '\r'

        file.write(titleLine)
        file.write(headerLine)

        # loops thru the curves by row
        for rowIndex in range(0, len(distanceArrays[0])):

            line = ''

            # loops thru each curve to get its distance and current
            for curveIndex in range(0, len(distanceArrays)):

                distanceValue = distanceArrays[curveIndex][rowIndex]
                currentValue = currentArrays[curveIndex][rowIndex]
                normDistanceValue = (float(distanceValue) - float(approachDistances[curveIndex]))/(probeTipDiameter/2/1000)
                normCurrentValue = float(currentValue) / float(currentArrays[curveIndex][0])

                line += distanceValue + ', ' + currentValue + ', ' + str(normDistanceValue) + ', ' + str(normCurrentValue) + ', , '

            line += '\r'
            lines.append(line)

        file.writelines(lines)

        file.close()

        xAxisLabel = 'Distance'
        yAxisLabel = 'Current'

        # plotter.figure(figsize=(11, 8.5), dpi=600)

        shouldPreview = boolQuestion('would you like to preview the plots?')
        shouldSmooth = boolQuestion('Should I smooth the plots?')

        smoothIterations = 0
        if shouldSmooth:
            smoothIterations = intQuestion('How many time should I apply the smooth operation?')

        exclude = input('which curve should i not plot?').split(' ')

        probeRadAboveSurfaceIndex = 0

        for i in range(0, len(distanceArrays[0])):
            if float(distanceArrays[0][i]) == probeTipDiameter/2/1000:
                probeRadAboveSurfaceIndex = i
                print(probeRadAboveSurfaceIndex)
                break

        for i in range(0, len(distanceArrays)-1):

            if shouldSmooth:
                currentArrays[i], distanceArrays[i] = smooth(int(smoothIterations), currentArrays[i], distanceArrays[i])

            if str(i) not in exclude:
                xAxisData = [((float(distanceValue) - float(approachDistances[i])) / (probeTipDiameter/2/1000)) for distanceValue in distanceArrays[i]]
                yAxisData = [(float(currentValue) / float(currentArrays[i][probeRadAboveSurfaceIndex])) for currentValue in currentArrays[i]]

                plotter.plot(xAxisData, yAxisData, ".", markersize=1, label='Curve ' + str(i + 1))

                if shouldPreview:
                    plotter.title('curve ' + str(i))
                    plotter.show()


        plotter.ylabel(yAxisLabel)
        plotter.xlabel(xAxisLabel)
        plotter.legend()
        #plotter.savefig(filepathToSaveTo, bbox_inches='tight')
        #plotter.close()
        plotter.show()

    else:
        print('ok so i couldnt find any .csv files')


class DataTable:

    headers = []

    def __init__(self, Table):
        self.table = Table
        self._GenerateHeaders()

    def _GenerateHeaders(self):
        for entry in self.table[0]:
            self.headers.append(entry)

    def getColumn(self, header):

        columnData = []

        columnIndex = self.headers.index(header)

        for row in self.table:
            columnData.append(row[columnIndex])

        return columnData


def smooth(times, dependentVarList, independentVarList):

    Data = [float(entry) for entry in dependentVarList]
    updateYData = [float(entry) for entry in independentVarList]

    for t in range(1, times):
        smoothData = []
        updateYData = updateYData[1:-1]
        for i in range(1, (len(Data) - 1)):
            aveValue = (Data[i-1] + Data[i] + Data[1+1])/3
            smoothData.append(aveValue)

        Data = smoothData

    return smoothData, updateYData


def intQuestion(text):
    while True:
        response = input(text)

        if response in digits:
            return int(response)
        else:
            print('Input not understood please try again.')


def boolQuestion(text):
    while True:
        response = input(text + ' (y/n)')

        if response == 'y':
            return True
        elif response == 'n':
            return False
        else:
            print('Input not understood please try again.')


def GetFilepathArray(rootDir, filterTermsArray = []):
    dirpaths = []
    fileNames = []
    filepaths = []

    for subdir, dirs, files in os.walk(rootDir):
        for file in files:
            # only gets files with the mpt extension
            if len(filterTermsArray) == 0 or any(terms in file for terms in filterTermsArray):
                dirpaths.append(subdir)
                fileNames.append(file)
                filepaths.append(os.path.join(subdir, file))

    return dirpaths, fileNames, filepaths


Main()