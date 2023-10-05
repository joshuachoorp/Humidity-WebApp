import sys
import subprocess
import pkg_resources
from pkg_resources import DistributionNotFound, VersionConflict



# Check if all packages in requirements.txt is installed
def checkReq():
    requireFile = open('requirements.txt',mode='r')
    requireList = requireFile.readlines()
    requireFile.close()
    for i in requireList:
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', i])