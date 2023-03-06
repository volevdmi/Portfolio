from bs4 import BeautifulSoup
import requests


def check_link(link, network_name):
    if network_name.lower() not in link.lower():
        return 0
    try:
        response = requests.get(link)
        soup = BeautifulSoup(response.text, 'lxml')
        return 1
    except:
        return 0


def check_number(text):
    for symbol in text:
        if not symbol.isdigit():
            return 0
    return 1


def read_countries(text):
    text.replace(", ", " ")
    text.replace(",", " ")
    countries = text.split(" ")
    for item in countries:
        if len(item) < 3:
            countries.remove(item)
    return countries


def read_age_interval(text):
    text.replace(" ", "")
    for symbol in text:
        if not (symbol.isdigit() or symbol == '-'):
            return "0"
    return text
