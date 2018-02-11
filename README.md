# Riminder Test

## Usage:

### Requirments

In order to get full functionaities out of this repository, you will need to have the next stack instaled on your machine:

**Front-End**

- NodeJS
- NPM
- Bower


**Back-End**

- Python
- virtualenv (_to avoid package collisions in your global packages with the project's ones_)


### How to proceed

First, install the stack bellow and clone this repository to your machine. 

Then you can start by installing `virtualenv` to your machine using ````pip```` with the following command: 

```batch
pip install virtualenv
```

After finishing the ``virtualenv`` installation, using your command line to land in the repository folder then into the `reminder-text-flask-backend` folder, and execute the ``virtualenv ./`` command in to it, this will create an isolated python envirenment for you inside the folder and away from your global packages. After that, `cd` into `Scripts` and run the `activate` (`activate.bat` for Windows CMD or `activate.ps1` for PowerShell) batch script to activate the isolated python envirenment.

Then you can proceed to installing the Back-end dependencies using ```pip``` in `reminder-text-flask-backend` folder, as follows:

```batch
pip install -r requirements.txt
```

```pip``` will handle every thing for you from choosing the appropriate packages and their versions to installing them and making executables for `pip` and `python`.

In order to run the application API (Back-end), you will have to run the following commands:

```batch
export FLASK_APP=server.py
```

then

```batch
flask run --port=3010
```

The first command will tell Flask the app executable script, and the second will actually run the app (On Windows you will ahve to use `set` instead of `export`)

In the second command, you can see that we provided the `--port=3010` argument, you can ignore that part if for any reason that port was not available, but you will ahve to change the URLs pointing the that port to the one you app give you (Usually it's 5000)

If no errors were displayed on the console, you're set to go after the Front-End part.

In the Front-End part, you will ahve to install NPM modules and also BOWER modules, and this can be achived by `cd` into `riminder-test-chrome-extension` and runinng the following commands:

```batch
npm install
```

and

```batch
bower install
```

Make sure you execute: `npm install` and other time under `riminder-test-chrome-extension\bin` as one of the modules used by the extenstion as not available in BOWER so I had to get it from NPM as a separate one, this is a major package that the extension will not be able to run without.

After that all modules had been install, now you can build your front-end app using `GulpJS`, in order to that, `cd` to `riminder-test-chrome-extension` and run:

```batch
gulp
```

This will build and watch all files changes for us.

To run our extension, open you Google Chrome browser and go to `chrome://extensions`, you will see a list of your installed extensions, and on top of them you will find a button labled as : **Load unpacked extension** that will ahve to click on, and choose the `bin` folder under `riminder-test-chrome-extension` as the folder of our extension and click on **OK**

An icon will be added next to Chrome's OmniBox for uour extenstion titled as Book't click on that icon and enjoy your extension