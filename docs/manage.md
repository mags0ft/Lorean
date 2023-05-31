# Managing backups

Lorean has a built-in backup manager which shows you the size of each backup and whether it contains errors. To learn how to use it, please follow along the instructions below.

## Instructions

1. Navigate to the home page and hit the "Manage" button.
2. Select the drive and location containing all your backup folders.
3. Wait for the analysis to finish.

You should see something like this:
![Backup manager image](./images/screenshot-manage.png)
You can click on the individual boxes to reveal the size and potential problems of the corresponding backup folder.

**Note** that a red tinted box indicates there are **problems** with this backup you should resolve, a green one indicated the backup is okay.

## What to do if problems are found

It's unlikely that there are problems with a backup - if there are, you should definetly do the following:

1. Re-run the backup to ensure that you really have the data all safe.
2. Read the error messages. If the backup is missing files, this might possibly point out your backup drive is damaged and therfore lost some files. Replace your drive with a new one and **re-run all backups that were on the old drive**. If the backup is incomplete and really not missing files, that just implies the computer or Lorean crashed while still running the backup. In really rare cases, there might be **more** files than expected inside of the backup. Reasons could be you accidentally copied some files into your backup folder, or malicious software tampered with your files.
3. You may also delete the old, problematic backup **if you made sure you do really have a secure backup** that actually works.