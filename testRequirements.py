import sys
import subprocess
import pkg_resources
from pkg_resources import DistributionNotFound, VersionConflict



# Check if all packages in requirements.txt is installed
def checkReq():
    try:
        from Functions import dataPlot, linear_regression, correlation, overview_data, predictionHumidity
        from distutils.command import upload
        from flask import Flask, render_template, request, redirect, flash, send_file, send_from_directory, current_app, abort
        import flask
        import pandas as pd
        import numpy as np


    except ModuleNotFoundError as e:
        print(e)
        requireFile = open('requirements.txt',mode='r')
        requireList = requireFile.readlines()
        requireFile.close()
        for i in requireList:
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', i])

    except Exception as e:
        print(e)
