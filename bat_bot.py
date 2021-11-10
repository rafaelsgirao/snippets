#!/usr/bin/env python3
import sys
import requests
import os

#Constants
BAT_FILE = './bat_val'
COLOR_RED = 16711680
COLOR_YELLOW = 16776960
COLOR_GREEN = 6750054

def get_bat_coinbase():
    r = requests.get("https://api.coinbase.com/v2/prices/BAT-EUR/spot")
    r.raise_for_status()
    bat_value = float(r.json()["data"]["amount"])
    return round(bat_value, 3)

def get_bat_value():
    bat_value = False
    endpoints = [get_bat_coinbase]
    for endpoint in endpoints:
        try:
            bat_value = endpoint()
            break
        except HTTPError as e:
            #Move on to next endpoint
            continue
    if bat_value == False or bat_value:
        raise ValueError
    return bat_value

print(get_bat_value())
