Here is my project to manage the database from the HR of my firm.
The application can be run with python in a little application developed by myself with tkinter.
Or in flask with html/css.


## Step 1 : 
Install git
    - Go to https://gitforwindows.org/
    - Download the exe
    - Open the exe click on next until the loading and then wait until the last screen where you will click on finish.

## Step 2 :
Open a terminal
navigate with the cd command where you want to clone the repo (by default it's the user directory)
Type git clone https://github.com/Gaspard2005/Cardpressodb


## Step 3 :
Install a sql manager (Laragon)
    - Go to https://laragon.org/download/
    - Download the full version
    - Open the exe downloaded
    - Set the language the click on next, next, install and wait until the loading is completed then click on finish
    -

## Step 4 : 
Import the dump in your sql manager
    - Open Laragon
    - Click on start all
    - Accept all the pop up
    - Then click on database
    - Don't touch anything and click Open
    - Click on file on the top left, then click on execute a sql file
    - Locate the dump you want to load and open it
    - If a pop-up appears click yes
    - Then reload the laragon by clicking on the whole directory and the click on f5 (or fn + f5)

## Step 5 :
Install Pycharm
    - Go to https://www.jetbrains.com/pycharm/download/?section=windows
    - Download the community edition exe
    - Open the exe then next, next, next, install, waiting for the loading to complete and then click finish
    - Open Pycharm accept the policy
    - Then click on open search the repo you cloned previously and select it.

## Step 6 :
Run the flask app
    - Open the project on pycharm and open the flask_app directory
    - then open flaskapp.py, warning will appears at the top of the window
    - Click on the create a new environement using requirements.txt, use python 3.12
    - Then run the flask app
    - You can now access the app here http://127.0.0.1:5000
    - The default username is root, there is no password and the database is cardpresso_db
    - (Optional) you can run a version directly in python that will open a python app --> run cardpresso.py in the main directory
