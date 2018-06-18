# python 3
import discord
import asyncio
import requests
import sys
import random
import re
import logging

client = discord.Client()
logger = logging.getLogger(__name__)
sub_blacklist = []
permalink_hashes = set()

def read_blacklist():
    f = open("blacklist.txt", "r")
    logger.info("opened blacklist.txt")
    for line in f:
        sub_blacklist.append(line.strip())
    f.close()
    logger.info("finished reading blacklist.txt")

def add_to_blacklist(pattern):
    sub_blacklist.append(pattern)
    f = open("blacklist.txt", "a")
    f.write(pattern + "\n")
    f.close()
    logger.info("added %s to blacklist" % pattern)

def subreddit_json_top(subreddit, t="day"):
    url = "https://www.reddit.com/r/" + subreddit + "/top/.json?limit=30&t=" + t
    h = {"User-Agent": "lombot v1"}

    response = requests.get(url, headers=h)
    response_children = response.json()["data"]["children"]

    unused_children = [ child for child in response_children if "https://www.reddit.com" + child["data"]["permalink"] not in permalink_hashes ]
    post_count = len(unused_children)

    return unused_children, post_count

def test_subreddit(subreddit):
    url_test = "https://www.reddit.com/r/" + subreddit + "/top/.json?t=all&limit=1"
    h = {"User-Agent": "lombot v1"}
    response = requests.get(url_test, headers=h)
    if len(response.json()["data"]["children"]) < 1:
        return False
    return True


def random_from_subreddit(subreddit):
    success = False
    blacklisted = False
    for pattern in sub_blacklist:
        if re.search(pattern, subreddit) is not None:
            logger.info("Subreddit {" + subreddit + "} matches blacklisted pattern {" + pattern + "}")
            blacklisted = True

    logger.info("testing subreddit success")
    test_success = test_subreddit(subreddit)
    logger.info("subreddit success = %s" % test_success)
    if not test_success or blacklisted:
        return None, None, None, None, None, success, blacklisted


    logger.info("trying top day")
    unused_children, post_count = subreddit_json_top(subreddit, t="day")

    if (post_count < 5):
        logger.info("trying top week")
        unused_children, post_count = subreddit_json_top(subreddit, t="week")

    if (post_count < 5):
        logger.info("trying top month")
        unused_children, post_count = subreddit_json_top(subreddit, t="month")

    if (post_count < 5):
        logger.info("trying top year")
        unused_children, post_count = subreddit_json_top(subreddit, t="year")

    if (post_count < 5):
        logger.info("trying top all")
        unused_children, post_count = subreddit_json_top(subreddit, t="all")

    if (post_count < 5):
        logger.info("no posts on sub?")
        return None, None, None, None, None, success, blacklisted

    success = True

    post = unused_children[random.randrange(0, post_count)]

    response_url = post["data"]["url"]
    response_title = post["data"]["title"]
    response_permalink = "https://www.reddit.com" + post["data"]["permalink"]
    response_selftext = post["data"]["selftext"]
    over_18 = post["data"]["over_18"]

    return response_url, response_title, response_permalink, response_selftext, over_18, success, blacklisted


@client.event
async def on_message(message):
    if message.author.bot:
        return

    if message.channel.name != "nsfw" and message.channel.name != "botspam":
        await client.send_message(message.channel, "Bot messages only allowed in \"nsfw\" and \"botspam\" channels")
        return

    logger.info("received message with content: %s" % message.content)
    message.content = message.content.lower()

    prefix = "!"

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
        post_url, post_title, post_permalink, post_selftext, over_18, success, blacklisted = random_from_subreddit(subreddit)
        if blacklisted:
            await client.send_message(message.channel, "Blacklisted subreddit")
            return
        if not success:
            return
        if over_18 and message.channel.name != "nsfw":
            await client.send_message(message.channel, "NSFW links not allowed outside of \"nsfw\" channel")
            return

        embed = discord.Embed(title=post_title, url=post_permalink, description=post_selftext)
        send_link = False

        if "youtu.be" in post_url or "youtube" in post_url:
            logger.info("youtube link detected")
            send_link = True
#            embed = discord.Embed(title=post_title, url=post_permalink, description=post_selftext, video=post_url)
        elif "imgur.com" in post_url or "i.redd.it" in post_url or "v.redd.it" in post_url or "gfycat.com" in post_url or "giphy" in post_url:
            logger.info("image/gif link detected")
            send_link = True
#            embed = embed.set_image(url=post_url)

        logger.debug("sending permalink: %s\n\npermalink_hashes is before add: %s\n\npermalink in hashes? %s\n\n" % (post_permalink, permalink_hashes, post_permalink in permalink_hashes))

        permalink_hashes.add(post_permalink)
        await client.send_message(message.channel, embed=embed)
        if send_link:
            await client.send_message(message.channel, post_url)

if __name__ == "__main__":
    logger.setLevel(logging.INFO)
    sh = logging.StreamHandler(sys.stdout)
    sh.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    sh.setFormatter(formatter)
    logger.addHandler(sh)

    read_blacklist()
    print(sub_blacklist)
    client.run(sys.argv[1])
