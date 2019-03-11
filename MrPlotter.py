import os
import matplotlib.pyplot as plotter
import pandas as pd
from string import digits

def Main():


    ## need to complete the code which uses a class/function to get the units of current and voltage from the data file

    formatsList = {
        'mpt': FileFormats.parstat
    }

    adminCommandsList = {
        'exit': 'Ends the program',
        'help': 'lists all the commands',
        'all': 'when added after a relevant command will preform the action on all files present',
        'filter': 'when added after a relevant command will ask for words to look in file names'}

    basicCommandsList = {
        'tafel': Plot.tafel,
        'f2129': Plot.f2129,
        'find': Tools.find}

    while True:

        userRawRequest = input('Type a command. Type help for a list of commands.\n').lower().split(' ')

        if userRawRequest[0] == 'exit':
            break

        elif userRawRequest[0] == 'help':
            printHelp(adminCommandsList, basicCommandsList)

        elif userRawRequest[0] == 'clear':
            os.system('cls' if os.name == 'nt' else 'clear')

        elif userRawRequest[0] == 'plot':
            if userRawRequest[1] in basicCommandsList:
                # this is used in the case where the user specifies all and/or filter
                if len(userRawRequest) > 2:
                    extenders = userRawRequest[2:]
                else:
                    extenders = []
                basicCommandsList[userRawRequest[1]].main(extenders, formatsList)
            else:
                print('Im not sure how to plot that kind of plot')

        else:
            print('Sorry your last command was not recognized. Please try again.')


## high level plot methods

class Plot:

    def ReadyForPlot(extenders, formatList):

        filters = []
        paths = []

        if any("filter" in entry for entry in extenders):
            filterStr = input('please type the terms you would like to select for, Separated with spaces')

        if any("all" in entry for entry in extenders):
            while True:
                check = input('Should I plot all the files I find in the current working directory? (y/n) ').lower()

                if check == 'n':
                    print('ok I will not plot anything')
                    break
                elif check == 'y':
                    _, _, paths = GetFilepathArray(os.getcwd(), filters)
                    break
                else:
                    print('Input not understood please try again.')

        else:
            paths = [input('Please type the path of the file to be plotted:\n')]

        if len(paths) != 0:

            yAxisLabel = input('What should the y-axis be labeled?')
            xAxisLabel = input('And what should the x-axis be labeled?')

            while True:

                saveChoice = input(
                    'Should I save the plots in the current working directory? (y/n)\n The current working directory is {}\n'.format(
                        os.getcwd())).lower()

                if saveChoice == 'y':
                    print('Ok I will save the plots in the current working directory')
                    filepathToSaveTo = os.getcwd()
                    break
                elif saveChoice == 'n':
                    print('Ok where should I save the plots?')
                    filepathToSaveTo = input(
                        'Please type a valid path\n Warning No checking is done to make sure you entered a valid path\n')
                    break
                else:
                    print('Input not understood please try again.')

            return paths, yAxisLabel, xAxisLabel, filepathToSaveTo


    class tafel:
        commandText = 'plot tafel'
        description = 'Will plot data in the format of a tafel plot'
        def main(extenders, formatList):

            paths, yAxisLabel, xAxisLabel, filepathToSaveTo = Plot.ReadyForPlot(extenders, formatList)

            for path in paths:

                ext = path.split('.')[-1]

                if ext != '' and ext in formatList:
                    table = LoadData(path, formatList[ext])

                    voltageArray = table.getColumn(formatList[ext].voltageHeader)
                    currentArray = table.getColumn(formatList[ext].currentHeader)

                    plotter.figure(figsize=(11, 8.5), dpi=600)
                    plotter.semilogx(GetAbsOfArray(currentArray), voltageArray, ".", markersize=1)
                    plotter.ylabel(yAxisLabel)
                    plotter.xlabel(xAxisLabel)
                    plotter.savefig(filepathToSaveTo, bbox_inches='tight')
                    plotter.close()
                    # plotter.show()
                else:
                    print(ext)
                    print('This file {} has no type or is not a recognized type and so will be not be plotted'.format(path))


    class f2129:
        commandText = 'plot f2129'
        description = 'Will plot data in the format of a F2129 plot'

        def main(extenders, formatExtentions):
            print('im empty right now :(')

class Tools:
    class find:
        commandText = 'find'
        description = 'STILL A WORK IN PROGRESS. will return all a list of all matched files in the current directory'

        def main(extenders, formatExtentions):
            print('im empty right now :(')


class FileFormats:
    class parstat:
        ext = ['mpt', 'mpr', 'mps']
        startLineMarker = 'mode'
        separator = '\t'
        timeHeader = 'time/s'
        voltageHeader = 'Ewe/V'
        currentHeader = '<I>/mA'

        # will return true if the line should be considered part of the data set
        # this will be unique to the file type / brand of potentiostat
        def qualifier(splitLineData):
            return splitLineData[0] in digits


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

## plotting support methods

def GetAbsOfArray(Array):
    results = []

    for entry in Array:
        results.append(abs(entry))

    return results

def printHelp(adminCommandsList, basicCommandsList):

    print('\n{}Here is a list of excepted commands:{}'.format(color.UNDERLINE, color.END))
    print('-' * 100)
    print(color.RED + '{command}' + color.END + ': {description}')
    print('-'*100)

    for command in adminCommandsList:
        print('{0}{1}{2}: {3}'.format(color.RED, command, color.END, adminCommandsList[command]))

    for command in basicCommandsList:
        print('{0}{1}{2}: {3}'.format(color.RED, basicCommandsList[command].commandText, color.END, basicCommandsList[command].description))

    print('-'*100)


def LoadData(path, formatSpecifier):

    hasFoundMarker = False
    rawPlotData = []

    with open(path) as file:
        data = file.readlines()

    for line in data:
        if formatSpecifier.startLineMarker in line:
            startIndex = data.index(line)
            hasFoundMarker = True
            break
        else:
            hasFoundMarker = False
            print('sry didnt find the line maker ' + formatSpecifier.startLineMarker)

    # converts the raw data into a usable table
    if hasFoundMarker:
        # line by line pulls the actual data from the file
        for line in data[startIndex+1:]:
            if formatSpecifier.qualifier(line.split(formatSpecifier.separator)):
                rawPlotData.append(line.split(formatSpecifier.separator))
            else:
                break

        #places the collected raw data into a table
        return DataTable(rawPlotData)


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

## style methods

class color:
   PURPLE = '\033[95m'
   CYAN = '\033[96m'
   DARKCYAN = '\033[36m'
   BLUE = '\033[94m'
   GREEN = '\033[92m'
   YELLOW = '\033[93m'
   RED = '\033[91m'
   BOLD = '\033[1m'
   UNDERLINE = '\033[4m'
   END = '\033[0m'

## file nav methods
# def dirNav(): ## work in progress
#
#     while True:
#
#         currentDir = os.path.dirname(os.path.realpath(__file__))
#
#         command = input('{}> '.format(currentDir))
#
#         if command == 'ls':
#             dirpaths, fileNames, filePaths = GetFilepathArray(currentDir)
#
#             dirList = fileNames.extend([entry.split('\\')[0] for entry in dirpaths])
#
#             print('\n'.join('{}'.format(k) for k in dirList))
#             print(dirpaths)
#             print(fileNames)


Main()