from io import BytesIO
import base64
from predictionV3 import linear_regression, correlation, overview_data, predictionHumidity
import time





#linear_regression().show()
#correlation().show()
overview_data()
#predictionHumidity().show()

def convertGraphToB64(plot):
    img = BytesIO()
    plot.savefig(img, format='png')
    img.seek(0)
    #plotB64 = base64.b64encode(img.getvalue()).decode('utf8')
    return base64.b64encode(img.read()).decode('utf8')

#pic_IObytes = BytesIO()
#overview_data().savefig(pic_IObytes,  format='png')
#pic_IObytes.seek(0)
#pic_hash = base64.b64encode(pic_IObytes.getvalue()).decode('utf8')

#print(pic_hash)

