import requests
import math
APPID = "320b5ed7aee20b24e7e3f5c5a7bb919a"
URL_BASE = "http://api.openweathermap.org/data/2.5/"


def current_weather(q: str = "Chicago", appid: str = APPID) -> dict:
    """https://openweathermap.org/api"""
    return math.ceil(int(requests.get(URL_BASE + "weather", params=locals()).json()['main']['temp']) - 273.15)
