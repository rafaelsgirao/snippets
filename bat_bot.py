#!/usr/bin/python3
import requests
from time import sleep
import os

BAT_FILE = './bat_val'

def get_bat():
    #return float("0.55")
    return float(requests.get("http://eur.rate.sx/1bat").text[:-1])


def post_webhook(title, color, content=""):
    webhook = os.environ["BAT_WEBHOOK_URL"]

    data = {
        "username" : "Stonks",
        "avatar_url" : "https://cdn.discordapp.com/emojis/833432167756464184.png?v=1",
        "content": content,
        "embeds": [
        {
          "title": title,
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
        print("Payload delivered successfully, code {}.".format(result.status_code))


previous_val = ""
color_green = 6750054
color_red = 16711680
color_yellow = 16776960

lyrics = ["I know, I know I've let you down",
        "I've been a fool to myself.",
        "I thought that I could live for no one else",
        "But now, through all the hurt and pain",
        "It's time for me to respect",
        "The ones you hodl mean more than anything.",
        "So with sadness in my heart",
        "I feel the best thing I could do",
        "Is sell it all, and leave forever",
        "What's bought is bought, it feels so bad",
        "What once was happy now is sad",
        "I'll never love again.",
        "My world is ending.",
        "I wish that I could turn back time",
        "'Cause now the guilt is all mine.",
        "Can't live without the trust from those you love",
        "I know we can't forget the past",
        "You can't forget love and pride",
        "Because of that it's killing me inside",
        "_It all returns to nothing_",
        "It all comes tumbling down, tumbling down, tumbling down...",
        "_It all returns to nothing_",
        "I just keep letting me down, letting me down, letting me down...",
        "In my heart of hearts, I know I can never love BAT again.",
        "Everything that matters to me matters in this world.",
        "_It all returns to nothing_",
        "It just keeps tumbling down, tumbling down, tumbling down...",
        "_It all returns to nothing_",
        "I just keep letting me down, letting me down, letting me down..."]
lyrics_iter = 9


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
    previous_val = get_previous()

    try:
        bat_val = round(get_bat(), 2)

        if previous_val == -1:
            previous_val = bat_val
            color = color_yellow


        delta = abs(bat_val - previous_val)
        if delta / previous_val > previous_val / 100:

            if bat_val > previous_val:
                color = color_green
                #content = "<:stonks:833381927255539743>"
                content = ""
            elif bat_val == previous_val:
                color = color_yellow
                content = ""
            else:
                color = color_red
                #content = lyrics[lyrics_iter]
                content = ""
                if lyrics_iter == len(lyrics) - 1:
                    lyrics_iter = 0
                else:
                    lyrics_iter += 1

            msg = f"BAT {bat_val}€"
            post_webhook(msg, color, content)
            save_previous(bat_val)
            init = True

    except Exception as e:
        print("Exception!")
        print(e)
        post_webhook("Connection failed to https://eur.rate.sx/1bat. \nSleeping 15 minutes.", color_red, content="")


if __name__ == '__main__':
    main()
