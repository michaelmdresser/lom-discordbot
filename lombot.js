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
        request("https://www.reddit.com/r/me_irl/top.json" + size, function(error, response, body) {
            cnt = JSON.parse(body).content
            msg.channel.sendMessage(cnt["data"]["url"])
        });
    }

});

bot.on('ready', () => {
  console.log('I am ready!');
});

var KEY = process.env.KEY || require('./config')

bot.login(KEY);
