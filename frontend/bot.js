const Discord = require("discord.js");
const client = new Discord.Client({ intents: ["GUILDS", "GUILD_MESSAGES"] });
const { JSDOM } = require("jsdom");
const { window } = new JSDOM("");
const $ = require("jquery")(window);
const http = require("http");
const https = require('https');
const fs = require('fs')

const token = process.argv.slice(2)[0];
const botId = process.argv.slice(2)[1];

backendUrl = 'http://127.0.0.1:8000'

client.login(token);

client.on("messageCreate", async message => {
    if (message.content.startsWith("draw ")) {
        const text = message.content.substring(5)
        message.react("⏱️")
        $.ajax({
            url: `${backendUrl}/text?author=${message.author.username}&text=${text}`,
            dataType: "text",
            accepts: {
                text: "text/plain"
            }
        }).done(response => {
            const botReactions = message.reactions.cache.filter(reaction => reaction.users.cache.has(botId));
            for (const reaction of botReactions.values())
                reaction.users.remove(botId);
            message.react("✏️");
        }).fail(err => {
            message.react("❌");
        });
    }

    if (message.content === "image" && message.attachments.size === 1) {
        message.attachments.forEach(item => {
            if (item.url.endsWith("jpg") || item.url.endsWith("jpeg") || item.url.endsWith("png")) {
                message.react("⏱️")
                const file = fs.createWriteStream(`/tmp/in.jpg`);
                https.get(item.url, function (response) {
                    response.pipe(file);
                    file.on('finish', function () {
                        file.close(() => {
                            $.ajax({
                                url: `${backendUrl}/image`,
                                dataType: "text",
                                accepts: {
                                    text: "text/plain"
                                }
                            }).done(response => {
                                const botReactions = message.reactions.cache.filter(reaction => reaction.users.cache.has(botId));
                                for (const reaction of botReactions.values())
                                    reaction.users.remove(botId);
                                message.react("✏️");
                            }).fail(err => {
                                const botReactions = message.reactions.cache.filter(reaction => reaction.users.cache.has(botId));
                                for (const reaction of botReactions.values())
                                    reaction.users.remove(botId);
                                message.react("❌");
                            });
                        });
                    });
                }).on('error', function (err) {
                    fs.unlink(dest);
                    message.react("❌")
                });
            } else {
                message.react("❌")
            }
        });
    }
})