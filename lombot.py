# python 3
import discord
import asyncio
import requests
import sys
import random
import re

client = discord.Client()
sub_blacklist = []

def read_blacklist():
    f = open("blacklist.txt", "r")
    for line in f:
        sub_blacklist.append(line.strip())

def subreddit_json_top(subreddit, t="day"):
    url = "https://www.reddit.com/r/" + subreddit + "/top/.json?t=" + t
    h = {"User-Agent": "lombot v1"}

    response = requests.get(url, headers=h)
    post_count = len(response.json()["data"]["children"])

    return response.json(), post_count

def random_from_subreddit(subreddit):
    for pattern in sub_blacklist:
        if re.search(pattern, subreddit) is not None:
            print("Subreddit {" + subreddit + "} matches blacklisted pattern {" + pattern + "}")
            return "Blacklisted pattern"
    if subreddit in sub_blacklist:
        print("Subreddit {" + subreddit + "} denied, on blacklist")
        return "Blacklisted subreddit"

    rjson, post_count = subreddit_json_top(subreddit)

    if (post_count < 5):
        rjson, post_count = subreddit_json_top(subreddit, t="week")

    if (post_count < 5):
        rjson, post_count = subreddit_json_top(subreddit, t="month")

    if (post_count < 5):
        rjson, post_count = subreddit_json_top(subreddit, t="year")

    if (post_count < 5):
        rjson, post_count = subreddit_json_top(subreddit, t="all")

    post_position = random.randrange(0, post_count)

    response_url = rjson["data"]["children"][post_position]["data"]["url"]

    return response_url

@client.event
async def on_message(message):
    message.content = message.content.lower()

    prefix = "!"

    if "kys" in message.content:
        await client.send_message(message.channel, "Please don't actually")
    elif re.search("should .+ do it", message.content) is not None:
        await client.send_message(message.channel, "do it")
    elif re.search("should .+ play.+", message.content) is not None:
        await client.send_message(message.channel, "play it")
    elif message.content.startswith("!reddit "):
        subreddit = message.content[8:]
        await client.send_message(message.channel, random_from_subreddit(subreddit))
    elif message.content == "anime_irl":
        subreddit = "anime_irl"
        await client.send_message(message.channel, random_from_subreddit(subreddit))

if __name__ == "__main__":
    read_blacklist()
    print(sub_blacklist)
    client.run(sys.argv[1])
