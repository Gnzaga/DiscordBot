# Work with Python 3.6
import discord
#For discord bot -> pip install Discord
import os
# to read files
import stocks
#uses alpha vantage api for live stock data
import WebScraperQuotes
#improts web scraper program
from random import randint
#random for random functionality


from discord.ext import commands
from discord.utils import get
from discord import FFmpegPCMAudio
#other discord stuff

from os import system
#more os stuff

import time
import nacl -> pip install pynacl

#more other stuff
import asyncio

#asyncio for async functions! -> pip install asyncio


#import resourcesTemplate
import resources
#see resourceTemplate.py for explanation on how to use.

TOKEN = resources.TOKEN
bot = commands.Bot(command_prefix='!')
client = discord.Client()
songs = asyncio.Queue()
play_next_song=asyncio.Event()


hiNum = 100
loNum = 0
guessNum = (hiNum - loNum) / 2
guessGameInProgress = False
guessCount = 0




@bot.command(name='MCServerAddress', brief="Gives Minecraft Server Address", description="Gives you address of our most current active MC server")
async def MCServerAddress(ctx):
    await ctx.send("gnzaga.aternos.me")
@bot.command(name='quote',brief="Gives Physics Quote", description='gives a cool physics quote')
async def quote(ctx):
    a = WebScraperQuotes.getRandQuote()
    await ctx.send(a)


@bot.command(name='add', brief="Adds Two Numbers", description='adds TWO numbers')
async def add(ctx, a: int, b: int):
    out = a+b
    await ctx.send(out)


@bot.command(name='multiply',brief="Multiply Two Numbers", description='multiplies TWO numbers')
async def multiply(ctx, a: int, b: int):
    await ctx.send(a * b)

@bot.command(name='crypto', brief="Returns Price of Cryptocurrency", description='returns latest price of given cryptocurrency')
async def crypto(ctx, symbol: str):
    await ctx.send(stocks.getCrypto(symbol))

@bot.command(name='stock', brief="Returns Price of Stock", description='returns latest price of given stock')
async def stock(ctx, a: str):
    await ctx.send(stocks.getLatestPrice(a))

@bot.command(name='testScore', brief="Returns your test score", description='returns your test score')
async def testScore(ctx):
    score = randint(0,100)

    message = "You scored a " + str(score) + " - "

    if score < 60:
        message = message + resources.message60

    if score >= 60 and score < 70:
        message = message + resources.message70
    if score >= 70 and score < 80:

        message = message + resources.message80

    if score >= 80 and score < 90:
        message = message + resources.message90

    if score >= 90 and score < 100:
        message = message + resources.message100

    await ctx.send(message)

@bot.command(name='greeting', description='gives a random greeting')
async def greet(message):
    greetings = resources.greetings
    await message.send(greetings[randint(0, len(greetings) - 1)])


@bot.command(name='cat', description='Sends a cat GIF')
async def cat(ctx):
    await ctx.send("https://media.giphy.com/media/JIX9t2j0ZTN9S/giphy.gif")



@bot.command(name="bye", description="Says Goodbye")
async def bye(message):
    await message.send("yup see ya")



#Experimental / no use at the moment below
"""
@bot.command(pass_context=True, brief="Makes the bot join your channel", aliases=['j', 'jo'])
async def join(ctx):
    channel = ctx.message.author.voice.channel
    if not channel:
        await ctx.send("You are not connected to a voice channel")
        return
    voice = get(bot.voice_clients, guild=ctx.guild)
    if voice and voice.is_connected():
        await voice.move_to(channel)
    else:
        voice = await channel.connect()
    await voice.disconnect()
    if voice and voice.is_connected():
        await voice.move_to(channel)
    else:
        voice = await channel.connect()
    await ctx.send(f"Joined {channel}")

@bot.command(pass_context=True, brief="Makes the bot leave your channel", aliases=['l', 'le', 'lea'])
async def leave(ctx):
    channel = ctx.message.author.voice.channel
    voice = get(bot.voice_clients, guild=ctx.guild)
    if voice and voice.is_connected():
        await voice.disconnect()
        await ctx.send(f"Left {channel}")
    else:
        await ctx.send("Don't think I am in a voice channel")


@client.event
async def on_message(message):
    if message.content.startswith('rom'):
        channel=message.channel
        await channel.send()





@client.event
async def on_ready():
    print(f'{client.user.name} has connected to Discord!')



@client.event
async def on_member_join(member):
    greetings = [f'Alright, {member.name} take your seat',
                 f'Welcome back {member.name}, you are late',
                 f'{member.name}, make sure you are NOT being part of the problem',
                 f'{member.name} stop being such a boring person, get off your phone and get a life']
    await member.send(greetings[randint(0, len(greetings))])


@bot.command(name='guess', brief = "Guesses number between 1 and 100")
async def guess(ctx, *argv):
    global guessGameInProgress
    global hiNum
    global loNum
    global guessNum
    global guessCount
    if guessGameInProgress ==  False:
        await ctx.send("Think of a number, Rom will try to guess it!")
        await ctx.send("If it's correct, send '!guess right'")
        await ctx.send("If it's incorrect, send '!guess wrong'")
    guessGameInProgress = True



"""
#end of experimental / No Use



bot.run(TOKEN)
