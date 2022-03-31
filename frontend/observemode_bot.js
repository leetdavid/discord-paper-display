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

  console.log(message);

  if (message.content === "image" && message.attachments.size === 1) {
    console.log('image detected')
    message.attachments.forEach(item => {
      if(item.url.endswith('jpg') || item.url.endswith('jpeg') || item.url.endsWith('png')) {
        const file = fs.createWriteStream(`/tmp/discord_display_image.jpg`);
        
        https.get(item.url, function(response) {
          response.pipe(file);
          file.on('finish', () => {
            file.close(() => {
              $.ajax({
                url: `${backendUrl}/image`,
                dataType: "text",
                accepts: {
                    text: "text/plain"
                }
              })
            })
          })
        }).on('error', (err) => {
          fs.unlink(dest);
        })
      }
    })
  } else {
    const text = message.content
    $.ajax({
      url: `${backendUrl}/text?author=${message.author.username}&text=${text}`,
      dataType: "text",
      accepts: {
          text: "text/plain"
      }
    });
  }
});