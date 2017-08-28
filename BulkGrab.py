from PyQt5.QtWidgets import QFileDialog, QErrorMessage, QDialog
from glob import glob


"""
    Purpose: User will be prompted with a window asking them to select a directory (folder).
            Once a folder has been selected it will grab all files that follow the filename convention

            FORMAT: FilePattern*.csv.
            - Where the filepattern is determined by a popup window
            - the '*' represents any characters. The astreik is essentially a wildcard so the only 
              string that needs to be matches is the filepattern.
"""

class DataList(object):
    def __init__(self, FilePattern):
        super(DataList, self).__init__()

        try:
            print(FilePattern)
            self.FilePattern = FilePattern
        except Exception as ImportFilePattern:
            print(ImportFilePattern)

        self.BulkFileGrab()


    def BulkFileGrab(self):
        print("inside BulkFileGrab")

        #Open directory window and grab path of directory we want to pull data from
        self.path = QFileDialog.getExistingDirectory()

        self.Error = QErrorMessage()        #creates an object using pyqt ErrorMessage class
        try:
            if self.path == "":         #if we detect an empty string (no path given) we give user an error
                self.Error.showMessage("invalid filepath given")
                self.NoneReturn = True  #confirmation that an error occured

            elif self.path != "":   # proper filepath was given (non-empty string)

                #print statements made for debugging purposes.
                #print(self.path)

                #Grab all csv files following proper name convention
                if self.FilePattern == "Enter File Pattern...":
                    print("No LineEdit input given. Default state confirmed. Grabbing Files with fileformat TestSample*.csv")
                    print(("{}/TestSample*.csv").format(self.path))

                    self.filepaths = glob(("{}/TestSample*.csv").format(self.path)) #glob responsible collecting all files that fit format
                    self.NoneReturn = False   #file path is not None, proper input given
                    print(self.filepaths)
                else:
                    print("LineEdit was given input. Changing from default filepattern name convention.")
                    print(("{}/{}*.csv").format(self.path, self.FilePattern))

                    # glob grabs files with new filepattern string at specified directory
                    self.filepaths = glob(("{}/{}*.csv").format(self.path,self.FilePattern))

                    self.NoneReturn = False     #file path is not None, proper input given
                    print(self.filepaths)

            else:   #Otherwise throw an error
                print("directory not given")
                self.Error.showMessage("Directory not given")
                self.NoneReturn = True
        except Exception as FilePatternErr:
            print("error occured when trying to choose file pattern.......ERROR: {}".format(FilePatternErr))


