#-------------------------------------------------------------------------------
# Name:        Spatial Index Checker
# Purpose:
#
# Author:      salangley
#
# Created:     22/07/2013
# Copyright:   (c) salangley 2013
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import arcpy
from arcpy import env
import re
import os, os.path
import glob
import arcgisscripting
import arcpy
import datetime
import ftplib
import logging
import os
import re
import shutil
import smtplib
import string
import subprocess
import sys
import time
import gzip
import platform
import sysconfig
import getpass
import zipfile
import zlib
import glob
import csv

def SpatialIndexChecker(g,n,dataset,data,data2):

    #Defining variables
    numberofrows=0
    data=[]
    data2=[]

    #Automatically sets the variable processworks to 1 to allow the code to execute straight through UNLESS it runs in an error Exception
    processworks=1
    print g

    #Breaking down each line within the csv file to obtain the Feature class and the CURRENT Spatial Indexes
    strSearchString =","

    #Getting the string that represents the relevant parameters, such as feature class name, current and default spatial indexes through string manipulation
    parameterline=dataset[g]
    parameterline=re.split(strSearchString,parameterline)

    Featureclassname=parameterline[0]
    CurrentSpatialIndex1=parameterline[1]
    CurrentSpatialIndex1=CurrentSpatialIndex1.replace("\n","")
    CurrentSpatialIndex2=parameterline[2]
    CurrentSpatialIndex2=CurrentSpatialIndex2.replace("\n","")
    CurrentSpatialIndex3=parameterline[3]
    CurrentSpatialIndex3=CurrentSpatialIndex3.replace("\n","")

    #Defining the Feature Classes Source link
    FeatureClassSource=Featureclassname

    try:
        #Getting the number of rows inside the feature class for the purpose of testing to whether or not the feature class is empty
        numberofrows=int(arcpy.GetCount_management(FeatureClassSource).getOutput(0))

    #If there is an error in trying to obtain the number of rows in the Feature class then an error message will be returned and the code will move on to the next line in the csv file
    except Exception, e:
        data = [FeatureClassSource,CurrentSpatialIndex1,CurrentSpatialIndex2,CurrentSpatialIndex3,"Please check if the URL is correct, the database connection and also its type.  " + str(e)]

        #Terminating the code execution for the current line in the csv file (g) by making the processworks disabled.
        processworks=0

    #otherwise...
    if processworks==1:

        #Checking to see if the featue class contains any data if so the.......
        if numberofrows!=0:

            #Calculate Default Spatial Grid Index
            try:
                DefaultSpatialIndex=arcpy.CalculateDefaultGridIndex_management(FeatureClassSource)


            #If unable to calculate default spatial index, then it is assumed to be something wrong with feature interms of trying to open it or an invalid field etc, a error message is returned
            except Exception, e:
                data = [FeatureClassSource,CurrentSpatialIndex1,CurrentSpatialIndex2,CurrentSpatialIndex3,"fail to open/work, please check the feature class in Arc Catalogue.  " + str(e)]

                #Terminating the code execution for the current line in the csv file (g) by making the processworks disabled.
                processworks=0

        #If there is no data inside the feature class then...
        else:

            #Return an error alerting that the feature class does not contain any data
            data = [FeatureClassSource,CurrentSpatialIndex1,CurrentSpatialIndex2,CurrentSpatialIndex3,"No data to calculate default spatial index"]

            #Terminating the code execution for the current line in the csv file (g) by making the processworks disabled
            processworks=0


    if processworks==1:

        #Getting the first spatial index value
        DefaultSpatialIndex1=DefaultSpatialIndex[0]
        DefaultSpatialIndex2=DefaultSpatialIndex[1]
        DefaultSpatialIndex3=DefaultSpatialIndex[2]

        #Checking to see if there is an actual default index, if no then print the message below
        if float(DefaultSpatialIndex1)==0:

            #Return an error alerting that the feature class does not contain any data
            data = [FeatureClassSource,CurrentSpatialIndex1,CurrentSpatialIndex2,CurrentSpatialIndex3,"Contains no default spatial indexes"]

            #Terminating the code execution for the current line in the csv file (g) by making the processworks disabled
            processworks=0


        #Checking to see if there is a R-Tree Spatial Index, if yes then print the message below
        if float(DefaultSpatialIndex1)==-2:
            data = [FeatureClassSource,CurrentSpatialIndex1,CurrentSpatialIndex2,CurrentSpatialIndex3,"contains a R-Tree spatial index"]

            #Terminating the code execution for the current line in the csv file (g) by making the processworks disabled
            processworks=0


        if processworks==1:

            #Comparing the CURRENT Spatial Index to the DEFAULT Spatial Index, if ALL three are the same then a message outlining the both CURRENT and DEFAULT Spatial Indexes along with a capital Y
            #indicating that this feature class is up to date otherwise a similar message is returned with a capital N outlining that the feature class is not up to date.
            #Each number format is rounded to 9 decimal places to elimnate diffrences due to rounding off errors and hence ensuring each feature class is catagorised propery.
            if format(float(CurrentSpatialIndex1),'.9f')==format(float(DefaultSpatialIndex1),'.9f'):
                if format(float(CurrentSpatialIndex2),'.9f')==format(float(DefaultSpatialIndex2),'.9f'):
                    if format(float(CurrentSpatialIndex3),'.9f')==format(float(DefaultSpatialIndex3),'.9f'):

                        data2 = [str(FeatureClassSource),CurrentSpatialIndex1,CurrentSpatialIndex2,CurrentSpatialIndex3,'Y',DefaultSpatialIndex1,DefaultSpatialIndex2,DefaultSpatialIndex3]

                    else:
                        data = [FeatureClassSource,CurrentSpatialIndex1,CurrentSpatialIndex2,CurrentSpatialIndex3,'N',DefaultSpatialIndex1,DefaultSpatialIndex2,DefaultSpatialIndex3]

                else:
                    data = [FeatureClassSource,CurrentSpatialIndex1,CurrentSpatialIndex2,CurrentSpatialIndex3,'N',DefaultSpatialIndex1,DefaultSpatialIndex2,DefaultSpatialIndex3]

            else:
                data = [FeatureClassSource ,CurrentSpatialIndex1,CurrentSpatialIndex2,CurrentSpatialIndex3,'N',DefaultSpatialIndex1,DefaultSpatialIndex2,DefaultSpatialIndex3]

    return g,n,dataset,data,data2

#################################################################################################################################################
#Defining the input csv file as a URL
SpatialIndexcsv="D:/GIS_Sytems_Development/SpatialIndexChecking/arcsde_grid_sizestest2.csv"

#Input for Database connection
databaseconnection="Database Connections/dmstest.dpipwe.tas.gov.au@sde.DC.sde"

#Defining a variable that allows to execute a particular block of code.  If = 0 then not, if = 1 then yes
processworks=1


#Trying to connect to specfied database
try:
    gp = arcgisscripting.create(10.1)
    gp.workspace = databaseconnection

    fcs = gp.ListFeatureClasses()

    #If connection is successful then display the following message and break out of the for loop
    for fc in fcs:
        print "CONNECTION WORKS.................."
        break

#If there is no input for database connection then return the following message..
except Exception, e:
    print "Please enter a valid path for spatial database connection"
    processworks=0


#If there  is a valid input Database connection then..
if processworks==1:

    #Creating the two csv out files.

    #File listing the feature classes that the current spatial indexes are different to the default spatial index (e.g. need updating)
    csvoutput1="D:/GIS_Sytems_Development/SpatialIndexChecking/SpatialIndexestobeupdated.csv"

    #File listing the feature classes that the current spatial indexes are the same as the default spatial index (e.g. up to date)
    csvoutput2="D:/GIS_Sytems_Development/SpatialIndexChecking/SpatialIndexesthatareupdated.csv"

    #Creating a tuple that represents the spatial indexes that need updating e.g. is used for the first csv file
    data=[]

    #Creating a tuple that represents the spatial indexes that are up to date e.g. is used for the second csv file
    data2=[]

    #Opening csv file to readlines from the input csv file
    try:
        inputfile = open(SpatialIndexcsv,'r')

    #If the path to input csv file is invalid then return error message.
    except Exception,e:
        print"Invalid path to input csv file"
        processworks=0

    if processworks==1:

        #Obtaining lines from input csv file
        dataset=inputfile.readlines();

        #Defining a workspace to loop through a Database Connection
        try:
            gp = arcgisscripting.create(10.1)
            gp.workspace = databaseconnection

        #If the above line do not work then return an error and disable the code from executing the code from this point onwards.
        except Exception, e:
            print "ERROR! CANNOT CONNECT TO DATABASE!  "
            print str(e)

            #Terminating the code execution
            processworks=0

put csv file
                    while g<n:

                        #Defining the column delimiter and line terminator
                        SpatialIndexestobeupdated = csv.writer(fp, delimiter=',',lineterminator='\n')

                        #Calling the spatial index checker function
                        g,n,dataset,data,data2=SpatialIndexChecker(g,n,dataset,data,data2)

                        #write to csv file only if the data[] contains information
                        if data!=[]:

                            #writing to csv file
                            SpatialIndexestobeupdated.writerow(data)

                        g=g+1

            #writing to csv output file2 that outlines all the feature classes that have up to date spatial indexes.
            #testing to see if csv output file 1 path is valid
            try:
                with open(csvoutput2, 'w') as fp:

                    #Defining the line counter
                    g=0

                    #Number of lines in text file
                    n=len(dataset)

            #Return message if the csv output file 2 path is not valid and terminate execution
            except Exception, e:
                print "Path for output csv output file 2 is not valid please try again"

                #Terminating the code execution
                processworks=0


            #If the Connection works then....
            if processworks==1:

                #writing to csv file that outlines all the feature classes that have already their spatial indexes updated
                with open(csvoutput2, 'w') as fp:

                    #Defining the line counter
                    g=0

                    #Number of lines in text file
                    n=len(dataset)

                    #This represents the loop through the input csv file
                    while g<n:
                        SpatialIndexestobeupdated = csv.writer(fp, delimiter=',',lineterminator='\n')

                        #Calling the spatial index checker function
                        g,n,dataset,data,data2=SpatialIndexChecker(g,n,dataset,data,data2)

                        #if the feature classes current spatial index matches the default spatial index then it will write to the csv file otherwise it will move on to the next line
                        if data2!=[]:
                            SpatialIndexestobeupdated.writerow(data2)

                        g=g+1


########################################################################################################################################################################################
#SAM CAN PROGRAM LIKE A PRO!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

