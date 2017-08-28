import matplotlib
from matplotlib import pyplot as plt
import matplotlib.patches as mpatches

matplotlib.use("Qt5Agg")

plt.style.use(['ggplot'])

# Backend door for matplotlib importation required to use Pyqt with matpltlib libray
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationBar
from matplotlib.figure import Figure
from matplotlib import rcParams

import numpy as np
import math

import DragHandler

import TableAttributesWin


class FigureAssembly(object):
    """
        Purpose: create the base figure for data to be plotted on.
        1. Inheritance/initalization
        2. defining figure and axes
        3. Plotting method
    """

    def __init__(self):
        super(FigureAssembly, self).__init__()

        self.figure = plt.figure()  # creates a blank figure to plot data on
        """
        'self.figure.add_subplot(111)'
        defines the number and position of subplots first two numbers are total number of plots on grid.
        For example 2x2 indicates total of 4 plots. Last number indicates the acutal plot number. For example 223 means
        there are four plots and we are looking at the third plot of the 4
        """
        self.axes = self.figure.add_subplot(111)

        # define axes headers
        self.axes.set_xlabel('x label')
        self.axes.set_ylabel('y label')

        # empty lists needed to append data to later on

        self.pltList = []       #stores the data that will be plotted
        self.LabelsList = []    #Label list store the x-axis labels for row, datapoints, and part names
        self.NameList = []      #Stores the name of the table
        self.TheRows = []       #Stores the which rows the data was taken from
        self.CleanedDataList = [] #Stores all of the sets of data that are planning to be plotted (for multiplot)
    def plotAnnotations(self, AnnotationList):
        print("begining to plot annotations")

        self.Annotations = AnnotationList
        #
        # try:
        #     print("adding annotations to plot")
        #
        #     for i in AnnotationList:
        #         print("inside annotation plotter")
        #         self.axes.text(.1,.1,i, picker = True, color = 'black', fontsize = 9.5)
        #         dragh = DragHandler.DragHandler()
        #
        # except Exception as AnnotationPltErr:
        #     print("error occured when trying to plot Annotations.....ERROR: {}".format(AnnotationPltErr))
        #
        # print("annotations have been added to plot")



    def plotDataBox(self, ydata, StatsDataFrame, RowIndex):
        print("Inside plotDataBox()")
        self.axes.grid()  # add a grid to plot

        ### BOX PLOT ###

        print("In method PlotData, begin configuring BoxPlot")
        self.y = ydata

        print("y data is here .......{}".format(self.y))
        self.cleanedY = [y for y in ydata if
                         str(y) != 'nan']  # creates a list of data filtering out Null values (empty cells)
        self.axes.boxplot(self.cleanedY)

        try:
            print("trying to create horizontal line")

            # reference the statistics data and get Upper/lower bound values
            upper = StatsDataFrame["Upper Bound"][RowIndex]
            lower = StatsDataFrame["Lower Bound"][RowIndex]

            #create horizontal lines at upper/lower bound       green = upper   red = lower
            self.axes.axhline(y = upper, xmin = 0, xmax = 5, c = 'green', linewidth = 1, zorder = 0)
            self.axes.axhline(y= lower, xmin=0, xmax=5, c='red', linewidth=1, zorder=0)
        except Exception as HorizontalLineErr:
            print('error occured when trying to plot arbitrary lines on the plot.......ERROR: {}'.format(HorizontalLineErr))
        self.axes.grid()

        # creates a textbox in the upper right corner of Plot displaying number of datapts used
        #   .text(distance from edges, text, vertical alignment, horizontal alignment, unknown, color, fontsize)
        self.axes.text(.98, .98, 'Number of Data Points: {}'.format(len(self.cleanedY)),
                       verticalalignment='top', horizontalalignment='right',
                        transform=self.axes.transAxes,
                       color='black', fontsize=9.5)

        print("begining to plot annotations")

        try:
            print("adding annotations to plot")

            for i in self.Annotations:
                print("inside annotation plotter")
                self.axes.text(.95,.95,i, picker = True, verticalalignment='top', horizontalalignment='right',
                        transform= self.axes.transAxes, color = 'black', fontsize = 9.5)
                #dragh = DragHandler.DragHandler()


        except Exception as AnnotationPltErr:
            print("error occured when trying to plot Annotations.....ERROR: {}".format(AnnotationPltErr))

        print("annotations have been added to plot")

        plt.show()


    def ScatterPlotData(self, ydata, xdata):
        print("Running Method ScatterPlotData, singular plots")

        ###Peculiar thing xdata is actually the y values and the y values are actually the xvalues

        self.axes.grid()  # add a grid to plot


        ### SCATTER PLOT ###

        print("In method ScatterPlotData, begin configuring Scatter Plot")

        NanIndex = []                       #store the indexes if there are Null values in the data from QtableWidget
        self.y = ydata                      #y data to be plotted
        xsmall = []                         #list to store column headers that will be removed
        RawData = list(enumerate(ydata))    #creates ordered pairs (index, data) for each value in xdata

        print("RAW DATA HERE.......................... {}".format(RawData))



        """
            loops through the ordered pairs and checks to see if there exists any Null Values and if they exist
            the index for null values are saved to be removed from the plotting data later on.
        """
        for index, item in enumerate(RawData, start=0):
            print(type(item[1]))
            if math.isnan(item[1]):
                NanIndex.append(index)

        print("NAN INDEX VALUE HERE.......................{}".format(NanIndex))

        self.cleanedY = [y for y in ydata if str(y) != 'nan'] #creates list of data after all null values have been removed

        try:
            #remove header values for corresponding null index.
            for i in NanIndex:
                xsmall.append(xdata[i])
        except Exception as HeaderClean:
            print("error found when trying to remove associated null value headers......ERROR:{}".format(HeaderClean))

        #converts lists to sets so we can perform Set mathematics on them
        xdata = set(xdata)
        xsmall = set(xsmall)

        self.x = list(xdata - xsmall)   #modified y data after null value associated headers have been removed


        n = len(self.x)
        m = len(self.cleanedY)
        print("LENGTH OF X DATA IS {}, LENGTH OF Y DATA IS {}".format(n,m))

        # Creates 1 to n many points along our x-axis for each piece of data we will plot
        self.NumTicks = np.arange(n)
        #print(self.NumTicks)

        # sets ticks 1-n as x-axis
        self.axes.set_xticks(self.NumTicks)
        #print("ticks have been created ")

        # sets our table headers as the x-axis labels for our datapoints, and rotates to look better
        self.axes.set_xticklabels(self.x, rotation=90)
        #print("strings have been set as labels")
        #  creates scatter plot
        self.axes.scatter(self.NumTicks, self.cleanedY)
        self.axes.grid()
        # self.axes.plt.tight_layout()

        #creates a textbox in the upper right corner of Plot displaying number of datapts used
        self.axes.text(.99, .95, 'Number of Data Points: {}'.format(len(self.cleanedY)),
                       verticalalignment='top', horizontalalignment='right',
                       transform=self.axes.transAxes,
                       color='black', fontsize=9.5)

        plt.show()
        print("Graph Successfully Completed")

    def MultiPlot(self, ydata, xdata, PlotVal, name, row, NullIndex ):
        print("Configuring Multiple Plots on Figure")

        #ydata = y data to be plotted
        #xdata = column headers which will represent tick marks on x-axis
        #PlotVal = type of plot scatter/box plot
        #name = table name
        #row = row index
        #Null Index = null values indices


        self.axes.grid()

        self.NameList.append(name)

        ### BOX PLOT ###
        if PlotVal == "box":
            print("inside boxplot")
            self.cleanedY = [y for y in ydata if str(y) != 'nan']   #filters out null values from ydata

            self.TheRows.append(row)
            self.pltList.append(self.cleanedY)
            self.CleanedDataList.append(len(self.cleanedY))

            self.axes.grid()

        elif PlotVal == "scatter":
            print("Inside multi scatter plot")
            self.y = ydata

            print("about to assign n")

            self.x = xdata.tolist()
            tempstorage = []
            print(NullIndex)
            for i in range(len(NullIndex)):
                tempstorage.append(self.x[i])   #stores the header values that share the same index as a null value

            for i in tempstorage:
                self.x.remove(i)    #remove column header values from x-data that were associated with null values

            print("after NUll - ColumnHeaders deletion has been finalized")

            n = len(self.x) #length of new cleaned x-data

            # Creates 1 to n many points along our x-axis for each piece of data we will plot
            self.NumTicks = np.arange(n)
            print(self.NumTicks)

            # sets ticks 1-n as x-axis
            self.axes.set_xticks(self.NumTicks)
            print("ticks have been created ")

            # sets our table headers as the x-axis labels for our datapoints, rotate makes header perpindicular with x-axis
            self.axes.set_xticklabels(self.x, rotation=90)
            print("strings have been set as labels")

            NumDataPts = len(self.x)

            self.axes.scatter(self.NumTicks, self.y, label = "row {}, Data Points: {}, {}".format(row, NumDataPts, name))
            self.axes.grid()


    def ShowScatter(self):
        self.axes.legend()
        plt.show()
        #shows data for multiple scatter plot data
    def BoxPltter(self):
        try:

            print(self.pltList)
            print(self.TheRows)
            print(self.CleanedDataList)
            print("Label List before loop")
            print(self.LabelsList)
            self.LabelsList = []
            for i in range(len(self.pltList)):
                print("what row is being plotted {}".format(self.TheRows[i]))
                self.LabelsList.append("row {}, Data pts: {}, {}".format(self.TheRows[i], self.CleanedDataList[i], self.NameList[i]))
                print(self.LabelsList)


            self.axes.boxplot(self.pltList)
            #self.LabelsList,
            self.axes.set_xticklabels(self.LabelsList)

            plt.show()
        except Exception as boxy:
            print("Error present in box pltter = {}".format(boxy))