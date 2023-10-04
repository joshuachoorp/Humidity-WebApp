import requests
from bs4 import BeautifulSoup
import csv, os.path

# Define the URL and headers 
url = "http://www.weather.gov.sg/wp-content/themes/wiptheme/page-functions/functions-climate-historical-daily-records.php"
headers = {
    "Accept": "text/plain, */*; q=0.01",
    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
    "Referer": "http://www.weather.gov.sg/climate-historical-daily",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36",
}

dwPath = "../Datasets" #Define download path
header = ["Date","Mean Temperature (°C)", "Maximum Temperature (°C)", "Maximum Temperature (°C)","Mean Wind Speed (km/h)", "Max Wind Speed (km/h)"]
cityName = ['Changi', 'Ang Mo Kio', 'Sembawang','Admiralty', 'Tengah', 'Jurong (West)', 'Tuas South', 'Sentosa Island', 'Newton', 'East Coast Parkway']
mth = ['July','June','August' ]
year = 2023
# Define the request data in a loop
for city_name in cityName:
    data_2d_array = []
    for month in mth:
        data = {
            "cityname": city_name,
            "month": month,
            "year": year,
            "redirectUrl": "http://www.weather.gov.sg/weather-world-forecast",
        }

        # Make the POST request
        response = requests.post(url, headers=headers, data=data)

        # Ensure that request was successful
        if response.status_code == 200:
            print(f"Request successful for {city_name} at {month}")

            # Parse the HTML content 
            soup = BeautifulSoup(response.text, 'html.parser')

            table = soup.find('table', {'class': 'table table-calendar'})

            # Check for table 
            if table:
                for row in table.find_all('tr'):
                    cells = row.find_all('td')
                    if cells:  
                        scrapData = [cells[0].text.strip()] + [cell.text.strip() for cell in cells[5:]]
                        data_2d_array.append(scrapData)
                
            else:
                print("Table with the specified class not found.")

        else:
            print(f"Request failed with status code {response.status_code}")

    csvFileName = f"{city_name}_data.csv"
    csvFilePath = os.path.join(dwPath, csvFileName)
    with open(csvFilePath, mode="w", newline="") as file:
        writer = csv.writer(file, delimiter=",", quotechar='"', quoting=csv.QUOTE_MINIMAL)   
        writer.writerow(header)
        for row in data_2d_array:
            #print(row) 
            writer.writerow(row)

                