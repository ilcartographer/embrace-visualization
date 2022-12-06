# embrace-visualization
CSE350/550 Fall 2022, Team 3

# Project Overview
The Embrace Visualization project is an application for visualizing data from the Embrace2 wearable. The device is used 
keep health metrics for patients that suffer from epileptic seizures. Being able to see this data can possibly help with
identifying trends which may help to find trigger points or predictors.

This application provides a GUI that a user can use to import the data from a CSV file. It will load the selected data
series and render the graphs. From there, the user can view the data points, zoom in and out, and update how the data is
aggregated for the graph.

# Running the Application
The application in written for Python 3. The main Python file to run the application is main-window.py. Running this 
will launch a blank window, where the user can use the top menu to open the data loader.

# Using the Application
(TODO: Text descriptions needed)
## Loading a Dataset
![](C:\Development\embrace-visualization\images\usermanual\load_data_menu.png)

![](C:\Development\embrace-visualization\images\usermanual\select_file_filled.png)
## Selecting Data Series
![](C:\Development\embrace-visualization\images\usermanual\series_selector.png)
## Viewing the Data
![](C:\Development\embrace-visualization\images\usermanual\graphs_loaded.png)
### Getting Graph Values
![](C:\Development\embrace-visualization\images\usermanual\data_hover.png)
### Zooming In/Out
![](C:\Development\embrace-visualization\images\usermanual\graph_zoom.png)
### Modifying Aggregation Settings
![](C:\Development\embrace-visualization\images\usermanual\aggregate_interval.png)

![](C:\Development\embrace-visualization\images\usermanual\aggregate_metric.png)

![](C:\Development\embrace-visualization\images\usermanual\data_aggregated.png)