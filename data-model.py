import pandas as pd # needs pandas installed
#test comment
class datamodel:
    def __init__(self,csvurl): #csvurl referring to summary
        self.data = pd.read_csv(csvurl)
    def timeYformat(self, time, Y): # return dataframe with only the specified time variable and Y variable
        return self.data.iloc[:,[time,Y]]