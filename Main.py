import os
import matplotlib.pyplot as plotter
import pandas as pd
from string import digits


def GetFilepathArray(rootDir):
    dirpaths = []
    fileNames = []
    filepaths = []

    for subdir, dirs, files in os.walk(rootDir):
        for file in files:
            # only gets files with the mpt extension
            if 'mpt' in file:
                if 'OCV' not in file:
                    dirpaths.append(subdir)
                    fileNames.append(file)
                    filepaths.append(os.path.join(subdir, file))

    return dirpaths, fileNames, filepaths


def find_start_index(path):
    with open(path) as file:
        data = file.readlines()

    for line in data:
        if line[0] == "\n":
            continue

        if line[0] == "\t":
            if line[1] in digits:
                shifted_index = data.index(line)
                return shifted_index - 2
                break

        else:
            if line[0] in digits:
                shifted_index = data.index(line)
                return shifted_index - 2
                break


def data_extractor(file_path):
    raw_data = pd.read_csv(file_path, sep='\t', skiprows=find_start_index(file_path), error_bad_lines=False)
    potential = [value for value in raw_data["Ewe/V"]]
    current = [value*1000 for value in raw_data["<I>/mA"]]
    return potential, current


def GetAbsOfArray(Array):
    results = []

    for entry in Array:
        results.append(abs(entry))

    return results


def PlotAndSaveLPRGraph(filepathToSaveTo, ArrayToPlot, xAxisLabel, yAxisLabel):
    # sets the plot to about the size of a piece of paper
    plotter.figure(figsize=(11, 8.5), dpi=600)
    # in puts the data to the plotter
    plotter.plot(ArrayToPlot[0], ArrayToPlot[1], ".", markersize=1)
    plotter.ylabel(yAxisLabel)
    plotter.xlabel(xAxisLabel)
    plotter.ticklabel_format(style='sci', axis='x', scilimits=(0, 0))
    plotter.savefig(filepathToSaveTo, bbox_inches='tight')
    plotter.close()
    # plotter.show()


def PlotAndSaveTPGraph(filepathToSaveTo, ArrayToPlot, xAxisLabel, yAxisLabel):
    plotter.figure(figsize=(11, 8.5), dpi=600)
    plotter.semilogx(GetAbsOfArray(ArrayToPlot[0]), ArrayToPlot[1], ".", markersize=1)
    plotter.ylabel(yAxisLabel)
    plotter.xlabel(xAxisLabel)
    plotter.savefig(filepathToSaveTo, bbox_inches='tight')
    plotter.close()
    # plotter.show()


rootDir = r'M:\myWorkShop\pyWorkShop\Data to process'
saveDir = r"M:\myWorkShop\pyWorkShop\Graphs"
dirPath, fileName, filePaths = GetFilepathArray(rootDir)

for entry in filePaths:

    Voltage, Current = data_extractor(entry)

    GraphFileName = entry.split("\\")[-2]
    print(GraphFileName)

    if "LPR" in entry:
        PlotAndSaveLPRGraph(saveDir + "\\LPR_" + str(GraphFileName) + ".pdf", [Current, Voltage], 'Current (mA)', 'Voltage (V vs SCE)')

    if "TP" in entry:
        PlotAndSaveTPGraph(saveDir + "\\TP_" + str(GraphFileName) + ".pdf", [Current, Voltage], 'Current (mA)', 'Voltage (V vs SCE)')