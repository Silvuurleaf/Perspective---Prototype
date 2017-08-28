"""
    Purpose: Formatter.py is responsible for converting the pandas dataframe into desired horizontal file layout
    this set of data will not yet include any statistics data, besides the nominal and tolerance values.

    Input: CleanData created from DataClassifier.py. It will be a list of pandas Dataframe objects. The dataframes
     will be formatted so they have two columns Name (Alpha Part Names) and Actual Value (Measurements). Each dataframe
     is created based off one trend report.

    Output:expected have a dataframe with the Alpha Part names as column headers, actual values (measurements)
    filled along row-wise, and the nominal and tolerance columns appended on the end of the dataframe.



"""
import pandas as pd
import numpy as np

class Reformat(object):
    def __init__(self, CleanData):
        super(Reformat, self).__init__()

        self.DataSet = CleanData

        print(self.DataSet)


        #Initialize empty lists to store values in them later on
        self.NominalValList = []
        self.ToleranceValList = []
        self.ReformattedData = []

        self.initializingFormat()

    def initializingFormat(self):
        print("Formatting proccess beginning")

        self.TransposedDataList = []    #list to store data once its been transposed
        ActualValues = pd.Series()      #instantiate a series to hold the measurements

        #DataSet is a list of objects that stores the Cleandata from DataClassifier.py
        print(self.DataSet)

        """
            loops through list of Pandas Dataframe objects, where j is one of the objects in the list
            j will become each object in the list until there are no new objects in the list. When we say j in (list object)
            it literally becomes whatever the first value is, then the next, then the next, until it reaches the end of the set.
        """
        for j in (self.DataSet):
            print("inside j loop")

            self.UnFormattedData = j    #unformatted data pandas dataframe with two veritcal cols name, actual values

            #grab attributes from from the cleandata(unformatted data)
            self.EntityVal = self.UnFormattedData.EntityType
            self.NominalValList.append(self.UnFormattedData.Nominal)
            self.ToleranceValList.append(self.UnFormattedData.Tolerance)

            print(self.UnFormattedData.CleanData)

            for i in range((len(self.UnFormattedData.CleanData.index))): #loops that loops through depending on the length of the index

                print("I value is {}".format(i))

                #Loops through unformatted data and goes through the measurement(actual value) columns and appends the values to our empty Pandas Series
                ActualValues = ActualValues.set_value(i, self.UnFormattedData.CleanData.loc[i, 'Actual Value'])

                ActualValuesDF = pd.DataFrame(ActualValues)                 # Convert ActualValues (Series) to DataFrame

                self.TransposedData = ActualValuesDF.transpose()            # transpose data

            print(self.NominalValList)
            print(self.ToleranceValList)

            self.rename() #Call rename to change column headers

    def rename(self):
        print("inside rename method")

        print(len(self.TransposedDataList))

        for k in range(len(self.TransposedData.columns.values)): #loops through depending on the number of column headers of transposed dataset

            print("VALUE OF k IS {}...........................".format(k))

            self.TransposedData.rename(columns={k: self.UnFormattedData.CleanData.loc[k, 'Name']}, inplace=True) #takes the part names and sets them as the header names

            print(self.TransposedData)

        #once we loop through and transpose all the data we will store it in a list
        self.TransposedDataList.append(self.TransposedData)

        #once all the data is in a list object we can call a concatenate function to combine them into a singular dataframe

        self.Combine() #calls combine to concatenate all the data into one sheet

    def Combine(self):
        print("Inside combine")
        self.CombinedData = pd.concat(self.TransposedDataList, axis = 0) #combines all pandas dataframes in the transposed list
        print("Outputting COMBINED DATA here..........")

        self.CombinedData = self.CombinedData.reset_index(drop = True) #resets index and drops old index column
        print(self.CombinedData)

        self.NomTol_Attach() #Call NomTol to attach nominal/tolerance columns to dataframe

    def NomTol_Attach(self):
        print("attaching Nominal and Tolerance to our transposed data")
        print(type(self.NominalValList[0]))
        for i in range(len(self.NominalValList)):
            if self.NominalValList[i] == 'NaN':
                self.NominalValList[i] = np.nan # replace string NaNs with float np.nan value so it can be filtered out later
            else:
                #if values aren't null just keep going, hence pass
                pass
        print(self.NominalValList)

        #turn list -> series -> dataframes

        NominalSeries = pd.Series(self.NominalValList)
        NominalDataFrame = pd.DataFrame(NominalSeries)

        ToleranceSeries = pd.Series(self.ToleranceValList)
        ToleranceDataFrame = pd.DataFrame(ToleranceSeries)

        #rename dataframes to have appropriate headers
        ToleranceDataFrame.rename(columns={0: "Tolerance"}, inplace= True)
        NominalDataFrame.rename(columns={0: "Nominal Value"}, inplace=True)

        print("finished creating NomTol")

        # combine nominal tolerance values into one dataframe (column-wise)
        NomTol = pd.concat([NominalDataFrame, ToleranceDataFrame], axis=1)
        print(NomTol)

        self.FormattedData = pd.concat([self.CombinedData, NomTol], axis=1) #combine all our data
