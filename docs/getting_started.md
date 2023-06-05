# Getting started with Lorean
In this little article you are going to learn about how to install Lorean on your system to create, manage and restore backups of your data. Please check the following minimum requirements to ensure your PC is able to run Lorean.

## Requirements
- minimum Python 3.7, **tested and recommended is Python 3.9.13 and above!**
- more than 50MB free disk space, **recommended is at least 100MB!**
- 50MB free RAM, **recommended is 100MB to 200MB RAM left for Lorean**

*Note that these requirements are partially way higher than the actual resource usage of Lorean; the extra margin is simply there to allow the app to expand in the future with more needed libraries, features etc. without causing any problems. Actual resource usage is, as stated, way lower.*

## Installation

**For Windows users only:** There are compiled .EXE files ready for you to be ran on your machine. Visit the
[Release page](https://github.com/mags0ft/Lorean/releases) on GitHub, click on "Assets" under the latest release and
download the .EXE. Put it in a separate folder on your machine which is empty (so Lorean can save it's settings and
config files somewhere) and run the file "Lorean.exe".

**For Mac/Unix users:** Native binary support may come in the future. For now, follow the instructions below.

1. Download the Lorean zip file and extract it, or simply clone the repo from GitHub:
`git clone https://github.com/mags0ft/Lorean.git`

2. Next, `cd` into the newly created directory: `cd ./Lorean`

3. Create a virtual environment: `python3 -m venv .venv`

4. Activate the virtual environment. This process may vary depending on your OS:
    - Windows: `./.venv/Scripts/Activate.ps1`
    - Unix/Linux: `source ./.venv/bin/activate`

5. Install all dependencies: `python3 -m pip install -r requirements.txt`

6. Run Lorean for the first time: `python3 -m flask -A "__init__.py" run`

## Done!
Lorean has now been successfully installed; any further steps for installation are performed by the software automatically. For the future, it's enough to run two commands:

1. activate the environment as stated above
2. `python3 -m flask run`

Lorean can be used inside your web browser of choice by opening the following address in the address bar:

`http://localhost:5000/`

That's it! If you encounter any problems during installation, don't ever hesitate to ask on the GitHub page.