#-------------------------------------------------------------------------------
# Name:        LISTPROD Data Backup Version 2.1
# Purpose:
#
# Author:      salangley
#
# Created:     09/10/2013
# Copyright:   (c) salangley 2013
#-------------------------------------------------------------------------------

#IMPORT MODULES
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
import arcgisscripting
import gc
import ast

from email.MIMEText import MIMEText
from types import *

from email.MIMEText import MIMEText
from types import *

################################################################################
#GETS TODAYS DATE
def getTodayDate():
    """
    Get today's date in format YYYYMMDD
    Keyword arguments:
    Returns:
    YYYYMMDD String.
    Notes:
    """
    now = datetime.datetime.now()
    yearStr = str(now.year)

    # Get the month in format MM
    if (now.month < 10):
        monthStr = "0" + str(now.month)
    else:
        monthStr = str(now.month)

    # Get the Day in format DD
    if (now.day < 10):
        dayStr = "0" + str(now.day)
    else:
        dayStr = str(now.day)

    # Build the string and return
    todayStr = yearStr + monthStr + dayStr
    return todayStr

################################################################################
#ZIPS THE GEODATABASE
def zipFileGeodatabase(inFileGeodatabase, newZipFN):
    if not (os.path.exists(inFileGeodatabase)):
        return False

    if (os.path.exists(newZipFN)):
        os.remove(newZipFN)

    zipobj = zipfile.ZipFile(newZipFN,'w')

    for infile in glob.glob(inFileGeodatabase+"/*"):
        zipobj.write(infile, os.path.basename(inFileGeodatabase)+"/"+os.path.basename(infile), zipfile.ZIP_DEFLATED)

    zipobj.close()

    return True

################################################################################
#SENDS AN EMAIL TO MYSELF AND JOHN ANDERSON
def sendEmail(emailbody,
              emailTo,
              subject,
              smtpserver='postoffice.dpiwe.tas.gov.au'):
    """
    Send email from Python.

    Keyword arguments:
    emailbody     String containing body of email
    emailTo       List of recipients.  sendmail() takes a list of recipients
    subject       String containing subject of email
    smtpserver    Optional : smtpserver name


    Notes:
    """

    try:
        strFrom = 'Samuel.Langley@dpipwe.tas.gov.au'
        strTo = ''.join(emailTo) # Convert list of email recipents to String

        # Create a text/plain message
        msgRoot = MIMEText(emailbody)
        msgRoot['Subject'] = subject
        msgRoot['From'] = strFrom
        msgRoot['To'] = strTo

errDesc:
        print("SMTPConnectError : ", errDesc)
        logging.critial("SMTPConnectError : " + errDesc)
    except smtplib.SMTPException, errDesc:
        print("SMTPException : ", errDesc)
        logging.critical("SMTPException : " + errDesc)
    except:
        print "Exception Error in emailSender : ", sys.exc_info()[0]
        print sys.exc_info()[1]
        print sys.exc_info()[2]
        logging.critical("Exception Error in emailSender : " + sys.exc_info()[0])
        logging.critical(sys.exc_info()[1])
        logging.critical(sys.exc_info()[2])

################################################################################
#DETERMINES THE LOGFILE BASED UPON THE USERNAME AND OPERATING SYSTEM EG WINDOWS
#XP OR WINDOWS 7
def LogFileDirectory():
    OperatingSystem=platform.release()
    Platform=sysconfig.get_platform()
    Username= getpass.getuser()

    print OperatingSystem
    print Platform
    print Username

    if OperatingSystem == "XP":
        logdir="C:\Documents and Settings\\"+Username+"\\Application Data\ESRI\Desktop10.0\ArcToolbox\History\\"
    elif OperatingSystem == "post2008Server":
        logdir="C:\\Users\\"+Username+"\\AppData\\Roaming\\ESRI\\Desktop10.0\\ArcToolbox\\History\\"
    else:
        print "Unrecognised Operating System"

    return logdir

######################################################################################################################
def RemoveDataFilter(FeatureClasses1,FeatureDatasets1,Tables1,FeatureClassRemove,FeatureDatasetRemove,TablesRemove):

    #Attempting to remove a feature dataset from the list derived from the SECOND Filter (FeatureDataset2) from the list derived from the FIRST Filter (FeatureDataset1)
    #to obtain a final list of feature datsets to copy (FeatureDataset1)
    i = 0
    for match in FeatureDatasetRemove:

        try:
            FeatureDatasets1.remove(match)
        except ValueError:
            print""
        i=i+1

        except ValueError:
            print""
        i=i+1

    return FeatureClasses1,FeatureDatasets1,Tables1

##################################################################################################
#PROVIDES A LIST OF FEATURE CLASSES, FEATURE DATASET AND TABLES FOR THE PROGRAM TO COPY AND BACK UP
def FILTERDATASETS(filterstring,databaseconnection):


    gp = arcgisscripting.create(10.1)
    gp.workspace = databaseconnection

    #A case parameter as to whether at least one feature class has been found
    datafound=0

    #Lists the feature classes, feature datasets and tables within the database
    fcs = gp.ListFeatureClasses()
    fds = gp.ListDatasets()
    tbls = gp.ListTables()

    #Defining the search sysbol as a string varialbe
    asterixsearch = "*"

    #Defining the list for copy Feature Classes from databse connections
    FeatureClasses=[]

    #Defining the list for copy Feature datasets from databse connections
    FeatureDatasets=[]

    #Defining the list for copy Tables from databse connections
    Tables=[]


    copydatalist=[]

    #If there is no filter string
    if filterstring == "":

        #Getting all the Feature classes from database connection and appending to the copydatalist
        for fc in fcs:
            FeatureClasses.append(fc)

        #Getting all the Feature datasets from database connection and appending to the copydatalist
        for fd in fds:
            FeatureDatasets.append(fd)

        #Getting all the Tables from database connection and appending to the copydatalist
        for tbl in tbls:
            Tables.append(tbl)


        return FeatureClasses,FeatureDatasets,Tables

    #If there is an * at both ends
    if filterstring[len(filterstring)-1] == asterixsearch and filterstring[0] == asterixsearch:
            print "* at both ends"

            #Looping through all feature classes
            for fc in fcs:

                #Defining filter string
                filterstring_temp=filterstring.replace(asterixsearch,"")

                #Determing if the feature classes name contains the filter string
                if fc.find(filterstring_temp) != -1:
                    FeatureClasses.append(fc)

            #Looping through all feature datasets
            for fd in fds:

                #Defining filter string
                filterstring_temp=filterstring.replace(asterixsearch,"")

                #Determing if the feature datasets name contains the filter string
                if fd.find(filterstring_temp) != -1:
                    FeatureDatasets.append(fd)


            #Looping through all Tables
            for tbl in tbls:

                #Defining filter string
                filterstring_temp=filterstring.replace(asterixsearch,"")

                #Determing if the tables name contains the filter string
                if tbl.find(filterstring_temp) != -1:
                    Tables.append(tbl)

            #returning a list of datasets to be copied
            return FeatureClasses,FeatureDatasets,Tables
#SSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBOOOOOOOOOOOOOOOOOOOOOOOOOOO
#SSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBOOOOOOOOOOOOOOOOOOOOOOOOOOO
#SSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBOOOOOOOOOOOOOOOOOOOOOOOOOOO
#SSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBOOOOOOOOOOOOOOOOOOOOOOOOOOO
#SSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBOOOOOOOOOOOOOOOOOOOOOOOOOOO
#SSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBOOOOOOOOOOOOOOOOOOOOOOOOOOO
#SSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBOOOOOOOOOOOOOOOOOOOOOOOOOOO
#SSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBOOOOOOOOOOOOOOOOOOOOOOOOOOO
    #If there is * at the front
    if filterstring[0] == asterixsearch and filterstring[len(filterstring)-1]!= asterixsearch:

            print "* at the start"

            #Looping through all feature classes
            for fc in fcs:

               #Defining filter string
                filterstring_temp=filterstring.replace(asterixsearch,"")
                print fc

                #Determining if the filter string is at the end of feature classes name
                if fc.endswith(filterstring_temp)==1:

                    FeatureClasses.append(fc)

            #Looping through all feature datasets
            for fd in fds:

               #Defining filter string
                filterstring_temp=filterstring.replace(asterixsearch,"")

                #Determining if the filter string is at the end of feature datasets name
                if fd.endswith(filterstring_temp)==1:

                    FeatureDatasets.append(fd)


            #Looping through all Tables
            for tbl in tbls:

               #Defining filter string
                filterstring_temp=filterstring.replace(asterixsearch,"")

                #Determining if the filter string is at the end of tables name
                if tbl.endswith(filterstring_temp)==1:

                    Tables.append(tbl)

            return FeatureClasses,FeatureDatasets,Tables


    #If there is * at the end
    if filterstring[len(filterstring)-1] == asterixsearch and filterstring[0] != asterixsearch:

            print "* at the end"

            #Looping through all feature classes
            for fc in fcs:

                #Defining the filter string
                filterstring_temp=filterstring.replace(asterixsearch,"")

                #Determining if the filter string is at the start of feature classes name
                if fc.startswith(filterstring_temp)==1:

                    FeatureClasses.append(fc)

       
        #Getting all the dataset from the list
        datasetname=copydatalist[g]
        datasettobecopied=databaseconnection+datasetname
        filestorageplace=directory+"\\"+Filename+"\\"+datasetname

        datasettobecopied=databaseconnection+"\\"+datasetname

####################################################################################

        #Copies the file for either Feature Dataset, Feature Class or Table (depending what datasetype type is equalled to)
        try:

            arcpy.Copy_management(datasettobecopied, filestorageplace, datasettype)
            copylog=copylog+"SUCCESS!!!, the " + datasettype + " " + datasetname + " copy is now complete.\n"
            u=u+1

        #If copy fails then it is recorded into the log file along with type of error
        except Exception, e:
            copylog=copylog + "\n"
            copylog=copylog+"ERROR!!!, the " + datasettype +" "+ datasetname +" has failed.\n"
            e=str(e)
            copylog=copylog+e
            copylog=copylog + "\n"
            failedtocopy=failedtocopy+1

        g=g+1


    return copylog,failedtocopy,u
##########################################################################################################################################################
#CREATES A NEW GEODATABASE
#Creating a string that writes a log in relation to the process of backing up
#data.  This log will be displayed on the top of the email.
copylog=""
todaystr=getTodayDate()
date=todaystr

mm=date[4:6]
dd=date[6:8]
yr=date[0:4]

copylog=copylog+ "The date of backup is "+dd+"-"+mm+"-"+yr+'\n'

#Creating the daily file name based upon the actual date of backup, for both
#geodatabase and zip file
AorB=sys.argv[-1]
Filename="LISTPRODBackup"+AorB+yr+mm+dd+".gdb"
Filenamezipped=AorB+yr+mm+dd+".zip "
print Filename
directory = "C:\LISTPROD_Data_Backup\BackUpFiles"

#Creates a geodatabase to copy the files to to back up
copylog=copylog+"Creating: new geodatabase"+Filename+'\n'
Filenamezipped="LISTPRODBackup"+AorB+date+".zip"

#Creates a geodatabase
try:
    LISTPROD_Data_Backup = directory
    arcpy.CreateFileGDB_management(LISTPROD_Data_Backup, Filename, "CURRENT")
    copylog=copylog+"new geodatabase"+Filename+" has now been created"+'\n'

#If todays geodatabase has already been back up then delete the existing
#one and replace with a new one
except Exception, e:
    copylog=copylog+"Overwriting existing geodatabase"+'\n'

    # Local variables:
    filetobedeleted = LISTPROD_Data_Backup+"\\"+Filename

    # Deletes the old GeodataBase
    arcpy.Delete_management(filetobedeleted, "Workspace")

    #Overwrites creates a new updated Geodatabase
    arcpy.CreateFileGDB_management(LISTPROD_Data_Backup, Filename, "CURRENT")

################################################################################
#OPENS TEXT FILE TO COPY THE DATASETS LISTED IN TEXTFILE TO THE NEW GEODATABASE

#Defining the path of the input text file
textfile=sys.argv[-2]
print textfile
f = open(textfile)

#Defining a counter to be used to determine the number of datasets that have failed to copy across
failedtocopy=0

#opens the text file that lists all the datasets to be backed up, loops through
#and copies each files onto the geodatabase LISTPROD_Data_Backup.
copylog=copylog+"Getting ready to copy files..............\n"
copylog=copylog + "\n"

datasource=f.readlines();

#Defining i as a counter for looping through each line in text file
i=0

#Number of lines in text file
n=len(datasource)

#Defining a variable to check if a line is valid or not
ValidLine=1

#Defining a varialbe that checks to if there is a second filter
SecondFilter=1

#Looping through each line in text file
while i<n:
    parametervalidation=0
    strSearchString =","
    parameterline=datasource[i]
    parameterline=re.split(strSearchString,parameterline)

    #Checking to see if the database connection is valid
    try:
        databaseconnection=""
        databaseconnection=parameterline[0]
        databaseconnection=databaseconnection.replace("\n","")
        databaseconnection=databaseconnection+"\\"

        gp = arcgisscripting.create(10.1)
        gp.workspace = databaseconnection

        fcs = gp.ListFeatureClasses()

        for fc in fcs:
            print "CONNECTION WORKS.................."
            break


    #Except Index error as user input error; as this code has to contain at least two parameter input comma seperated format and
    #importantly  notify the user that the input database connection in invalid
    except Exception,e:
        print str(e)
        copylog=copylog + "INPUT ERROR! " + databaseconnection + " is not valid, please check the text file.\n"
        fail="[LISTPROD BACKUP HAS FAILED] either one or more layers have failed or there is an invalid input from text file.\n"
        ValidLine=0

    #If the connection is valid then...
    if ValidLine==1:

        #Obtaining the feature class filter string
        try:
            filterstring=""
            filterstring=parameterline[1]
            filterstring=filterstring.replace("\n","")

        #Checking to see if the input is valid
        except:

            IndexError

#SSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBOOOOOOOOOOOOOOOOOOOOOOOOOOO

            #Checking to see if the input is valid
            except:

                IndexError

                #Reporting Input Error in email
                copylog=copylog + "INPUT ERROR! " + filterstring + " is not valid, please check the text file.\n"
                copylog=copylog + "INPUT ERROR! Unable to retrieve input, check to see that there is at least 2 parameters in the textfile on Line " + str(i+1) + ", also that they are seperated by commas and check for unnecessary spaces.\n"
                fail="[LISTPROD BACKUP HAS FAILED] either one or more layers have failed or there is an invalid input from text file.\n"
                SecondFilter=0
                ValidLine=0

            #If input is valid then....
            if ValidLine==1:

                #Calling the FILTERDATASETS Function to obtain a list of all the feature classes, feature datasets and tables under the specified FIRST Filter
                FeatureClasses1,FeatureDatasets1,Tables1=FILTERDATASETS(filterstring,databaseconnection)

                #Defining a list of feature classes, feature datasets and tables that are to be removed when applying the filters,
                #e.g these will be the input parameters for RemoveDataFilter() function
                FeatureClassRemove=[]
                FeatureDatasetRemove=[]
                TablesRemove=[]

            #Obtaining a list of oracle views that are to be appended to the list of tables that are to be removed
            try:
                sql_execute = arcpy.ArcSDESQLExecute(databaseconnection)
                views = sql_execute.execute("select user || '.' || t1.view_name from sys.dual, user_views t1")

                #Defining a counter to loop through the list of view tables
                v=0

                #If the return type is a list then there must be at least 2 oracle view tables
                #Appending the view tables to list of tables that are to be removed
                if type(views) is list:
                    h=len(views)
                    while v<h:

                        #Appending the view tables to list of tables that are to be removed
                        TablesRemove=TablesRemove+views[v]
                        print views[v]
                        v=v+1

                #If the return type is a unicode then there must be ONE oracle view table.
                if type(views) is unicode:

                    #Converting views from unicode to a list format
                    views=[views]
                    views=list(views)

                    #Appending the view table to list of tables that are to be removed
                    TablesRemove=TablesRemove+views

            except ValueError:
                print""

            #If there is SecondFilter defined then break down the string into parts as defined by ";" to obtain all the subfilters contained within the Second....
            if SecondFilter!=0:

                #Defining the number of subfilters
                x=0

                #Breaking down filter string into sub components
                strSearchString2 =";"
                filterstring2=re.split(strSearchString2,filterstring2)


                #Creating a loop, to go through all the the filters listed in the sub components.
                z=len(filterstring2)

                while x<z:
                    filterstring=filterstring2[x]

                    #Calling the FILTERDATASETS Function to obtain a list of Feature Classes, Feature Datasets and tables under the SECOND Filter,
                    #this represents a list of datsets that are to be NOT included in the main list
                    FeatureClasses2,FeatureDatasets2,Tables2=FILTERDATASETS(filterstring,databaseconnection)

                    #Adding to the list, that represent thefeature classes, feature datasets and tables that are to be removed
                    FeatureClassRemove=FeatureClassRemove+FeatureClasses2
                    FeatureDatasetRemove=FeatureDatasetRemove+FeatureDatasets2
                    TablesRemove=TablesRemove+Tables2

                    #Moving on to the next filter
                    x=x+1

            #Calling the RemoveDataFilter function to remove the datasets that are listed from the above function from the original list of datsets listed under the first filter.  This will
            #finally contain the list of datasets that are to be copied after applying the 2 filters
            FeatureClasses1,FeatureDatasets1,Tables1=RemoveDataFilter(FeatureClasses1,FeatureDatasets1,Tables1,FeatureClassRemove,FeatureDatasetRemove,TablesRemove)

            #Defining the number of features copied under a specific filter for the purpose of testing to see if at least one feature has been copied across from a particular line.
            u=0

            #This looks at the list of all the feature classes and copies them to the geodatabase by calling the COPYINGDATASETS function
            datasettype="FeatureClass"
            copydatalist=FeatureClasses1

            copylog,failedtocopy,u=COPYINGDATASETS(Filename,directory,databaseconnection,copydatalist,datasettype,copylog,failedtocopy,u)

            #This looks at the list of all the feature datasets and copies them to the geodatabase by calling the COPYINGDATASETS function
            datasettype="FeatureDataset"
            copydatalist=FeatureDatasets1
            copylog,failedtocopy,u=COPYINGDATASETS(Filename,directory,databaseconnection,copydatalist,datasettype,copylog,failedtocopy,u)

            #This looks at the list of all the tables and copies them to the geodatabase by calling the COPYINGDATASETS function
            datasettype="Table"
            copydatalist=Tables1
            copylog,failedtocopy,u=COPYINGDATASETS(Filename,directory,databaseconnection,copydatalist,datasettype,copylog,failedtocopy,u)

            #If there are no features in the list then display a warning in the email
            if u==0:
                copylog=copylog + "\n"
                copylog=copylog + "WARNING!!! There are no datasets to be copied under the " + filterstring + " filter string, please check line " + str(i+1)+" in the text file.\n"
                copylog=copylog + "\n"
                warning="[LISTPROD BACKUP WARNING]"

            if failedtocopy !=0:
                fail="[LISTPROD BACKUP HAS FAILED]"

    i=i+1

##################################################################################
#ZIPPING GEODATABASE AND DELETING THE OLD UNZIPPED GEODATABASE

infile = directory+"\\"+Filename

#Compressing the geodatabase
try:
    print "Compressing the geodatabase...."
    # Process: Compress the data
    arcpy.CompressFileGeodatabaseData_management(infile)

except:
    # If an error occurred while running the tool print the messages
    print arcpy.GetMessages()

outfile = directory+"\\"+Filenamezipped
copylog=copylog + "\n"
copylog=copylog+"Zipping"+Filename+'\n'

try:
    zipFileGeodatabase(infile,outfile)
    copylog=copylog+Filename+"has been zipped up.\n"

    # Local variables:
    filetobedeleted = infile

    # Deletes the old GeodataBase
    arcpy.Delete_management(filetobedeleted, "Workspace")
    copylog=copylog+"geodatabase has now been deleted and replaced by zip file.\n"


    #Deletes the zip file for the same day 2 months ago
    mm=date[4:6]
    mm=int(mm)
    yr=date[1:4]
    yr=int(yr)+2000
    if mm==1 or mm==2:
        mm=mm+10
        yr=yr-1
    else:
        mm=mm-2
        if mm<10:
            mm=str(mm)
            mm="0"+mm
    yr=str(yr)
    mm=str(mm)
    dd=str(dd)
    dailyzippedtobedeleted=AorB+yr+mm+dd+".zip"

    try:
        os.remove(directory+"\\"+dailyzippedtobedeleted)
        copylog=copylog+"Deleting zip file from 2 months ago"+dailyzippedtobedeleted+'\n'

    except Exception, e:
        copylog=copylog+"There is no file for this day 2 months ago.\n"

except IOError:

    copylog=copylog+Filename+"has been zipped up.\n"

    # Local variables:
    filetobedeleted = infile

    # Deletes the old GeodataBase
    arcpy.Delete_management(filetobedeleted, "Workspace")
    copylog=copylog+"geodatabase has now been deleted and replaced by zip file.\n"


    #Deletes the zip file for the same day 2 months ago
    mm=date[4:6]
    mm=int(mm)
    yr=date[1:4]
    yr=int(yr)+2000
    if mm==1 or mm==2:
        mm=mm+10
        yr=yr-1
    else:
        mm=mm-2
        if mm<10:
            mm=str(mm)
            mm="0"+mm
    yr=str(yr)
    mm=str(mm)
    dd=str(dd)
    dailyzippedtobedeleted=AorB+yr+mm+dd+".zip"

    try:
        os.remove(directory+"\\"+dailyzippedtobedeleted)
        copylog=copylog+"Deleting zip file from 2 months ago"+dailyzippedtobedeleted+'\n'

    except Exception, e:
        copylog=copylog+"There is no file for this day 2 months ago.\n"

#SSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBOOOOOOOOOOOOOOOOOOOOOOOOOOO
#SSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBOOOOOOOOOOOOOOOOOOOOOOOOOOO
#SSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBOOOOOOOOOOOOOOOOOOOOOOOOOOO
#SSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBOOOOOOOOOOOOOOOOOOOOOOOOOOO
#SSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBOOOOOOOOOOOOOOOOOOOOOOOOOOO
#SSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBOOOOOOOOOOOOOOOOOOOOOOOOOOO
####################################################################################
#GRABBING THE MOST RECENT LOG FILE AND OPENING IT, COPYING THE TEXT AND PASTING
#IT IN AN EMAIL AND SENDING IT TO MYSELF AND JOHN ANDERSON

print "creating logfile"
logdir= LogFileDirectory()

print logdir

logfiles = filter(os.path.isfile, glob.glob(logdir + "*"))
logfiles.sort(key=lambda x: os.path.getmtime(x))

mostrecentlogfilename = (logfiles[-1],)
mostrecentlogfilename=''.join(mostrecentlogfilename)
print mostrecentlogfilename
f = open(mostrecentlogfilename)
body = f.readlines();
print body
body=''.join(body)
logfilename=mostrecentlogfilename.split(logdir)
logfilename=logfilename[-1]
copylog=copylog+"####################################################################.\n"

####################################################################################
#EMAILING LOG FILE TO THE PEOPLE LISTED ON MY EMAIL LIST
emailfile="C:\LISTPROD_Data_Backup\EmailList.txt"
f=open(emailfile)
emaillist=f.readlines();
e=0
n=len(emaillist)
while e<n:
    body=copylog+body
    emailbody=body
    emailTo=emaillist[e]
    print emailTo

    try:
        subject=fail+" "+warning
        subject="[LISTPROD BACKUP WARNING & FAILURE]"

    except NameError:

        try:
            subject=fail

        except NameError:

            try:
                subject=warning

            except NameError:

                subject="[LISTPROD BACKUP SUCCESSFUL]"
    smtpserver='postoffice.dpipwe.tas.gov.au'
    sendEmail(emailbody,emailTo,subject,smtpserver)
    e=e+1

###################################################################################
