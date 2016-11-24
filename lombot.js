var Discord = require("discord.js");
var request = require("request");
var bot = new Discord.Client();

bot.on("message", msg => {

    let prefix = "!";

    msg.content = msg.content.toLowerCase();

    if (msg.author.bot) return;

    else if (msg.content.startsWith(prefix) && msg.content.includes("d")) {
        spl = msg.content.split("d");
        spl[0] = spl[0].substring(1, spl[0].length);
        space = spl[1].search(" ");
        if (space != -1) {
            spl[1] = spl[1].substring(0, space);
        }
        console.log(spl);
        var sum = 0;
        var first = Number(spl[0]);
        var second = Number(spl[1]);
        if (spl[0] == "") {
            first = 1;
        }

        if (first != NaN && second != NaN && Math.abs(first) < 100000) {
            for (i = 0; i < first; i++) {
                sum += Math.floor(Math.random() * second) + 1;
            }
        }
        if (sum != 0 && sum != NaN) {
            msg.channel.sendMessage(sum);
        }
    }

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

    if (msg.content.includes("should i do it")) {
        msg.channel.sendMessage("do it");
    }

    if (msg.content.includes("gopitt")) {
        msg.channel.sendMessage("Fuck Penn State");
    }

    if (msg.content.includes("fuck penn state")) {
        msg.channel.sendMessage("Fight on for dear old Pittsburgh\nAnd for the glory of the game\nShow our worthy foe that the Panther's on the go\nPitt must win today! Rah! Rah! Rah!\nCheer loyal sons of Pittsburgh\nCheer on to victory and fame\nFor the Blue and gold shall conquer as of old\nSo fight, Pitt, fight!");
    }

    if (msg.content.includes("gregory")) {
        msg.channel.sendMessage("eyy");
    }

});

bot.on('ready', () => {
  console.log('I am ready!');
});

var KEY = process.env.KEY || require('./config')

bot.login(KEY);
