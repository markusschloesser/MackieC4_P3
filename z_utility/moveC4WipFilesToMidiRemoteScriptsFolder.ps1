#
#
# Powershell script will copy "updated" .py files found in $path directory to $dest directory.
#
# update the $path for your local repo location
# update the $MIDI_REMOTE_SCRIPT_NAME if you want
# update the $LIVE_VERSION for your test version
#
# To run in PowerShell console:
#           update script as above, create dest remote script folder as below
#           cd to repo directory (any level in path)
#           run the script: .\markusC4Repo\z_utility\moveC4WipFilesToMidiRemoteScriptsFolder.ps1 (for example)
#


$LIVE_VERSION = 10
$MIDI_REMOTE_SCRIPT_NAME = "MarkusC4test"   # the name to add to a "remote script slot" in Live midi options
                                            # This "folder" should already exist empty at $dest before the script first runs
$QUIET = $false   # make $true to silence console output


# set source dir
$path = "D:\deadDriveArchive\newStuff\repos\markusC4Repo\wip\MackieC4"

# set destination dir
$dest = "C:\ProgramData\Ableton\Live {0} Suite\Resources\MIDI Remote Scripts\{1}" -f $LIVE_VERSION, $MIDI_REMOTE_SCRIPT_NAME


# When using the -Include parameter, if you do not include an asterisk in the path
# the Get-ChildItem command returns no output.
$include_path = $path + "\*"
$filesAtTestSource = Get-ChildItem -Path $include_path -Include *.py

$include_dest = $dest + "\*"
Foreach($file in $filesAtTestSource) {

    $destFile = Get-Item -Path $include_dest | Where-Object {$_.name -eq $file.name}
    # move only updated .py files
    if ($destFile.LastWriteTime -lt $file.LastWriteTime)
    {
        if ($false -eq $QUIET)
        {
            $msg = "copying newer source <{0}> to dest <{1}>" -f $file.name, $dest
            Write-Output $msg
        }
        Copy-Item -Path $file -Destination $dest
    }
    else
    {
        if ($false -eq $QUIET)
        {
            $msg = "no changes to file <{0}>" -f $destFile.FullName
            Write-Output $msg
        }
    }
}

exit 0

