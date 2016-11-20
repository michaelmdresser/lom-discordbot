var Discord = require("discord.js");
var request = require("request");
var bot = new Discord.Client();

bot.on("message", msg => {

    let prefix = "!";

    if (msg.author.bot) return;

    else if (msg.content.contains("kys")) {
        msg.channel.sendMessage("Please don't actually");
    }

});

bot.on('ready', () => {
  console.log('I am ready!');
});

var KEY = process.env.KEY || require('./config')

bot.login(KEY);
