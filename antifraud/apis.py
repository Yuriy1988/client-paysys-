import requests
import json


def get_country_code_by_bin(bin_code):
    # quota: 3000 request per day
    api_key = "8f4b318ed020e089a83f0a29f586a65d"
    url = "https://api.bincodes.com/bin-checker.php?api_key={key}&bin={bin}&format=json"
    try:
        card_info = json.loads(requests.get(url.format(key=api_key, bin=bin_code)).text)
    except json.decoder.JSONDecodeError as ex:
        return
    return card_info.get("countrycode")


def get_country_code_by_ip(ip):
    # quota: 10000 request per hour
    url = "http://freegeoip.net/json/{ip}"
    try:
        ip_info = json.loads(requests.get(url.format(ip=ip)).text)
    except json.decoder.JSONDecodeError as ex:
        return
    return ip_info.get("country_code")

