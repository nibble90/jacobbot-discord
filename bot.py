import os
import random
import discord
from dotenv import load_dotenv
from discord.ext import commands
from redditgrabber.main_classes import RedditAPI
from twitterinterface.main import User_OAuth, User_Unauthenticated

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
    
    @staticmethod
    @bot.command(name="tweet", help="Tweets a message from your twitter account")
    async def tweet(ctx, *, message):
        uuid = ctx.author.id
        inst = User_OAuth(str(uuid))
        authorised = inst.attempt_authorise()
        if(not authorised):
            url = inst.generate_url()
            attach = discord.Embed(title="Twitter Authorisation Link",
                                    description="Click this link to authorise your twitter account to this bot",
                                    url=url)
            await ctx.author.send(embed=attach)
        else:
            if(len(message) > 280):
                await ctx.send("This message is above the 280 character Twitter limit")
            else:
                inst.tweet(message)

    @staticmethod
    @bot.command(name="twitteruser", help="Gathers information on a twitter user")
    async def twitteruser(ctx, username):
        user = str(username)
        inst = User_Unauthenticated(user)
        info = inst.basic_info() #return self.screen_name, self.name, self.description, self.follower_count, self.profile_picture
        attach = discord.Embed(title=str(info[1]),
                                description=str(info[2]),
                                url=str(info[5]))
        attach.add_field(name="Username", value="@{}".format(info[0]))
        attach.add_field(name="Followers", value=info[3])
        attach.set_image(url=info[4])
        await ctx.send(embed=attach)

    @staticmethod
    @bot.command(name="gettweet", help="Gets a user's most recent tweet")
    async def gettweet(ctx, username):
        user = str(username)
        inst = User_Unauthenticated(user)
        info = inst.last_tweet(formatting="chatbot") #return self.screen_name, self.name, self.description, self.follower_count, self.profile_picture
        attach = discord.Embed(title="@{}".format(info[2]),
                                description=str(info[0]),
                                url=str(info[1]))
        attach.set_image(url=info[3])
        await ctx.send(embed=attach)

                
if __name__ == "__main__":
    DiscordBot()