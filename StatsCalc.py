import pandas as pd
import numpy as np
import math

class DataStatistics(object):
    def __init__(self, FormattedObj):
        super(DataStatistics, self).__init__()
        """
        Start of statistics calculations.
        Purpose: calls subfunctions to calculate statistics and concatenate all the data into one dataframe to be
        exported to excel as a .csv file.
        """

        self.Data = FormattedObj.FormattedData

        # Assigns statistical data to be whatever is run through the function Statistics()
        StatsData, DataFix = self.Statistics()

        # Combines the all the measurement data with its relavent statistics data
        self.CompletedData = pd.concat([DataFix, StatsData], axis=1)
        print(self.CompletedData)



    def Statistics(self):
        print("Statistics Calculations Start Here")


        # Base Stats isolate the measured values from the dataframe by dropping "Nominal measurements" and "Tolerance"
        try:
            BaseStats = self.Data.drop('Nominal Value', axis=1)
            BaseStats = BaseStats.drop('Tolerance', axis=1)
            BaseStats = BaseStats.reset_index(drop=True)
        except Exception as e:
            print(e)

        # Mean/Average Calculations_________________________________________________________________________________
        """
    
        for some reasons conversion of the series/dataframe was being altered and prevented the use of built in functions such as .mean.
        Best solution was to build my own minifunction to loop through the dataframe and calculate the averages that way
    
    
        1. Create a list of zeros for length of the dataset (number of trend reports)
        2. for loop that runs through all the values and sums up each measurement and then divides by the total to get the average
            i. 
        3. convert list back into a series and store it in a new dataframe with the header 'Mean'
        """
        # 1
        meanlist = [0] * (len(BaseStats))

        # 2
        for i in range(len(BaseStats)):
            # takes all the values in a row of dataframe and stores them as a list of values to be referenced later on
            values = BaseStats.iloc[i, :]
            n = len(values)

            sumTotal = 0

            # Values being pulled from dataframe are not considered floats and thus must be converted
            ConvertedVals = pd.to_numeric(values)

            # the below for loop, loops through the values in the list and creates a sum of values and then we take the average
            for index, val in ConvertedVals.iteritems():
                sumTotal = sumTotal + val
            average = sumTotal / n
            average = round(average, 4)
            meanlist[i] = average

        # checking the output is as expected
        # print(meanlist)

        # 3).Convert the list to a series and store it in our main dataframe
        mean = pd.Series(meanlist)
        # print(mean)

        StatsFrame = pd.DataFrame()
        StatsFrame['mean'] = mean

        # MEDIAN: uses built in function .median to calculate median values
        StatsFrame['median'] = BaseStats.median(axis=1)
        # print(StatsFrame)

        # MIN: uses a built in function .min to calculate the minimum value of a trend report
        StatsFrame['min'] = BaseStats.min(axis=1)
        # print(StatsFrame)

        # MAX:uses a built in function .max to calculate the max value of a trend report
        StatsFrame['max'] = BaseStats.max(axis=1)
        # print(StatsFrame)

        # RANGE: max values - min values to calculate the range of each trend report
        StatsFrame['range'] = StatsFrame['max'] - StatsFrame['min']
        print(StatsFrame)

        # DEVIATION:
        """
        For similar reasons as for when calculating mean, Deviation need its own mini function involving conversions
        from objects to floats in order to analyze the data.
        """
        # NomValsCON stands for the converted nominal values to floats, which are then stored into a list so we can convert them to arrays and use element wise math
        try:
            NomValsCON = self.Data['Nominal Value'].astype(float)
            NomList = NomValsCON.tolist()

        except Exception as ConversionErr:
            print("error occured when trying to converty Nominal values to floats......ERROR:{}".format(NomValsCON))


        # referencing the above created list of mean values we convert our list of nominal values to arrrays so we can perform element wise arithmatic
        Deviation = np.asarray(NomList) - np.asarray(meanlist)

        StatsFrame['Deviation'] = pd.DataFrame(Deviation)
        print(StatsFrame)
        print("here is deviation list")
        print(Deviation)


        # VARIANCE:
        n = len(BaseStats)
        variancelist = [0] * (n)    #empty list to hold our values
        for i in range(n):
            values = BaseStats.iloc[i, :]   #loop through all rows of our data
            m = len(values)
            sumTotal = 0
            ConvertedVals = pd.to_numeric(values)   #convert data values to numbers
            for index, val in ConvertedVals.iteritems():
                sumTotal = sumTotal + ((val - (StatsFrame['mean'][i])) ** 2) #eqn for variance
            varianceval = sumTotal / (m - 1)
            varianceval = round(varianceval, 6)
            variancelist[i] = varianceval

        variance = pd.Series(variancelist)
        print(variance)

        StatsFrame['variance'] = variance

        print(StatsFrame)


        # STANDARD DEVIATION:
        n = len(StatsFrame['variance'])
        variancelist = np.zeros([n])
        for i in range(n):
            variancelist[i] = StatsFrame['variance'][i]

        for i in range(n):
            variancelist[i] = math.sqrt(variancelist[i])

        StdDev = pd.DataFrame(variancelist)

        # print(StdDev)
        StatsFrame['Standard Deviation'] = StdDev
        print(StatsFrame)


        # MAX/MIN TOLERANCE

        # if .split('±')
        n = len(self.Data)

        location = [0] * n  #make an empty list filled with zeros the length of our data. This will serve to save index location
        storage = np.zeros([n]) #make an array length of our data

        Data = self.Data.reset_index(drop = True)

        DataFilled = Data.fillna(0)     #fill all nan values with zeros

        try:
            for i in range(n):
                if DataFilled['Nominal Value'][i] == 0:
                    storage[i] = 0
                else:
                    print("location is here {}".format(location))
                    TolList = Data['Tolerance'].values.tolist()
                    location = TolList[i].split('±')
                    print("location after operation {}".format(location))
                    storage[i] = location[1]
                    print(storage)
        except Exception as MaxMinTol:
            print("an error occurred when calculating Max and Min Tolerances.....ERROR: {}".format(MaxMinTol))

        try:
            Tolerances = pd.DataFrame({'Tolerances': storage}) #create a dataframe with column header Tolerances using 'storage' array

            ConvTol = pd.to_numeric(Tolerances['Tolerances'])   #convert objects to floats

            NomVals = self.Data['Nominal Value'].astype(float)  #convert data in Data Pandas object to floats

        except Exception as floatERR:
            print("error occurs when converting str to float.........ERROR:{}".format(floatERR))

        print("Datatypes are here______________________________________________________")
        print(Data['Nominal Value'].dtype)
        print(ConvTol.dtype)


        StatsFrame['LowerBound'] = pd.DataFrame(NomVals - ConvTol)
        StatsFrame['UpperBound'] = pd.DataFrame(NomVals + ConvTol)

        print(Data)
        print(StatsFrame)

        DataFix = Data.reset_index()
        DataFix.drop('index', 1, inplace=True)

        return (StatsFrame, DataFix)