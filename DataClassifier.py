import pandas as pd

"""
        Purpose" DataClassifier.py works as a blueprint for creating our Data in its specified format
            - the program saves traits such as Entity Type, Tolerance Value, and Nominal Value
            - Program reformats data so it saves the part names and actual values as pandas dataframe
            - Removes several columns from the csv data that contain all null values, or unused data
            
        Input: Raw data being pulled from the .csv file
        Output: Data Object with saved traits such as, Entity Type, Tolerance Value, and Nominal Value.
                Data object contains a pandas dataframe with two colums Name(Alpha Part Names) & Actual Value(Measurements)
"""

class File_Attributes(object):
    def __init__(self, file):
        super(File_Attributes, self).__init__()
        print("inside File_Attributes")

        #List of EntityTypes grouped together by their shared traits
        self.EntityTypeList1 = ["Surface Profile", "Flatness", "Circularity"]
        self.EntityTypeList2 = ["Linear Dim.", "Angular Dim.", "Radial Dim."]

        self.Data = file

        #Call methods to instantiate data attributes Entity, Tolerance, and Nominal Value
        self.EntityFind()
        self.ToleranceFind()
        self.NominalFind()

        #Calls method to reorganize data
        self.Clean()

    def EntityFind(self):

        ENlist = pd.unique(self.Data['Unnamed: 1'].ravel())     #Creates an array of all the unique values in specified column

        # for loop creates variable Entype and sets it equal the entity type of whatever was measured
        # loop checks every element in the list until it finds something that is not a NaN value or the title string 'Entity Type'

        for i in range(len(ENlist)):
            if ENlist[i] != 'Entity Type' and 'NaN':
                self.EntityType = ENlist[i]

        print("Entity type is {}".format(self.EntityType))

    def ToleranceFind(self):


        print("Tolerance")
        """
            Function works in the same way as EntityFind() except there are two loops depending on the Entity Type of the file.
            
            each group of entity types has a different file format so the column where tolerance is located is different
            so in order find the tolerance we have to run a case by case basis.
            
            group 1: self.EntityTypeList1 = ["Surface Profile", "Flatness", "Circularity"]
                - Shares traits Actual Value, Tolerance, Bonus Tolerance
            group 2: self.EntityTypeList2 = ["Linear Dim.", "Angular Dim.", "Radial Dim."]
                - Shares traits Actual Value, Nominal, Deviation, and Tolerance
        """

        try:
            if self.EntityType in self.EntityTypeList1:     #checks to see if the entity type of the data is in group 1

                ToleranceList = pd.unique(self.Data['Unnamed: 3'].ravel())

                for i in range(len(ToleranceList)):
                    if ToleranceList[i] != 'Tolerance' and 'NaN':
                        self.Tolerance = ToleranceList[i]

                print("                               ")
                print("Tolerance is {}".format(self.Tolerance))

            elif self.EntityType in self.EntityTypeList2:   #checks to see if the entity type of the data is in group 2

                ToleranceList = pd.unique(self.Data['Unnamed: 5'].ravel())


                for i in range(len(ToleranceList)):
                    if ToleranceList[i] != 'Tolerance' and 'NaN':
                        self.Tolerance = ToleranceList[i]

                print("Tolerance is {}".format(self.Tolerance))
            else:
                pass
        except Exception as ToleranceErr:
            print("error found when trying to find Tolerance value of unformatted data..........ERROR:{}".format(ToleranceErr))

    def NominalFind(self):
        """
            Works just like the previous two functions. See EntityFind() for more information

            Since only EntityType2 has nominal values we only have to loop through their list
        """

        if self.EntityType in self.EntityTypeList2:
            NominalList = pd.unique(self.Data['Unnamed: 2'].ravel())

            for i in range(len(NominalList)):
                if NominalList[i] != 'Nominal Value' and 'NaN':
                    self.Nominal = NominalList[i]
            print("                               ")
            print("Nominal Value is {}".format(self.Nominal))

        else:
            self.Nominal = 'NaN'
            print("No Nominal Value Present {}".format(self.Nominal))

    def Clean(self):
        """
            Purpose: Drop any superflous data. The goal is to have just the Actual values and the part names, since we already collected all the other information
        """

        self.Data.dropna(thresh=1, axis=1, inplace=True) #Drops all columns that don't have at least one value that isn't a null value



        self.Data.drop('Name', 1, inplace=True)     # Filter Statistical Information:(USL, LSL, Cp, CPU, etc...) provided by the datasheet


        self.Data.drop('Unnamed: 1', 1, inplace=True)
        self.Data.drop('Unnamed: 4', 1, inplace=True)
        self.Data.drop('Actual Value', 1, inplace=True)
        self.Data.dropna(how='any', inplace=True)


        #We have to run case by case filtration because each EntityList has a different file format
        #In the end all that we should have left are the alpha part names column and the actual value measurements column

        if self.EntityType in self.EntityTypeList1: #check if the enity type belongs to group1

            print(self.Data)
            self.Data.drop('Unnamed: 3', 1, inplace=True)     #drops tolerance column


            """
                whenever you reset the index of a dataframe it saves the old index as a new column,
                you have to specify drop = true in order not to save it.
            """
            self.Data.reset_index(inplace=True, drop = True)  #reset row index so it starts at zero again, and drop old index

            print(self.Data)
            self.Data.drop([0], inplace=True)               #drops the row that holds column headers
            self.Data.reset_index(inplace=True, drop =True) #reset row index so it starts at zero again, and drop old index


            self.Data.rename(columns={'Unnamed: 0': "Name" }, inplace=True)
            self.Data.rename(columns={'Unnamed: 2': "Actual Value"}, inplace=True)
            print(self.Data)


        elif self.EntityType in self.EntityTypeList2:

            print(self.Data)
            self.Data.drop('Unnamed: 2', 1, inplace=True)   #drops the nominal value column of raw data
            self.Data.drop('Unnamed: 5', 1, inplace=True)   #drops the Tolerance value column of raw data

            print(self.Data)
            self.Data.reset_index(inplace=True, drop = True)        #reset the index
            self.Data.drop([0], inplace=True)                       #drops the column headers that are in row zero
            self.Data.reset_index(inplace=True, drop = True)        #reset the index

            self.Data.rename(columns={'Unnamed: 0': "Name" }, inplace=True)
            self.Data.rename(columns={'Unnamed: 3': "Actual Value"}, inplace=True)

        print(self.Data)

        length = len(self.Data.index)   #gets length of data along row-wise

        print("length of data is {}".format(length))

        self.CleanData = self.Data #Store our data in variable as cleaned data

        print("Data has been cleaned and formatted to include only names and measurements")
        print(self.CleanData)





