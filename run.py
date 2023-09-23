import sys
import subprocess
from testRequirements import checkReq




if __name__ == '__main__':
    while True:
        #Checks for required packages and installs them if not found
        try:
            from app import app
            app.run(debug=True)

        except Exception as e:
            checkReq()            
            continue
        
        break

    

        