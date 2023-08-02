# File Date Modification Project

## Table of Contents

- [Overview](https://github.com/Eli-Rousseau/ChangingFileDates#overview)
  
- [Prerequisites](https://github.com/Eli-Rousseau/ChangingFileDates#prerequisites)
  
- [Descriptions](https://github.com/Eli-Rousseau/ChangingFileDates#descriptions)
  
  - [ObtainFileList.ps1](https://github.com/Eli-Rousseau/ChangingFileDates#obtainfilelistps1)
    
  - [ChangeFileDateScript.py](https://github.com/Eli-Rousseau/ChangingFileDates#changefiledatescriptpy)
    
- [Usage](https://github.com/Eli-Rousseau/ChangingFileDates#usage)
  
- [Output](https://github.com/Eli-Rousseau/ChangingFileDates#output)
  
- [Contributing](https://github.com/Eli-Rousseau/ChangingFileDates#contributing)
  
- [License](https://github.com/Eli-Rousseau/ChangingFileDates#license)
  

## Overview

The File Date Modification project is a set of PowerShell and Python scripts that allow users to find all files in a specified directory and modify their creation and modification dates based on a specific date pattern. This project consists of two main scripts: `ObtainFileList.ps1` and `ChangeFileDateScript.py`.

## Prerequisites

Before running the scripts, ensure you have the following requirements met:

- PowerShell installed on your system.
- Python 3.x installed on your system.
- Required Python Libraries:
  - `re` (Regular Expression Operations)
  - `time` (Time access and conversions)
  - `datetime` (Basic date and time types)
  - `win32file` and `pywintypes` (Windows-specific file operations)
  - `os` (Miscellaneous operating system interfaces)

Side note: The Python script uses the `win32file` and `pywintypes` modules to modify the file creation date, and the `os` module to modify the file modification date. Therefore, the script is intended for use on Windows systems.

## Description

### ObtainFileList.ps1

The `ObtainFileList.ps1` script is written in PowerShell and serves as the initial step of the File Date Modification project. It takes a single parameter, `Path`, which should be the fully qualified path to the desired directory. The script's function is to retrieve the fully qualified paths of all files within the specified directory and its subdirectories. It validates the provided path and starts the process of finding files.

Once the files are found, the script creates an output file called `MyFiles.txt`, where it stores the fully qualified paths of all the discovered files. This file will be used as input for the subsequent Python script, `ChangeFileDateScript.py`.

### ChangeFileDateScript.py

The `ChangeFileDateScript.py` script is written in Python and works in conjunction with the `ObtainFileList.ps1` script. Its primary function is to process the information stored in the `MyFiles.txt` input file, containing fully qualified paths to various files.

The script then examines each filename in search of a specific date pattern in the format `YYYYMMDD` (e.g., `20230802`). This date pattern represents the exact creation date of the file. If the script successfully identifies the required date pattern in a filename and confirms that the file's creation and modification dates have not been modified yet, it proceeds to set both the creation and modification dates of that file to match the specified date pattern.

However, if the dates have already been modified or if the date pattern is not found in the filename, the script skips that particular file and continues to the next one without making any changes.

During the process, the script generates an output file named `NotChangedFiles.txt`. This file contains the fully qualified paths of all the files in which the required date pattern was not detected. This log of non-modified files helps keep track of the files that remained unchanged during the execution of the script.

## Usage

Before using the File Date Modification scripts, ensure that you have the repository cloned on your machine. To clone the repository, open a terminal and execute the following command:

```powershell
git clone https://github.com/your-username/file-date-modification.git
```

Replace `your-username` with your GitHub username.

After cloning the repository, change to the working directory of the project:

```powershell
Set-Location -Path "C:\path\to\cloned\directory"
```

Open a PowerShell terminal and execute the `ObtainFileList.ps1` script with the `-Path` parameter. The parameter should be the fully qualified path to the desired directory, where you want to find the files.

```powershell
.\ObtainFileList.ps1 -Path "C:\path\to\your\desired\directory"
```

## Output

After running the `ChangeFileDateScript.py` script, it will display information about the number of files found, the number of files with the correct date pattern, the number of files requiring date modifications, and the number of files without the correct date pattern. The script will also create an output file called `NotChangedFiles.txt` in the same directory, which contains the fully qualified paths of files that did not match the expected date pattern.

## Contributing

Feel free to modify the content according to your preferences, and don't forget to add a license file (e.g., `LICENSE`) to your project if you haven't already.

## License

This project is licensed under the [MIT License](https://github.com/Eli-Rousseau/WSL/blob/master/LICENSE).
