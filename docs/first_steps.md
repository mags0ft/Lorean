# First steps with Lorean

There are a few things to do if you want to get started with Lorean as smooth as possible; in this brief documentation article, we're going to look at what to set up and what's important to note when using the software.

## Recommendations

There are a lot of general precautions to note when doing backups.
- First of all, you should **always** store your backups on a removable, external drive to ensure they are completely isolated from your computer and/or the internet.
- It is also **highly** recommended to create several independent drives, each containing all your backups, so you won't regret it if one drive fails.
- On each drive, there should be separate folders for each device you want to make backups of.
- It's important to keep backups secure and make sure they still work, so you should always practically test if all your backups work, for example using the [Lorean backup manager](./manage.md).
- You achieve the best security results if you create backups regularly.

## Drive setup

You can use any type of drive/storage to store your backups, from USB-Stick to external hard drive. **It's discouraged to use HDDs.**
The best solution would be to create a new folder at the root of your drive, and directories for each device you use to create backups of
using the removable drive.

Make sure your backups work for your file system - if your drive runs FAT32, you may not be able to store files individually bigger than 4 GB, so you might want to format your drive, even though such big files are uncommon.

You may then add the locations of these folders to the Lorean settings, so it's more convenient to create backups - more information about this below (*In-app configuration*).

```
drive root
|_ Backups
   |_ Computer
   |_ Laptop
```

Note that a Lorean backup is just another directory created inside the Backup folder, so it would look like this:

```
drive root
|_ Backups
   |_ Computer
      |_ 2023-05-31 15-00 (generated by Lorean)
      |...
```

## In-app configuration

You can change general settings regarding your backups inside Lorean itself - just run the app and click on "Settings" in the navigation bar.

- **Excludes** are a crucial part of Lorean; they can be used to skip over files that match **any** of the specified patterns.
The patterns are written in regular expressions (regex), and the relative part of the file in folder getting backed up is tested
against them.
- Saving **backup locations** is just a convenience/quality-of-life feature that remembers the **abosolute** paths of directories
containing your backups, so you don't have to type them out every single time.

## config.py file configuration

You can customize the general configuration of Lorean using the file `app/config.py`, in which you can set values to match your expectations. Lorean will use them to work properly, so you should only **change** them, never **delete** any.

These values are:
- `ENVFILE`: file to store environment variables in.
- `LOGDIR`: directory to put logs in.
- `LOG_SKIPS`: whether to log if a file is skipped.
- `LOG_COPY`: whether to log if a file is copied.

**Warning!** Setting `LOG_SKIPS` and/or `LOG_COPY` to `True` may consume a lot of storage,
as Lorean will log way more than you might think. Log files will likely get several megabytes
big, plus it can slow down the backup process a lot.