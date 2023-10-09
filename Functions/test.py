from io import BytesIO
import base64
from predictionV2 import linear_regression, correlation, overview_data, predictionHumidity






#linear_regression().show()
#correlation().show()
overview_data().show()
#predictionHumidity().show()

def convertGraphToB64(plot):
    img = BytesIO()
    plot.savefig(img, format='png')
    img.seek(0)
    #plotB64 = base64.b64encode(img.getvalue()).decode('utf8')
    return base64.b64encode(img.getvalue()).decode('utf8')



print(convertGraphToB64(overview_data()))

