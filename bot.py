import os
import random
import discord
from dotenv import load_dotenv
from discord.ext import commands
from redditgrabber.main_classes import RedditAPI

bot = commands.Bot(command_prefix="+")

class DiscordBot:
    def __init__(self):
        load_dotenv()
        self.TOKEN = os.getenv('DISCORD_TOKEN')
        # bot = commands.Bot(command_prefix="+")
        bot.run(self.TOKEN)

    @staticmethod
    @bot.event
    async def on_ready():
        print("{} has connected to Discord".format(bot.user.name))
    #    for guild in client.guilds:
    #        print("Connected to guild {}, id:{}".format(guild.name, guild.id))
        guild = discord.utils.get(bot.guilds)
    #    print(repr(guild))
        print("Connected to guild {}, id:{}".format(guild.name, guild.id))

    @staticmethod
    @bot.command(name="hello", help="Responds with a hello message")
    async def hello(ctx):
        hellos = [
            "Hello! <@{}>",
            "Hey! <@{}>",
            "Grandma <@{}>, is that you?",
            "<@{}>! you finally came back, where's the milk though?",
            "<@{}>, who even are you?"]

        response = random.choice(hellos)
        response = response.format(ctx.author.id)
        await ctx.send(response)

    @staticmethod
    @bot.command(name="pic", help="Responds with the current top image from r/pics")
    async def reddit_pic(ctx):
        pics = RedditAPI().pics()
        for (title, score, url, selftext, author, post_id) in pics:
            attach = discord.Embed(
                title=title,
                description=selftext,
                url="https://redd.it/"+str(post_id)
            )
            attach.set_image(url=url)
            attach.add_field(name="Upvotes", value=score)
            attach.add_field(name="User", value="u/" + str(author))
            await ctx.send(embed=attach)