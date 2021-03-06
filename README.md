![Shikamaru is handsome](https://cdn.discordapp.com/avatars/759338827432722472/e5d0d195b45e4c057dfedda875d8eed2.png?size=1024)

# 𝓢𝓱𝓲𝓴𝓪𝓶𝓪𝓻𝓾
Shikamaru is an open-source Discord bot filled with numerous features. It's written in Python and uses Hikari, a lightweight bot framework for Python.
=======

## 𝑹𝒖𝒏𝒏𝒊𝒏𝒈 𝒕𝒉𝒆 𝒃𝒐𝒕

I already have an instance of Shikamaru hosted which you can [invite](https://discord.com/api/oauth2/authorize?client_id=759338827432722472&permissions=8&scope=bot) to your servers so it's not required for you to host it. But if you do want to run it,
you have to clone the repo first. So open up your terminal and type,

> Note: You need to at least have Python 3.8.5 already installed to run the bot

```bash
git clone https://github.com/ahnaf-zamil/shikamaru-bot.git
```

Now go to the folder and run

```py

pip install -r requirements.txt
```

You would have to create a `config.ini` file and then fill it according to the `config.example.ini` file. Also make a new environment variable called `TOKEN` and put your bot's token there. You also need to make an account at [Imgflip](https://imgflip.com) becuase this bot is using their API for the meme generator commands. Store your Imgflip username and password in two environment variables called ``IMGFLIPUSER`` and ``IMGFLIPPASS`` because making an API request to their API will require you to use your Imgflip username and password.


If you are using Windows then open your command prompt and write
```cmd
SET TOKEN=your bot token
SET IMGFLIPUSER=your imgflip username
SET IMGFLIPPASS=your imgflip password
```

If you are using Linux then write
```bash
export TOKEN=your bot token
export IMGFLIPUSER=your imgflip username
export IMGFLIPPASS=your imgflip password
```

Then run the bot using

```bash
python run.py
```

## 𝑪𝒐𝒏𝒕𝒓𝒊𝒃𝒖𝒕𝒊𝒏𝒈

Shikamaru is a new Discord bot and it requires a lot of development so your contribution is welcome. If you want to add any plugins/cogs to the bot, just email me or make an issue on the repository [here](https://github.com/ahnaf-zamil/shikamaru-bot/issues).
