# Import standard built-in python libraries
from datetime import datetime
import os
import re
import sys
import time


# Import thhird party python libraries
import win32file
import pywintypes


def importFiles():
    """
    Function that will import all file paths from MyFiles.txt in the correct format
    """
    # List storing the fully qualified paths to each file
    flist = []

    # Read-in the input file from the current directory
    with open("MyFiles.txt", "r", encoding="utf-16") as myfiles:

        # Properly format each file path in turn
        for file in myfiles.readlines():

            # Removes the redundant part in the beginning of the file path
            file = file[:-1].split("::")[1][:3] + file[:-1].split(":\\")[1]

            # Changing the '\' into '/' character
            file = file.split("\\")
            file = "/".join(file)

            # Adding the formatted path to the new list
            flist.append(file)

    # Closing the input file
    myfiles.close()

    # Returns the list with the fully qualified paths to each file
    return flist


class fileObject:
    """
    Class to initialize methods for the file objects
    """

    def __init__(self, file):
        """
        Initializes the object attributes
        """
        # Define the file attribute
        self.file = file

    def findCreationDate(self):
        """
        Finds the file creation date based on its file path name
        """

        # Finds the current time in %H:%M:%S format
        timepart = time.localtime()
        timepart = time.strftime("%H:%M:%S", timepart)

        # Finds the date from the file path name in %Y%m%d format
        datepart = re.search("\d{8}", self.file)

        # Verifies that the correct pattern was recovered
        if datepart:

            # Combines the date and time as a single string
            datepart = datepart.group()
            pattern = (
                datepart[:4]
                + "-"
                + datepart[4:6]
                + "-"
                + datepart[6:8]
                + " "
                + timepart
            )

        # Otherwise, file that lack the correct pattern
        else:

            # Gets a None as the date and time value
            pattern = None

        # Returns the expected file creation date
        return pattern

    def checkFileCreateDate(self):
        """
        Checks whether the file creation date should be changed
        """

        # Finds the latest file creation date setting
        filedate = time.ctime(os.path.getctime(self.file))
        filedate = datetime.strptime(filedate, "%a %b %d %H:%M:%S %Y")
        filedate = datetime.strftime(filedate, "%Y-%m-%d")

        # Finds the pattern of the expected file creation date
        pattern = self.findCreationDate()[0:10]

        # Check whether the creation date is different
        return True if filedate != pattern else False

    def convertTimestamp(self):
        """
        Converts the creation date of a file in a Unix timestamp
        """

        # Retrieve the date pattern of a file
        pattern = self.findCreationDate()

        # Verifies that a file has a regular date pattern
        if pattern:

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
        """
        Changes the creation date of the input file
        """

        # Retrieve the date pattern of a file
        timestamp = self.convertTimestamp()

        # Verifies that a file has a regular date pattern
        if timestamp:

            # Opens file and get the handle of file
            # API: http://timgolden.me.uk/pywin32-docs/win32file__CreateFile_meth.html
            handle = win32file.CreateFile(
                self.file,
                win32file.GENERIC_WRITE,
                0,
                None,
                win32file.OPEN_EXISTING,
                0,
                0,
            )

            # Creates a PyTime object
            # API: http://timgolden.me.uk/pywin32-docs/pywintypes__Time_meth.html
            PyTime = pywintypes.Time(timestamp)

            # Resets the creation time of file
            # API: http://timgolden.me.uk/pywin32-docs/win32file__SetFileTime_meth.html
            win32file.SetFileTime(handle, PyTime)

    def changeFileModificationDate(self):
        """
        Changes the modification date of the input file
        """

        # Retrieve the date pattern of a file
        timestamp = self.convertTimestamp()

        # Verifies that a file has a regular date pattern
        if timestamp:

            # Resets the file modification date
            os.utime(self.file, (os.path.getatime(self.file), timestamp))


def notchangedFileList(incfiles):
    """
    Writes the list of the non-changed files to the NotChangedFiles.txt file
    """

    # Define the output string
    output = (
        "Here you will find the files that did not match the expected date pattern:\n"
    )
    output += "Total file(s): {}\n".format(len(incfiles))

    # Join the files to the output string
    incfiles = "\n".join(incfiles)
    output += incfiles

    # Write down the output string to the 'NotChangedFiles.txt' file
    with open("NotChangedFiles.txt", "w") as file:

        file.write(output)

    # Close the output file
    file.close()


def main():
    """
    Function that floods the main execution stream of the script
    """

    ## 1. Import the list of file paths
    flist = importFiles()
    sys.stdout.write(
        "A total of {} file(s) were recovered in the specified location.\n".format(
            len(flist)
        )
    )

    ## 2. Grouping files with the correct date pattern
    cfiles = [file for file in flist if fileObject(file).findCreationDate()]
    sys.stdout.write(
        "Of these, {} file(s) have the correct date pattern.\n".format(len(cfiles))
    )

    ## 3. Checking which files require changes
    mfiles = [file for file in cfiles if fileObject(file).checkFileCreateDate()]
    sys.stdout.write(
        "Finally, {} file(s) require a change in modification and creation date.\n".format(
            len(mfiles)
        )
    )

    ## 4. Perform changes in the creation and modification dates of files
    if mfiles:

        for file in mfiles:

            fileObject(file).changeFileCreateDate()
            fileObject(file).changeFileModificationDate()

        sys.stdout.write("The files were successfully modified.\n")

    # The files are already up to date and no changes have to be made
    else:

        sys.stdout.write("All files were already correctly labelled.\n")

    ## 5. Grouping files without the correct date pattern
    incfiles = [file for file in flist if not fileObject(file).findCreationDate()]

    # Writing down the non changed files to an output file
    notchangedFileList(incfiles)
    notchangedfiles = '"{}\\NotChangedFiles.txt"'.format(
        os.getcwd()
    )  # Path to output file
    sys.stdout.write(
        "Files that did not match the expected date pattern can be found in the log file:\n{}".format(
            notchangedfiles
        )
    )


# Verifies whether this is the main execution script
if __name__ == "__main__":
    main()
