import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import os
from glob import glob

def readTecFile(fileCat, fileNum, run_name):
    #display(run_name, fileCat, fileNum)
    fileName = '{}_{}.{}'.format(run_name, fileNum, fileCat)
    with open(fileName) as f:
        f.readline()
        headerLine = f.readline()    
        columnHeaders = headerLine[11:]
        columnHeaders = columnHeaders.replace("'", "")
        columnHeaders = columnHeaders.replace('"', "")
        columnHeaders = columnHeaders.replace('(yrs)', "")
        columnHeaders = columnHeaders.replace(' ', "")
        columnHeaders = columnHeaders.rstrip()
        columnHeaders = columnHeaders.rstrip(',')
        columnHeaders = columnHeaders.split(',')

        df = pd.read_csv(fileName, engine='python', sep='\s+', skiprows=[0,1,2], names=columnHeaders)
        return df, columnHeaders
    

def plot2DTecFile(dataFrame, scalarName, vmin, vmax):
    z = dataFrame.pivot('z', 'x', scalarName)
    x, y = np.meshgrid(z.columns.values, z.index.values)
    levels = np.linspace(vmin, vmax, 16)
    CS = plt.contourf(x, y, z, levels=levels, cmap=cm.viridis, extend='both')

    colorbar = plt.colorbar(CS)
    plt.show()
    
def plot1DTecFile(dataFrame, scalarName):
    plt.plot(dataFrame[scalarName], dataFrame['z'])
    #maxdepth=max(dataFrame['z'])
    #plt.ylim([maxdepth, 0])
    
def getDataCats(directory, run_name):
    os.chdir(directory)
    fList = glob(run_name+'_*')
    fList=[s for s in fList if [any(i.isdigit() for i in s)] == [True]]
    fList = [i.lstrip(run_name+'_') for i in fList]
    fList = [s for s in fList if ['gs' in s] == [True]]
    fList = [i.lstrip('.0123456789') for i in fList]
    fSet = set(fList)
    outputTotal = len(fList) / len(fSet)
    return fSet, int(outputTotal)

def plotTimeNav(fileCat, time, plotVar, maxTime, run_name):
    df, columnHeaders = readTecFile(fileCat, time, run_name)
    vmin, vmax = findColorMapRange(maxTime, fileCat, plotVar, run_name)
    plot2DTecFile(df, plotVar, vmin, vmax)
    
def plotTimeNav1D(fileCat, time, plotVar, maxTime, run_name):
    df, columnHeaders = readTecFile(fileCat, time, run_name)
    #display(df)
    plot1DTecFile(df, plotVar) 
    
def findColorMapRange(maxTime, fileCat, plotVar, run_name):
    minList = []
    maxList = []
    for t in range(1, maxTime):
        df = readTecFile(fileCat, t, run_name)[0]
        s = df.loc[:, plotVar]
        minList.append(s.nsmallest(1).values)
        maxList.append(s.nlargest(1).values)

    timeSeriesMin = np.amin(minList)
    timeSeriesMax = np.amax(maxList)
    
    return timeSeriesMin, timeSeriesMax

def importTimeSeries(fileName):
    with open(fileName) as f:
        f.readline()
        headerLine = f.readline()    
    columnHeaders = headerLine[11:]
    columnHeaders = columnHeaders.replace("'", "")
    columnHeaders = columnHeaders.replace('"', "")
    columnHeaders = columnHeaders.replace('(yrs)', "")
    columnHeaders = columnHeaders.replace(' ', "")
    columnHeaders = columnHeaders.rstrip()
    columnHeaders = columnHeaders.rstrip(',')
    columnHeaders = columnHeaders.split(',')
    
    df = pd.read_csv(fileName, engine='python', sep='\s+', skiprows=[0,1,2], names=columnHeaders)
    return df, columnHeaders

def plotBreakthrough(time, plotVar, dataFrame):
    fig, ax = plt.subplots()
    ax.plot(time, dataFrame.loc[:, plotVar])