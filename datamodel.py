import inline as inline
import matplotlib
import pandas as pd # needs pandas installed
import tkinter as tk
import numpy as np
import matplotlib.pyplot as plt

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

    def getdatacolumn(self,select):#gets only column, specified by number, returns as a dataframe object
        return self.data.iloc[:,select]



