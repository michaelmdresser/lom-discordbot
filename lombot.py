# python 3
import discord
import asyncio
import requests
import sys
import random
import re

client = discord.Client()
sub_blacklist = []
permalink_hashes = set()

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
    url = "https://www.reddit.com/r/" + subreddit + "/top/.json?t=&limit=20" + t
    h = {"User-Agent": "lombot v1"}

    response = requests.get(url, headers=h)
    response_children = response.json()["data"]["children"]

#    unused_children = [ child for child in response_children if child["data"]["permalink"] not in permalink_hashes ]
    unused_children = []
    for child in response_children:
        if "https://www.reddit.com" + child["data"]["permalink"] not in permalink_hashes:
            unused_children.append(child)
    post_count = len(unused_children)

    return unused_children, post_count

def random_from_subreddit(subreddit):
    for pattern in sub_blacklist:
        if re.search(pattern, subreddit) is not None:
            print("Subreddit {" + subreddit + "} matches blacklisted pattern {" + pattern + "}")
            return None, None, None, None

    print("trying top day")
    unused_children, post_count = subreddit_json_top(subreddit, t="day")

    if (post_count < 1):
        print("trying top week")
        unused_children, post_count = subreddit_json_top(subreddit, t="week")

    if (post_count < 1):
        print("trying top month")
        unused_children, post_count = subreddit_json_top(subreddit, t="month")

    if (post_count < 1):
        print("trying top year")
        unused_children, post_count = subreddit_json_top(subreddit, t="year")

    if (post_count < 1):
        print("trying top all")
        unused_children, post_count = subreddit_json_top(subreddit, t="all")

    if (post_count < 1):
        print("no posts on sub?")
        return None, None, None, None

#    post_position = random.randrange(0, post_count)
    post = unused_children[random.randrange(0, post_count)]

    response_url = post["data"]["url"]
    response_title = post["data"]["title"]
    response_permalink = "https://www.reddit.com" + post["data"]["permalink"]
    over_18 = post["data"]["over_18"]

    return response_url, response_title, response_permalink, over_18


@client.event
async def on_message(message):
    message.content = message.content.lower()

    prefix = "!"

    if message.author.bot:
        return

    if message.content.startswith("!redditblacklist") and message.author.roles:
        for role in message.author.roles:
            if role.name == "admin":
                add_to_blacklist(message.content[17:].strip())
                break
    elif re.search("should .+ do it", message.content) is not None:
        await client.send_message(message.channel, "do it")
    elif re.search("should .+ play.+", message.content) is not None:
        await client.send_message(message.channel, "play it")
    elif message.content.startswith("!reddit "):
        subreddit = message.content[8:]
        post_url, post_title, post_permalink, over_18 = random_from_subreddit(subreddit)
        if (post_url is None or post_title is None or post_permalink is None):
            await client.send_message(message.channel, "Blacklisted subreddit")
            return
        if over_18 and message.channel.name != "nsfw":
            await client.send_message(message.channel, "NSFW links not allowed outside of nsfw channel")
            return
        embed = discord.Embed(title=post_title, url=post_permalink)
        if "imgur.com" in post_url or "i.redd.it" in post_url or "v.redd.it" in post_url or "gfycat.com" in post_url or "giphy" in post_url:
            print("image/gif link detected")
            embed = embed.set_image(url=post_url)
        print("sending permalink: %s\n\npermalink_hashes is before add: %s\n\npermalink in hashes? %s\n\n" % (post_permalink, permalink_hashes, post_permalink in permalink_hashes))
        permalink_hashes.add(post_permalink)
        await client.send_message(message.channel, embed=embed)

if __name__ == "__main__":
    read_blacklist()
    print(sub_blacklist)
    client.run(sys.argv[1])
