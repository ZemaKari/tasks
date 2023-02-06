from conf import weather_token
import requests
import datetime
import time

from pprint import pprint


def get_wether(city, weather_token):
    '''функция возвращает город, текущую дату,разницу между ощущаемой температурой и ночной,
    продолжительность светового дня.

    :param city: город
    :param weather_token: токен с сайта погоды
    :type city: str
    :type weather_token:
    :except Exception: Если не правильно указать город, или токен получаем ошибку.
    '''

    try:
        req = requests.get(
            f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={weather_token}&unit=metsric"

        )
        date = req.json()
        # pprint(date)
        city = date['name']
        curr_date = datetime.datetime.fromtimestamp(date['dt'])
        current_temp_night = date['main']['temp_min']
        feels_like = date['main']['feels_like']
        sunrice = date['sys']['sunrise']
        sunset = date['sys']['sunset']
        diff_sunrice_sunset = datetime.datetime.fromtimestamp(sunset) - datetime.datetime.fromtimestamp(sunrice)
        min_temp_difference = round(feels_like - current_temp_night, 2)

        print(f"Погода в городе {city}\nТекущая дата и время: {curr_date}\n"
              f"Разница между ощущаемой и ночной температурой: {min_temp_difference} С°")
        return city, curr_date, min_temp_difference, diff_sunrice_sunset
    except Exception as ex:
        print(f"{ex} Город не найден.")


def get_sunrice(day, weather_token):
    '''функция возвращает текущую дату и продолжительность светового дня

    :param day: время в секундах
    :param weather_token: токен с сайта погоды
    :type day: str
    :type weather_token: str
    :except Exception: Если неправильно ввести параметр day или токен получаем ощибку'''

    try:
        req = requests.get(
            f"https://api.openweathermap.org/data/2.5/onecall/timemachine?lat=54.775&lon=56.0375&dt={day}"
            f"&appid={weather_token}&unit=metsric"
        )
        date = req.json()   
        # pprint(date)
        sunrise = date['current']['sunrise']
        sunset = date['current']['sunset']
        diff_sunrise_sunset = datetime.datetime.fromtimestamp(sunset) - datetime.datetime.fromtimestamp(sunrise)
        curr_datetime = datetime.datetime.fromtimestamp(date['current']['dt'])
        # print(f'Дата: {curr_datetime}\nПродолжительность светового дня: {diff_sunrise_sunset}')
        return curr_datetime, diff_sunrise_sunset
    except Exception as ex:
        print(ex)


past_day_list = []
dt_ = int(time.time())
for i in range(5):
    past_day_list.append(dt_)
    dt_ -= 86400
past_day_list.reverse()
print(past_day_list)

city = "ufa"
print('-' * 40)
get_wether(city, weather_token)
print('-' * 40)

day_length_list = []
for day in past_day_list:
    a = get_sunrice(str(day), weather_token)
    day_length_list.append(a)
max_day_length = max(day_length_list)
print(f'За послдние 5 дней максимальная продолжительность дня была {max_day_length[0].strftime("%Y-%m-%d")} '
      f'числа\nи сoставила {max_day_length[1]}.')
print('-' * 40)
