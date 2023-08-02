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

    # Read-in the input file from the current directory
    with open('MyFiles.txt', 'r', encoding='utf-16') as myfiles:

        # Properly format each file path in turn
        for file in myfiles.readlines():

            # Removes the redundant part in the beginning of the file path
            file = 'C:' + file[:-1].split('C:')[1]
            
            # Changing the '\' into '/' character
            file = file.split('\\')
            file = '/'.join(file)

            # Adding the formatted path to the new list
            flist.append(file)

    # Closing the input file
    myfiles.close()

    # Returns the list with the fully qualified paths to each file
    return flist


# Class to represent the file object
class fileObject:

    # Method that will initialize the object attributes
    def __init__(self, file):
         
         # Define the file attribute
         self.file = file

    # Method that will derive the creation date of the file
    def findCreationDate(self):

        # Finds the current time in %H:%M:%S format
        timepart = time.localtime()
        timepart = time.strftime('%H:%M:%S', timepart)

        # Finds the date from the file path name in %Y%m%d format 
        datepart = re.search('\d{8}', self.file)

        # Verifies that the correct pattern was recovered
        if datepart != None: 

            datepart = datepart.group()
            datepart = datepart[:4] + '-' + datepart[4:6] + '-' + datepart[6:8]

            # Combines the date and time as a single string
            pattern = datepart + ' ' + timepart

        # Otherwise, file that lack the correct pattern 
        else:

            # Gets a None as the date and time value
            pattern = None

        # Returns the expected file creation date
        return pattern
    
    # Method that will check whether the file creation date should be changed
    def checkFileCreateDate(self):

        # Finds the latest file creation date setting
        filedate = time.ctime(os.path.getctime(self.file))
        filedate = datetime.strptime(filedate, '%a %b %d %H:%M:%S %Y')
        filedate = datetime.strftime(filedate, '%Y-%m-%d')

        # Finds the pattern of the expected file creation date
        pattern = self.findCreationDate()[0:10]

        # If the two variables are equal
        if filedate == pattern:

            # The file creation date should not be changed
            return False
    
        # Else the variables are not equal
        else:

            # The file creation date should be changed
            return True
    
    # Method that will convert the creation date of a file in a Unix timestamp
    def convertTimestamp(self):

        # Retrieve the date pattern of a file
        pattern = self.findCreationDate()

        # Verifies that a file has a regular date pattern
        if pattern != None:

            # Converts the input string to a datetime object
            dtobject = datetime.strptime(pattern, "%Y-%m-%d %H:%M:%S")

            # Converts the datetime object to a Unix timestamp
            timestamp = dtobject.timestamp()

        # Otherwise, file that lack the correct pattern 
        else:

            # Gets a None as the timestamp
            timestamp = None

        # Returns the file timestamp
        return timestamp
    
    # Method that will change the creation date of the input file
    def changeFileCreateDate(self):

        # Retrieve the date pattern of a file
        timestamp = self.convertTimestamp()

        # Verifies that a file has a regular date pattern
        if timestamp != None:

            # Opens file and get the handle of file
            # API: http://timgolden.me.uk/pywin32-docs/win32file__CreateFile_meth.html
            handle = win32file.CreateFile(self.file, win32file.GENERIC_WRITE, 0, None, win32file.OPEN_EXISTING, 0, 0)

            # Creates a PyTime object
            # API: http://timgolden.me.uk/pywin32-docs/pywintypes__Time_meth.html
            PyTime = pywintypes.Time(timestamp)

            # Resets the creation time of file
            # API: http://timgolden.me.uk/pywin32-docs/win32file__SetFileTime_meth.html
            win32file.SetFileTime(handle, PyTime)

    # Method that will change the modification date of the input file
    def changeFileModificationDate(self):

        # Retrieve the date pattern of a file
        timestamp = self.convertTimestamp()

        # Verifies that a file has a regular date pattern
        if timestamp != None:

            # Resets the file modification date
            os.utime(self.file, (os.path.getatime(self.file), timestamp))


# Function that will display return the list of the non-changed files
def notchangedFileList(incfiles):

    # Define the output string
    output = 'Here you will find the files that did not match the expected date pattern:\n'
    output += 'Total file(s): {}\n'.format(len(incfiles))

    # Add each of the files to the output string
    for file in incfiles:

        output += file + '\n'
    
    # Write down the output string to the 'NotChangedFiles.txt' file
    with open('NotChangedFiles.txt', 'w') as file:

        file.write(output)

    # Close the output file
    file.close()


# Function that floods the main stream of the script
def main():
    
    # Import the list of file paths
    flist = importFiles()
    sys.stdout.write('A total of {} file(s) were recovered in the specified location.\n'.format(len(flist))) # Write text to the console

    # Grouping files with the correct date pattern
    cfiles = [file for file in flist if fileObject(file).findCreationDate() != None]
    sys.stdout.write('Of these, {} file(s) have the correct date pattern.\n'.format(len(cfiles))) # Write text to the console

    # Checking which files require changes
    mfiles = [file for file in cfiles if fileObject(file).checkFileCreateDate()]
    sys.stdout.write('Finally, {} file(s) require a change in modification and creation date.\n'.format(len(mfiles))) # Write text to the console

    # Perform changes in the creation and modification dates of files
    if len(mfiles) != 0:

        for file in mfiles:

            fileObject(file).changeFileCreateDate()
            fileObject(file).changeFileModificationDate()
    
        sys.stdout.write('The files were successfully modified.\n') # Write text to the console
    
    # The files are already up to date and no changes have to be made
    else:
        
        sys.stdout.write('All files were already correctly labelled.\n') # Write text to the console
    
    # Grouping files without the correct date pattern
    incfiles = [file for file in flist if fileObject(file).findCreationDate() == None] # Incorrect files
    sys.stdout.write('Files that did not match the expected date pattern can be found in the log file:\n') # Write text to the console

    # Writing down the non changed files to an output file
    notchangedFileList(incfiles)
    notchangedfiles = '"{}\\NotChangedFiles.txt"'.format(os.getcwd()) # Path to output file
    sys.stdout.write(notchangedfiles) # Write text to the console

main()