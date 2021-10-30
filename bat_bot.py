#!/usr/bin/python3
import requests
from time import sleep
import os

#-----------------
BAT_FILE = './bat_val'
COLOR_RED = 16711680
COLOR_YELLOW = 16776960
COLOR_GREEN = 6750054
#-----------------

def get_bat():
    #return float("0.55")
    return float(requests.get("http://eur.rate.sx/1bat").text[:-1])


def post_webhook(title, color, content=""):
    webhook = os.environ["BAT_WEBHOOK_URL"]

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
        print(err)
    else:
        print("Webhook delivered successfully, code {}.".format(result.status_code))


def get_previous():
    """
    returns -1 if it fails to read BAT_FILE
    """
    try:
        with open(BAT_FILE, 'r') as f:
            val_str = f.read()
            val = float(val_str)
            return val
    except:
        return -1


def save_previous(bat_val):
    """
    throws if opening BAT_FILE for writing fails
    """
    with open(BAT_FILE, 'w') as f:
        f.write(str(bat_val))


def main():
    msg, color, content = "", COLOR_YELLOW, ""
    try:
        previous_val = get_previous()
        bat_val = round(get_bat(), 2)

        if previous_val == -1:
            previous_val = bat_val
            color = COLOR_YELLOW

        delta = abs(bat_val - previous_val)
        if delta / previous_val > previous_val / 100:
            if bat_val > previous_val:
                color = COLOR_GREEN
                content = ""
            elif bat_val == previous_val:
                color = COLOR_YELLOW
                content = ""
            else:
                color = COLOR_RED
                content = ""
            msg = f"BAT {bat_val}€"
            #post_webhook(msg, color, content)
            save_previous(bat_val)

    except ValueError as e:
        print(f"Exception! {e}")
        msg = f"Server sent an invalid value. Sleeping 15 minutes."
        content = str(e)
        print(content)
        color = COLOR_RED

    except Exception as e:
        print("Exception!")
        print(e)
        msg = f"Connection failed to https://eur.rate.sx/1bat. \nSleeping 15 minutes."
        color = COLOR_RED
        content = str(e)
        print(content)

    finally:
        post_webhook(msg, color, content)


if __name__ == '__main__':
    main()
