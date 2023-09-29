import sys
import subprocess
from testRequirements import checkReq




if __name__ == '__main__':
    while True:
        #Checks for required packages and installs them if not found
        try:
            from app import app
            app.run(debug=True)

        #Checks for required packages and installs them if not found
        #If module required not installed, will throw exception. 
        #If thrown exception, will install modules required based on requirements.txt
        except ModuleNotFoundError:
            checkReq()         
            continue

        except Exception as e:
            checkReq()            
            continue
        
        break

    

        