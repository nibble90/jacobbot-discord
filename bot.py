import os
import random
import discord
from dotenv import load_dotenv
from discord.ext import commands
from redditgrabber.main_classes import RedditAPI
from twitterinterface.main import User_OAuth

bot = commands.Bot(command_prefix="+")

class DiscordBot:
    def __init__(self):
        load_dotenv(dotenv_path="/home/ubuntu/jacobbot/discordbot/.env")
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
        for (nsfw, title, score, url, selftext, author, post_id) in pics:
            attach = discord.Embed(
                title=title,
                description=selftext,
                url="https://redd.it/"+str(post_id)
            )
            attach.set_image(url=url)
            attach.add_field(name="Upvotes", value=score)
            attach.add_field(name="User", value="u/" + str(author))
            await ctx.send(embed=attach)

    @staticmethod
    @bot.command(name="sub", help="Responds with the current top image from the provided sub")
    async def subreddit(ctx, sub: str):
        results = RedditAPI().subreddit_search(sub)
        for (nsfw, title, score, url, selftext, author, post_id) in results:
            attach = discord.Embed(
                title=title,
                description=selftext,
                url="https://redd.it/"+str(post_id)
            )
            attach.set_image(url=url)
            attach.add_field(name="Upvotes", value=score)
            attach.add_field(name="User", value="u/" + str(author))
            await ctx.send(embed=attach)
    @staticmethod
    @bot.command(name="twitterregister", help="Responds with link to register bot to your Twitter account")
    async def twitter_register(ctx):
        uuid = ctx.author.id
        url = User_OAuth(str(uuid)).generate_url()
        attach = discord.Embed(title="Twitter Authorisation Link",
                                description="Click this link to authorise your twitter account to this bot",
                                url=url)
        await ctx.author.send(embed=attach)
        # print(ctx.author.id)
        