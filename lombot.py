# python 3
import discord
import asyncio
import requests
import sys
import random
import re

client = discord.Client()

def random_from_subreddit(subreddit):
    url = "https://www.reddit.com/r/" + subreddit + "/top/.json"
    h = {"User-Agent": "lombot v1"}
    post_position = random.randrange(0, 25)

    response = requests.get(url, headers=h)
    print(len(response.json()["data"]["children"]))
    response_url = response.json()["data"]["children"][post_position]["data"]["url"]

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
    client.run(sys.argv[1])
