# Import the required Python modules
import re
import time
from datetime import datetime
import win32file, pywintypes
import os
import sys


# Function that will import all file paths in the correct format
def importFiles():

    # List storing the fully qualified paths to each file
    flist = []

    # Read-in the file 'MyFiles.txt' from the current directory
    with open('MyFiles.txt', 'r', encoding='utf-16') as file:

        for f in file.readlines():
            f = formatFilePath(f[:-1]) # Formatting the path of a single file
            flist.append(f)

    file.close()

    # Returns the list with the fully qualified paths to each file
    return flist


# Function that well format the file path correctly
def formatFilePath(file):

    # Removes the redundant part in the beginning of the file path
    file = 'C:' + file.split('C:')[1]

    # Changing the '\' into '/' character
    file = file.split('\\')
    file = '/'.join(file)

    # Returns the correctly formatted file path
    return file


# Function that will derive the creation date from the formatted file paths
def findCreationDate(file):

    # Finds the current time in %H:%M:%S format
    ctime = time.localtime()
    ctime = time.strftime('%H:%M:%S', ctime)

    # Finds the date from the file path name in %Y%m%d format 
    date = re.search('\d{8}', file)

    # Verifies that the correct pattern was recovered
    if date != None: 

        date = date.group()
        date = date[:4] + '-' + date[4:6] + '-' + date[6:8]

        # Combines the date and time as a single string
        cdate = date + ' ' + ctime

        # Converts the input string to a datetime object
        dtobject = datetime.strptime(cdate, "%Y-%m-%d %H:%M:%S")

        # Converts the datetime object to a Unix timestamp
        timestamp = dtobject.timestamp()

    # Files that lack the correct pattern 
    else:

        # Gets a None as timestamp value
        timestamp = None

    # Returns the file path together with its corresponding date and timestamp
    return (file, timestamp)


# Function that will check whether the timestamp of a file should be changed
def checkFileCreateDate(file, timestamp):

    # Finds the file properties derived creation date
    prdate = time.ctime(os.path.getctime(file))
    prdate = datetime.strptime(prdate, '%a %b %d %H:%M:%S %Y')
    prdate = datetime.strftime(prdate, '%Y-%m-%d')
    
    # Convert timestamp to the file pattern derived creation date
    cdate = datetime.utcfromtimestamp(timestamp)
    cdate = cdate.strftime('%Y-%m-%d')

    # If the two variables are equal
    if prdate == cdate:

        # The file's timestamp should not be changed
        return False
    
    # Else the variables are not equal
    else:

        # The file's timestamp should be changed
        return True


# Function will change the creation date of the input file to its corresponding timestamp
def changeFileCreateDate(file, timestamp):

    # Opens file and get the handle of file
    # API: http://timgolden.me.uk/pywin32-docs/win32file__CreateFile_meth.html
    handle = win32file.CreateFile(file, win32file.GENERIC_WRITE, 0, None, win32file.OPEN_EXISTING, 0, 0)

    # Creates a PyTime object
    # API: http://timgolden.me.uk/pywin32-docs/pywintypes__Time_meth.html
    PyTime = pywintypes.Time(timestamp)

    # Resets the creation time of file
    # API: http://timgolden.me.uk/pywin32-docs/win32file__SetFileTime_meth.html
    win32file.SetFileTime(handle, PyTime)


# Function that will display return the list of the non-changed files
def nchangeFileList(nchfiles):

    # Define the output string
    output = 'Here you will find the files that did not match the expected date pattern:\n'
    output += 'Total file(s): {}\n'.format(len(nchfiles))

    # Add each of the files to the output string
    for f in nchfiles:

        output += f[0] + '\n'
    
    # Write down the output string to the 'NotChangedFiles.txt' file
    with open('NotChangedFiles.txt', 'w') as file:

        file.write(output)

    file.close()


# Function that will change the modification date of the input file to its corresponding timestamp
def changeFileModificationDate(file, timestamp):

    # Resets the modification time of file
    os.utime(file, (os.path.getatime(file), timestamp))


# Import the list of file paths
flist = importFiles()
sys.stdout.write('A total of {} file(s) were recovered in the specified location.\n'.format(len(flist))) # Write text to the console

# Determine the timestamp of each file
dlist = [findCreationDate(f) for f in flist]

# Grouping files with the correct date pattern
cfiles = [f for f in dlist if f[1] != None] # Correct files
sys.stdout.write('Of these, {} file(s) have the correct date pattern.\n'.format(len(cfiles))) # Write text to the console

# Checking which files require changes
mfiles = [f for f in cfiles if checkFileCreateDate(f[0], f[1])]
sys.stdout.write('Finally, {} file(s) require a change in modification and creation date.\n'.format(len(mfiles))) # Write text to the console

# Perform changes in the creation and modification dates of files
if len(mfiles) != 0:

    for f in mfiles:

        changeFileCreateDate(f[0], f[1])
        changeFileModificationDate(f[0], f[1])
        sys.stdout.write('The files were successfully modified.\n') # Write text to the console

# The files are already up to date and no changes have to be made
else:
    
    sys.stdout.write('All files were already correctly labelled.\n') # Write text to the console

# Grouping files without the correct date pattern
incfiles = [f for f in dlist if f[1] == None] # Incorrect files
nchangeFileList(incfiles)
sys.stdout.write('Files that did not match the expected date pattern can be found in the log file:\n') # Write text to the console
sys.stdout.write('"C:\\Users\\rouss\\Documents\\Programming Projects\\Python\\ChangingFileDates\\NotChangedFiles.txt"') # Write text to the console
