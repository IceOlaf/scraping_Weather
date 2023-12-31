from django.shortcuts import render
from .models import WeatherQuery
from bs4 import BeautifulSoup
import requests

# Create your views here.
def home(request):
    return render(request, 'home.html')

def search(request):
    location = request.POST.get('location')
    
    
    query = WeatherQuery(location = location) #Saving the search history
    query.save()
    
    try:
        """
        First searching for the desired location and getting the required page's link.
        """

        primary_search_url  = 'https://www.timeanddate.com/weather/?query='+location.replace(" ",'+')
        
        response1 = requests.get(primary_search_url)

        primary_soup = BeautifulSoup(response1.text, features='html.parser')

        query_results = primary_soup.find('div',{'class':'tb-scroll'})
        
        link = query_results.find('a').get('href')
        
        location_name = query_results.find('a').text
        # print(location_name)

        secondary_search_url = 'https://www.timeanddate.com/'+link
        response2 = requests.get(secondary_search_url)
        
        secondary_soup = BeautifulSoup(response2.text, features='html.parser')
        
        
        temp_section = secondary_soup.find('div',{'id':'qlook', 'class':'bk-focus__qlook'})
        
        current_temp = temp_section.find(class_='h2').text

        current_condition = temp_section.find('p').text
        forecast = temp_section.find('span',{'title':'High and low forecasted temperature today'}).text
        img = temp_section.find('img',{'id':'cur-weather'}).get('src')
        
        #Getting all the relevant facts like visibilty, pressure, humidity...
        fact_section = secondary_soup.find('div',{'class':'bk-focus__info'}).findAll('tr')[3:]
   
        facts={
            'Visibility':fact_section[0].text,
            'Pressure':fact_section[1].text,
            'Humidity':fact_section[2].text,
            'DewPoint':fact_section[3].text,
        }
        
        # Temperature data for upcoming hours
        upcoming_hours_temp_list = secondary_soup.find('table',{'id':'wt-5hr','class':'fw sep tc'})
        time = [time.text for time in upcoming_hours_temp_list.find('tr',{'class':'h2'}).findAll('td')]
        images_upcoming_hours = [img.get('src') for img in upcoming_hours_temp_list.findAll('img')]
        temp_upcoming_hours = [temp.text for temp in upcoming_hours_temp_list.find('tr',{'class':'h2 soft'}).findAll('td')]

        #Getting a list for parsing the upcoming weather data for 5 hours onto the page
        weather_forecast = [[time[i],images_upcoming_hours[i], temp_upcoming_hours[i]] for i in range(6)]
        upcoming_hour_data = {
            'hour0':weather_forecast[0],
            'hour1':weather_forecast[1],
            'hour2':weather_forecast[2],
            'hour3':weather_forecast[3],
            'hour4':weather_forecast[4],
            'hour5':weather_forecast[5],
        }

        #The final dict that's passed to the page
        weather_dict={
            'location':location_name,
            'current_temp':current_temp,
            'current_condition':current_condition,
            'forecast':forecast,
            'condition_img':img,
            'fact_section':facts,
            'upcoming_hour_data':upcoming_hour_data,
        }    
        
        return render(request, 'weather_query.html', weather_dict)

    except Exception:
        return render(request, 'weather_query.html', {'error': True})