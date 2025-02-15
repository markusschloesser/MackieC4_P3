#
#
# Powershell script will copy "updated" .py files found in $path directory to $dest directory.
#
# update the $path below for your local repo location
# update the $MIDI_REMOTE_SCRIPT_NAME if you want
# update the $LIVE_VERSION for your development target version
#
# To run in PyCharm's PowerShell Terminal console Tab:
#           update script as above, create dest remote script folder as below
#           cd to repo directory (any level in $path below?)
#           run the script: .\MackieC4Pro\z_utility\moveC4WipFilesToMidiRemoteScriptsFolder.ps1 (for example)
#


$LIVE_VERSION = 12
# This Remote Script "folder" should already exist at $dest before the script first runs
$MIDI_REMOTE_SCRIPT_NAME = "MackieC4pro_test"   # the name to add to a "remote script slot" in Live midi options

#$QUIET = $false   # make $true to silence console output
#$WHISPER = $true  # make $false to see "loud" (not-quiet) console output


# set source dir
$path = "G:\MackieC4Pro\wip\MackieC4"

# set destination dir
$dest = "C:\ProgramData\Ableton\Live {0} Suite\Resources\MIDI Remote Scripts\{1}" -f $LIVE_VERSION, $MIDI_REMOTE_SCRIPT_NAME

$Source = $path
$Destination = $dest
###################################################
# updated script code adapted courtesy of: James Turns A of their own Q
# https://stackoverflow.com/questions/677789/powershell-copy-item-but-only-copy-changed-files
###################################################

function Get-FileMD5 {
    Param([string]$file)
    $mode = [System.IO.FileMode]("open")
    $access = [System.IO.FileAccess]("Read")
    $md5 = New-Object System.Security.Cryptography.MD5CryptoServiceProvider
    $fs = New-Object System.IO.FileStream($file,$mode,$access)
    $Hash = $md5.ComputeHash($fs)
    $fs.Close()
    [string]$Hash = $Hash
    Return $Hash
}
function Copy-LatestFile{
    Param($File1,$File2,[switch]$whatif)
    $File1Date = get-Item $File1 | foreach-Object{$_.LastWriteTimeUTC}
    $File2Date = get-Item $File2 | foreach-Object{$_.LastWriteTimeUTC}
    if($File1Date -gt $File2Date)
    {
        Write-Host "$File1 is Newer... Copying..."
        if($whatif){Copy-Item -path $File1 -dest $File2 -force -whatif}
        else{Copy-Item -path $File1 -dest $File2 -force}
    }
    else
    {
        #Don't want to copy this in my case..but good to know
        #Write-Host "$File2 is Newer... Copying..."
        #if($whatif){Copy-Item -path $File2 -dest $File1 -force -whatif}
        #else{Copy-Item -path $File2 -dest $File1 -force}
    }
    Write-Host
}

# Getting Files/Folders from Source and Destination
$SrcEntries = Get-ChildItem $Source -Recurse
$DesEntries = Get-ChildItem $Destination -Recurse

# Parsing the folders and Files from entry Collections before any changes
$Srcfolders = $SrcEntries | Where-Object{$_.PSIsContainer}
$SrcFiles = $SrcEntries | Where-Object{!$_.PSIsContainer}
$Desfolders = $DesEntries | Where-Object{$_.PSIsContainer}
$DesFiles = $DesEntries | Where-Object{!$_.PSIsContainer}

# Checking for Folders that are in Source, but not in Destination
foreach($folder in $Srcfolders)
{
    # if $Srcfolders is an empty collection, $folder will be null
    if(!([string]::IsNullOrEmpty($folder)))
    {
        $SrcFolderPath = $source -replace "\\","\\" -replace "\:","\:"
        $DesFolder = $folder.Fullname -replace $SrcFolderPath, $Destination
        if (!(test-path $DesFolder))
        {
            Write-Host "Folder $DesFolder Missing at destination. Creating it!"
            new-Item $DesFolder -type Directory | out-Null
        }
    }
}

# Checking for Folders that are in Destination, but not in Source
foreach($folder in $Desfolders)
{
    # if $Desfolders is an empty collection, $folder will be null
    # (or if) $folder is an empty string (there's nothing to remove)
    if(!([string]::IsNullOrEmpty($folder))) {
        $DesFilePath = $Destination -replace "\\", "\\" -replace "\:", "\:"
        $fullName = $folder.Fullname
        $SrcFolder = $fullName -replace $DesFilePath, $Source
        # if $SrcFolder is an empty string or not "on" a path at source, remove from destination
        if (([string]::IsNullOrEmpty($SrcFolder)) -or !(test-path $SrcFolder))
        {
            Write-Host "Folder $folder Missing from source. Removing it from Destination"
            Remove-Item -path $fullName -force -Recurse # -Recurse or get confirmation prompt because __pycache__ not empty
        }
    }
}

# Checking for Files that are in the Source, but not in Destination
# and adding those Files at Destination
# or if Files exist at both Source and Destination and MD5 hashes are different
# Copying updated (latest) file from Source to Destination (newer Files should never appear at Destination)
foreach($entry in $SrcFiles)
{
    $SrcFullname = $entry.fullname
    $SrcName = $entry.Name
    $SrcFilePath = $Source -replace "\\","\\" -replace "\:","\:"
    $DesFile = $SrcFullname -replace $SrcFilePath,$Destination
    if(test-Path $Desfile)
    {
        $SrcMD5 = Get-FileMD5 $SrcFullname
        $DesMD5 = Get-FileMD5 $DesFile
        If(Compare-Object $srcMD5 $desMD5)
        {
            Write-Host "The Files MD5's are Different... Checking Write
            Dates"
            Write-Host $SrcMD5
            Write-Host $DesMD5
            Copy-LatestFile $SrcFullname $DesFile
        }
    }
    else
    {
        Write-Host "$Desfile Missing... Copying from $SrcFullname"
        copy-Item -path $SrcFullName -dest $DesFile -force
    }
}

# Checking for Files that are in the Destination, but not in Source
# and removing from Destination
foreach($entry in $DesFiles)
{
    $DesFullname = $entry.fullname
    $DesName = $entry.Name
    if (!($DesFullName.Contains("__pycache__"))) # __pycache__ always missing from source, already gone from dest
    {
        $DesFilePath = $Destination -replace "\\", "\\" -replace "\:", "\:"
        $SrcFile = $DesFullname -replace $DesFilePath,$Source
        if (!(test-Path $SrcFile))
        {
            Write-Host "$SrcFile Missing... Removing it from $DesFullname"
            Remove-Item -path $DesFullname -force
        }
    }
}