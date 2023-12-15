# Import the required libraries
import requests  # For making HTTP requests
from bs4 import BeautifulSoup  # For web scraping
import csv  # For working with CSV files
import os
import shutil

# Define the URL for the weather website
url = 'https://www.google.com/search?q=camp+eagle&rlz=1C1GCEB_enHK1084HK1084&oq=camp+eagle&gs_lcrp=EgZjaHJvbWUqDggAEEUYJxg7GIAEGIoFMg4IABBFGCcYOxiABBiKBTIICAEQRRgnGDsyBggCEEUYOzITCAMQLhiDARjHARixAxjRAxiABDIGCAQQRRg8MgYIBRBFGD0yBggGEEUYPDIGCAcQRRg80gEIMjk5NmowajeoAgCwAgA&sourceid=chrome&ie=UTF-8#lrd=0x8658d9dadce71323:0xb5d5d25c31c86c60,1,,,,'  # Replace with the actual URL for Ottawa's weather

# Make a GET request to the weather website
response = requests.get(url)


soup = BeautifulSoup(response.content, 'html.parser')

with oepn("review.html", w) as f:
    f.write(response.text)



temperature_element = soup.find('span', {'data-testid': 'TemperatureValue'})
humidity_element = soup.find('span', {'data-testid':'PercentageValue'})
wind_element = soup.find('span',{'data-testid':'Wind'})

if temperature_element and humidity_element and wind_element:
    temp = temperature_element.get_text()
    humidity = humidity_element.get_text()
    wind = wind_element.get_text()[14:]
    
    if os. path.isdir('weather'):
        shutil.rmtree('weather')
    os.makedirs('weather')
    with open('weather/ottawa_weather.csv', 'w', newline = '', encoding = 'utf-8') as file:
        writer = csv.writer(file)
        
        writer.writerow(['Temperature','Humidity','Wind'])
        writer.writerow([temp, humidity, wind])
    print("Weather data saved to ottwa_weather.csv")
    
else:
    print("Failed to find weather data on the website")


