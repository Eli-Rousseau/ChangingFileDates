# Define the Path Parameter to the desired directory to execute the script
param 
(
    [Parameter(Mandatory=$true)][System.String]$Path
)

# Check the validity of the provided path
if (Test-Path -Path $Path -PathType "Container")
{
    Write-Host "The folder is valid, let's get started."
}
else 
{
    Write-Host "You entered an invalid path."
    Write-Host "Try again by providing the fully qualified path to a valid directory."
    exit
}

# Retrieve the fully qualified path of alle files for which the date has to be changed
$files = Get-ChildItem -Path $Path -Recurse -Attributes "a" | ForEach-Object {$_.PSParentPath + '\' + $_.Name}

# Send list of files to a text file
$files | Out-File -FilePath ".\MyFiles.txt" -Encoding "bigendianunicode"

# Perform all the changes from the python script
python "./ChangeFileDateScript.py"