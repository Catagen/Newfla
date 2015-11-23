# Newfla
Simple python script for quickly creating a Flask project structure set up with a virtual environment containing Redis, Bootstrap, Moment and the packagages of your choice.

###Requirements to run the script
* Python 3.X
* Python Click
* Windows (has not been tested on other platforms but has potential to work cross-platform)

###Requirements to run the app
* Python 3.X

###Instructions
To run the script simply run the following command, the script will then set up a virtual environment and prompt you for further actions
```
python newfla.py --name=YourAppName
```
_Note that leaving the name blank will set your projects name to 'FlaskApp'._
_You can edit the packages installed by default by manipulating the packages file, altho I would recommend leaving the default packages in place._
####Future pushes will contain
* Cross platform tested and debugged version
