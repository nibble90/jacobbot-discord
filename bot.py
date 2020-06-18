import os
import random
import discord
from dotenv import load_dotenv
from discord.ext import commands

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix="+")

@bot.event
async def on_ready():
    print("{} has connected to Discord".format(bot.user.name))
#    for guild in client.guilds:
#        print("Connected to guild {}, id:{}".format(guild.name, guild.id))
    guild = discord.utils.get(bot.guilds)
#    print(repr(guild))
    print("Connected to guild {}, id:{}".format(guild.name, guild.id))

@bot.command(name="hello", help="Responds with a hello message")
async def hello(ctx):
    hellos = [
        "Hello! <@{}>",
        "Hey! <@{}>",
        "Grandma <@{}>, is that you?",
        "<@{}>! you finally came back, where is the milk though?",
        "<@{}>, who even are you?"]

    response = random.choice(hellos)
    response = response.format(ctx.author.id)
    await ctx.send(response)






bot.run(TOKEN)
