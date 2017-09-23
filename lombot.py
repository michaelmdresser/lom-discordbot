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
    f.close()

def add_to_blacklist(pattern):
    sub_blacklist.append(pattern)
    f = open("blacklist.txt", "a")
    f.write(pattern + "\n")
    f.close()

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
    response_title = rjson["data"]["children"][post_position]["data"]["title"]
    response_permalink = "https://www.reddit.com" + rjson["data"]["children"][post_position]["data"]["permalink"]

    return response_url, response_title, response_permalink

@client.event
async def on_message(message):
    message.content = message.content.lower()

    prefix = "!"
    kys_pattern = "k\s?y\s?s"
    kms_pattern = "k\s?m\s?s"

    if message.content.startswith("!redditblacklist") and message.author.roles:
        for role in message.author.roles:
            if role.name == "admin":
                add_to_blacklist(message.content[17:].strip())
                break
    elif re.search(kys_pattern, message.content) is not None or "kill yourself" in message.content:
        await client.send_message(message.channel, "Please don't actually")
    elif re.search(kms_pattern, message.content) is not None or "kill myself" in message.content:
        await client.send_message(message.channel, "Please don't actually")
    elif re.search("should .+ do it", message.content) is not None:
        await client.send_message(message.channel, "do it")
    elif re.search("should .+ play.+", message.content) is not None:
        await client.send_message(message.channel, "play it")
    elif message.content.startswith("!reddit "):
        subreddit = message.content[8:]
        post_url, post_title, post_permalink = random_from_subreddit(subreddit)
        embed=discord.Embed(title=post_title, url=post_permalink)
        await client.send_message(message.channel, embed=embed)
        await client.send_message(message.channel, post_url)

if __name__ == "__main__":
    read_blacklist()
    print(sub_blacklist)
    client.run(sys.argv[1])
