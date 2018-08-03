import os
import matplotlib.pyplot as plotter


def GetFilepathArray(rootDir):
    dirpaths = []
    fileNames = []

    for subdir, dirs, files in os.walk(rootDir):
        for file in files:
            # only gets files with the mpt extension
            if file.split(".")[1] == "mpt":
                # dirpath.append(os.path.join(subdir, file))
                dirpaths.append(subdir)
                fileNames.append(file)

    return dirpaths, fileNames


def GetAbsOfArray(Array):
    results = []

    for entry in Array:
        results.append(abs(entry))

    return results


def PlotAndSaveLPRGraph(filepathToSaveTo, ArrayToPlot, xAxisLabel, yAxisLabel):
    # sets the plot to about the size of a piece of paper
    plotter.figure(figsize=(11, 8.5), dpi=600)
    # in puts the data to the plotter
    plotter.plot(ArrayToPlot[0], ArrayToPlot[1], ".", markersize=3)
    plotter.ylabel(yAxisLabel)
    plotter.xlabel(xAxisLabel)
    plotter.ticklabel_format(style='sci', axis='x', scilimits=(0, 0))
    plotter.savefig(filepathToSaveTo, bbox_inches='tight')
    # plotter.show()


def PlotAndSaveTPGraph(filepathToSaveTo, ArrayToPlot, xAxisLabel, yAxisLabel):
    plotter.figure(figsize=(11, 8), dpi=600)
    plotter.semilogx(GetAbsOfArray(ArrayToPlot[0]), ArrayToPlot[1], ".", markersize=3)
    plotter.ylabel(yAxisLabel)
    plotter.xlabel(xAxisLabel)
    plotter.savefig(filepathToSaveTo, bbox_inches='tight')
    # plotter.show()


