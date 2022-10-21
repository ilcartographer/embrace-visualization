import pandas as pd # needs pandas installed
import tkinter as tk

#test comment
class datamodel:


    def __init__(self,csvurl): #csvurl referring to summary, can take StringVar or string
        print(csvurl)
        tempstr = ""
        if type(csvurl) is tk.StringVar:
            tempstr = csvurl.get()
        else:
            tempstr = csvurl
        if tempstr is not None and len(tempstr)>0:
            self.url = tempstr
            self.data = pd.read_csv(tempstr)
        else:
            self.url=""


    def setnewurl(self,csvurl):#sets new csvurl and data
        print(csvurl)
        tempstr = ""
        if type(csvurl) is tk.StringVar:
            tempstr = csvurl.get()
        else:
            tempstr = csvurl
        if tempstr is not None and len(tempstr) > 0:
            self.url = tempstr
            self.data = pd.read_csv(tempstr)
        else:
            self.url = ""


    def timeYformat(self, time, Y): # return dataframe with only the specified time variable and Y variable
        return self.data.iloc[:,[time,Y]]
    def getDF(self): #returns dataframe
        return self.data

    def __str__(self):
        return "datamodel:" + self.url

    def getdatacolumn(self,select):#gets only column, specified by number or string, returns as a dataframe object, can select by column name
        tempindex = select
        if type(select) is str:
            tempindex = self.getcolumnindex(select)
        return self.data.iloc[:,tempindex]

    def getcolumnaslist(self,select):#returns selected column as a list
        tempindex = select
        if type(select) is str:
            tempindex = self.getcolumnindex(select)
        temp = self.getdatacolumn(tempindex)
        return temp.values.tolist()
    def getcolumnindex(self,name):#returns numerical index of named column
        index = 0
        namelist = self.getcolumnnameslist()
        if name in namelist:
            index = namelist.index(name)
        return index
    def getcolumnnameslist(self):#returns list of column names
        namelist = self.data
        namelist = namelist.columns.tolist()
        return namelist

