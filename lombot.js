var Discord = require("discord.js");
var request = require("request");
var bot = new Discord.Client();

bot.on("message", msg => {

    let prefix = "!";

    if (msg.author.bot) return;

    else if (msg.content.includes("kys")) {
        msg.channel.sendMessage("Please don't actually");
    }

    else if (msg.content.startsWith("me_irl")) {
        request("https://www.reddit.com/r/me_irl/top.json", function(error, response, body) {
            cnt = JSON.parse(body)
            url = cnt["data"]["children"][0]["data"]["url"]
            fixed = url.replace(/&amp;/g, "&")
            msg.channel.sendMessage(fixed)
        });
    }

    if (msg.content.includes("sko buffs")) {
        msg.channel.sendMessage("Fight CU down the field,\nCU must win\nFight, fight for victory\nCU knows no defeat\nWe'll roll up a mighty score\nNever give in\nShoulder to shoulder\nWe will fight, fight\nFight, fight, fight!");
    }

    if (msg.content.includes("gopitt")) {
        msg.channel.sendMessage("Fuck Penn State");
    }

});

bot.on('ready', () => {
  console.log('I am ready!');
});

var KEY = process.env.KEY || require('./config')

bot.login(KEY);
