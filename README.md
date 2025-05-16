![Lorean logo](https://raw.githubusercontent.com/mags0ft/Lorean/master/app/static/images/logo.png)

# 🚗 Lorean

Lorean is a simple and user-friendly backup management tool written in Python using Flask.
You can easily create, manage and restore backups which are still human readable and can be
easily modified. Technically, you could also call it "over-engineered file copying app".

**WARNING**! This is by no means a well-tested and bulletproof backup system. Always make
sure to follow the 3-2-1 backup rule, do not put full trust into this program if the data
being backed up is critical and make sure your recovery strategy works.

See `LICENSE`. This software comes with ABSOLUTELY NO WARRANTY.

## 🔥 Features

Lorean has some advantages compared to just copying and pasting your folders, such as:

### 🚫 Regex-powered excludes
Specify paths that are unnecessary to back up (for example, `node_modules` or similar) which
Lorean will skip over to save tons of time and storage. This can be achieved using regular
expressions, offering you a huge variety of filtering mechanisms at your fingertips.

### 🔎 Backup scanning
You can monitor the validity of your backups using the Lorean backup manager; it will warn you
about suspicious anomalies and problems regarding your saved files, so you won't easily make
things worse when recovering from a backup.

### 📕 Detailed logging
Lorean creates verbose and user-customizable logs that explain what was going on in each backup
process, which files have been skipped and what might've gone wrong, so you can lean back and let your
backup run in the background, close your browser or whatever you like to do - later, you will
find everything noted down in the logs.

### 🥳 Keeps your backups organized
Create a folder on your removable drive, add it in the Lorean settings and the rest doesn't have
to be your business - Lorean manages everything regarding your file structure under the hood, but
if you need it, each backup is still human-readable and can be easily used to copy and paste files
from without performing a full recovery.

### ✨ Beautiful UI
It isn't a hassle to work with Lorean, it's actually super simple; you start the app, visit the
web interface in your browser and enjoy the user-friendly interface.
