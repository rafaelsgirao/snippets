#!/usr/bin/env python3
import sys
import requests
import os
import logging
#import json
from urllib.error import HTTPError
import time

#Constants
COLOR_RED = 16711680
COLOR_YELLOW = 16776960
COLOR_GREEN = 6750054
STORE_FILE = "coin_val-{}.txt"
SENSITIVITY = 2
TIME_BOUND = 3600*6
CHANGE_BOUND = 10/100

COINBOT_WEBHOOK_URL = os.getenv("COINBOT_WEBHOOK_URL")

logging.basicConfig(
        filename='coin_bot.log',
        encoding='utf-8',
        format='%(asctime)s.%(msecs)03d %(levelname)s %(module)s - %(funcName)s: %(message)s',
        datefmt='[%d-%m-%Y %H:%M:%S]',
        level=logging.DEBUG
        )


class CoinValue:
    valid_coins = ["BAT", "ETH", "BTC"]
    coin = ""
    previous_value = False
    value = False

    def __init__(self, coin):
        previous_value = False    
        if coin not in self.valid_coins:
            logging.warn(f"Attempted to init CoinValue with an unknown coin '{coin}'")
            raise ValueError
        self.coin = coin
        self.target_file = STORE_FILE.format(self.coin)
        logging.debug(f"CoinValue instanced, coin='{self.coin}', target_file='{self.target_file}'")

    def get_previous(self):
        return self.previous_value
    
    def update_previous(self):
        logging.debug(f"Updating previous value, current = {self.value}, previous was {self.previous_value}")
        self.previous_value = self.value

    def get_target_file(self):
        return self.target_file

    def get_value(self):
        def get_value_coinbase():
            r = requests.get(f"https://api.coinbase.com/v2/prices/{self.coin}-EUR/spot")
            r.raise_for_status()
            coin_value = float(r.json()["data"]["amount"])
            logging.debug(f"Sucessfully got {self.coin} value from Coinbase, raw val={coin_value}, code {r.status_code}")
            return round(coin_value, SENSITIVITY)
    
        def get_value_rate_sx():
            coin_adapted = self.coin.lower()
            r = requests.get(f"https://eur.rate.sx/1{coin_adapted}")
            coin_value = float(r.text)
            logging.debug(f"Sucessfully got {self.coin}/{coin_adapted} value from rate.sx, raw val={coin_value}, code {r.status_code}")
            return round(coin_value, SENSITIVITY)

        endpoints = [get_value_coinbase, get_value_rate_sx]
        for endpoint in endpoints:
            try:
                coin_value = endpoint()
                break
            except HTTPError as e:
                logging.info(f"Couldn't get coin value at endpoint {endpoint.__name__}. Reason: {str(e)}")
                #Move on to next endpoint
                continue
        if coin_value == False:
            logging.error(f"Couldn't get coin {self.coin} value with any known method.")
            raise ValueError
        self.value = coin_value
        return coin_value

    def dump_previous(self):
        if self.previous_value == False:
            logging.error("Attempted to dump an incorrect coin value")
            #raise ValueError
            return
        try:
            with open(self.target_file, "w") as f:
                f.write(str(self.previous_value))
            logging.debug(f"Dumped previous value to file; previous_value='{self.previous_value}'")
        except ValueError as e:
            logging.error(f"Failed to dump to file {self.target_file}. Reason: '{str(e)}'")
        
    def load_previous(self):
        try:
            with open(self.target_file, "r") as f:
                self.previous_value = float(f.read())
            logging.debug(f"Loaded previous value from file; previous_value='{self.previous_value}'")
        except ValueError as e:
            logging.error(f"Failed to load file '{self.target_file}'. Reason: {str(e)}")

def post_webhook(title, color, content=""):
    webhook = os.environ["COINBOT_WEBHOOK_URL"]

    data = {
        "username" : "Stonks",
        "avatar_url" : "https://cdn.discordapp.com/emojis/833432167756464184.png?v=1",
#        "content": content,
        "embeds": [
        {
          "title": title,
          "description": content,
          "color": color
        }
      ]
    }
    result = requests.post(webhook, json = data)
    try:
        result.raise_for_status()
    except requests.exceptions.HTTPError as err:
        logging.error(f"HTTPError while delivering Webhook. Reason: {str(err)}")
    else:
        logging.info("Webhook delivered successfully, code {}.".format(result.status_code))

def update_condition(time, change):
    return (time/TIME_BOUND)**2 + (change/CHANGE_BOUND)**2 >= 1
        
def main():
    logging.debug(f"Script started.")
    try:
        bat = CoinValue("BAT")
        bat_val = bat.get_value()
        try:
            bat.load_previous()
            previous_val = bat.get_previous()
        except IOError as e:
            logging.info("Error ocurred while loading previous val file, continuing.")
            filetime_condition = False
            previous_val = False

        logging.debug(f"Var debug: bat_val='{bat_val}', previous='{previous_val}'")

        if previous_val == False:
            logging.error("previous_val was False, overriding with new.")
            color = COLOR_YELLOW
            msg = f"BAT {bat_val}€"
            post_webhook(msg, color)
            bat.update_previous()
            bat.dump_previous()

        else:
            logging.debug("previous_val wasn't false, continuing")
            delta = abs(bat_val - previous_val)

            #Epoch
            target_file = bat.get_target_file()
            if not (os.path.isfile(target_file)):
                logging.info("Previous value file doesn't yet exist, ignoring on delta check")
                filetime_condition = False
            else: 
                logging.debug(f"target_file = {target_file}")

            file_modified_time = int(os.path.getmtime(target_file))
            current_time = int(time.time())

            if update_condition(current_time - file_modified_time, delta/previous_val):
                logging.debug("Deltas condition passed")
                if bat_val > previous_val:
                    color = COLOR_GREEN
                    #content = "<:stonks:833381927255539743>"
                elif bat_val == previous_val:
                    color = COLOR_YELLOW
                else:
                    color = COLOR_RED
    
                msg = f"BAT {bat_val}€"
                
                bat.update_previous()
                bat.dump_previous()
                post_webhook(msg, color)
            else:
                logging.debug(f"Delta condition failed. delta='{delta}', previous_val='{previous_val}', bat_val = '{bat_val}'")

    except Exception as e:
        logging.fatal(f"Houston, we have a problem.")
        logging.exception(e)
        post_webhook("Exception occurred while getting price.", COLOR_RED, content="Check logs for details")
        sys.exit(-1)


if __name__ == '__main__':
    main()
