[![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](https://www.python.org/)
[![made-with-selenium](https://img.shields.io/badge/Made%20with-Selenium-brightgreen)](https://selenium-python.readthedocs.io)
[![made-with-pysimplegui](https://img.shields.io/badge/Made%20with-PySimpleGUI-red)](https://pysimplegui.readthedocs.io/en/latest/)
[![creative-commons](https://img.shields.io/badge/License-creativecommons-yellow)](https://creativecommons.org/share-your-work/public-domain/cc0/)

# WeTransfer Checker
> A program that automates uploading a file to WeTransfer and restarts if the upload has failed.
>Designed with slow internet, large files, and COVID-19 lockdown stress in mind.

![Arrests Map](.img/wetransferchecker.png)

## Table of contents
* [Usage](#usage)
* [Technologies](#technologies)
* [Features](#features)
* [Contact](#contact)

## Usage
If you're on a mac, you can download a zip file [here](.zip/wetransferchecker.zip). Simply unzip it,
copy the cloud icon to your applications folder and then double click it to run the program.

Otherwise, you'll need to make sure python3.8 is installed on your machine before running the following commands in 
the same directory:

```
git clone https://github.com/osintalex/wetransferchecker.git
python3 -m venv env
source env/bin/activate
pip install -r requirements.txt
cd app
python wetransferchecker.py
```

## Technologies
* Python 3.8
* Selenium 
* Pytest 
* Tenacity
* PySimpleGUI

## Features
* Browser automation
* Very straightforward GUI to run the script
* Regularly checks upload status 
* If your upload fails, closes the browser and restarts it
* Automatically saves your download link into a simple .txt file

## Contact
Created by Alex Darby - feel free to contact me on os1ntal3x@gmail.com !
