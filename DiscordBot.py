#import resourcesTemplate as resources
import resources
#see resourceTemplate.py for explanation on how to use.
import discord
#For discord bot -> pip install Discord
import os
# to read files
import stocks
#uses alpha vantage api for live stock data
from random import randint
#random for random functionality
import requests
from bs4 import BeautifulSoup

from discord.ext import commands
from discord.utils import get
#other discord stuff

from os import system
#more os stuff

import time
import nacl #-> pip install pynacl

#more other stuff
import asyncio
import re
#asyncio for async functions! -> pip install asyncio




TOKEN = resources.TOKEN
bot = commands.Bot(command_prefix='!')
client = discord.Client()

wordles={}

forbiddenAsciiNums = [35,36,37,28,29,43,60,61,62,64,91,93,94,123,124,125,126]
def setOfWordles():
    fn=open("wordles.txt")
    lines = fn.readlines()
    for line in lines:
        wordles[line.strip()] = True

setOfWordles()


@bot.command(name='quote', brief="Gives Physics Quote")
async def quote(ctx):
    def isNormal(s):
        forbiddenAsciiNums = [35,36,37,28,29,43,60,61,62,64,91,93,94,123,124,125,126]
        for a in s:
            temp = ord(a)
            try:
                forbiddenAsciiNums.index(temp)
                return False
            except Exception:
                continue
        return True
     
    await ctx.trigger_typing()
    URL= "https://www.goodreads.com/quotes/tag/physics"
    num = randint(1,25)
    if num > 1:    
        URL = URL + "?page=" + str(num)
     
    quotes = []

    page = requests.get(URL)
    soup = BeautifulSoup(page.content, 'html.parser')
    res = soup.find_all(class_='quoteText')
    
    for a in res:
        if isNormal(a.text):
            quotes.append(a.text)
    await ctx.send(quotes[randint(0,len(quotes))])


@bot.command(name='add', brief="Adds Two Numbers", description='adds TWO numbers')
async def add(ctx, a: int, b: int):
    out = a+b
    await ctx.send(out)


@bot.command(name='multiply',brief="Multiply Two Numbers", description='multiplies TWO numbers')
async def multiply(ctx, a: int, b: int):
    await ctx.send(a * b)

@bot.command(name='crypto', brief="Returns Price of Cryptocurrency", description='returns latest price of given cryptocurrency')
async def crypto(ctx, symbol: str):
    await ctx.trigger_typing()
    await ctx.send(stocks.getCrypto(symbol))

@bot.command(name='stock', brief="Returns Price of Stock", description='returns latest price of given stock')
async def stock(ctx, a: str):
    await ctx.trigger_typing()
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

@bot.command(name="define", definition="Define the word")
async def define(ctx, word : str):
    await ctx.trigger_typing()
    URL = "https://merriam-webster.com/dictionary/"
    URL = URL + word
    regex = re.compile('.*sense .*')
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, 'html.parser')
    res = soup.find_all("div", {"class" : regex})

    out = word
    count = 1

    def isNormal(s):
        for a in s:
            temp = ord(a)
            try:
                forbiddenAsciiNums.index(temp)
            except Exception:
                continue
        return True
    for a in res:
        if isNormal(a.text) and len(a.text) > 5:
            for b in a.text.split("\n"):
                if len(b) > 5 and b[0] == ':' and count <= 5:
                    out = out + "\n" + str(count) + b
                    count = count + 1
    if out == word:
        await ctx.send("Sorry, but **" + word + "** couldn't be found in the dictionary.")
       
    else:
        await ctx.send(out)
    


@bot.command(name="iswordle", description="Checks if word is a wordleable word!")
async def iswordle(message, word : str):
    if word in wordles:
        await message.send(word + " is a playable word!")
    else:
        await message.send(word + " is NOT a playable word!")


@bot.command(name="wordle", description="Play Wordle!")
async def wordle(ctx):
    greenSquare = ":green_square:"
    yellowSquare = ":yellow_square:"
    blackSquare = ":white_square_button:"

    alphabet = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L",
            "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y",
            "Z"]
    #This function generates the row for A users valid input
    #takes in guess and answer, assumes guess is valid length and word
    def toString(arr):
        out = ""
        for substr in arr:
            out = out + substr
        return out
    def result(guess, answer):
        nonlocal alphabet
        #@alphabet = alphabet
        out = "";
        isGreen=[False,False,False,False, False]
        isYellow=[False,False,False,False, False]
        for i in range(len(guess)):
           if guess[i] == answer[i]:
            isGreen[i] = True
            
        for i in range(len(guess)):
            for j in range(len(guess)):
                if guess[i] == answer[j]:
                    if isGreen[j] == False:
                        isYellow[i] = True
                        

        for i in range(len(guess)):
            if isGreen[i]:
                out = out + greenSquare
            elif isYellow[i]:
                out = out + yellowSquare
            elif isYellow[i] == False and isGreen[i] == False:
                index = ord(guess[i]) - 97
                if len(alphabet[index]) == 1:
                    alphabet[index] = "~~" + alphabet[index] + "~~"
                
                out = out + blackSquare
        return out
    #fix later to use hash table instead of search
    def getWord():
        return list(wordles)[randint(0,len(list(wordles)))]
        #f = open('wordles.txt', 'r')
        #lines = f.readlines()
        #bound = randint(0,len(lines))
        #for i in range(len(lines)):
        #    if i == bound:
        #        return lines[i].strip()


    #word = res.getWordleWord();
    word = getWord()
    #word = "drops"
    print(word)
    board = []
    won = False
    exitGame = False
    tries = 6
    out = ""

    def getName(name):
        index = 0
        for i in range(len(name)):
            if name[i] == "#":
                return name[:i]
        return name
# local check function makes sure author and channel are the same
    def check(msg):
        return msg.author == ctx.author and msg.channel == ctx.channel
    
    player = getName(str(ctx.author))
    print("New Game: " + player + " -> " + word)
    for i in range(0,tries):
        if(i < tries-1):
            await ctx.send( player + ', guess a 5 letter word, you have ' + str(tries-i) + " tries left!");
        else:
            await ctx.send(player + ", guess a 5 letter word, you have 1 try left!");
        response = await bot.wait_for('message', check=check);
        response_text = response.content.lower()
        
        if(response_text == "quit"):
            break
        
        
        while(len(response_text) != 5):
            print("X " + player + " -> " + response_text + " -> " + str(len(response_text)) ) 

            if(len(response_text) > 5):
                await ctx.send(player + ", the word is GREATER than 5 letters, try again!")
            else:
                await ctx.send(player + ", the word is LESS than 5 letters, try again!")
            response = await bot.wait_for('message', check=check)
            response_text = response.content.lower()
             
            if(response_text == "quit"):
                exitGame = True
                break
        while((response_text in wordles) == False):
            print("X " + player + " -> " + response_text + " -> " + str(len(response_text)) ) 

            if(response_text == "quit"):
                exitGame = True
                break
            await ctx.send(player + ", " + response_text + " is an invalid word, try again!")
            response = await bot.wait_for('message', check=check)
            response_text = response.content.lower()
        if(exitGame):
            break
        row = result(response_text, word.lower())    
        board.append(row)
        
        if(response_text == word):
            won = True
            for m in board:
                #await ctx.send(m)
                out = out + m + "\n"
            if(i == 1):
                #await ctx.send("You took 1 try to guess " + word)
                out = out + player + " took 1 try to guess " + word + "\n"
            else:    
                #wait ctx.send("You took " + str(i+1) + " tries to guess " + word)
                out = out + player + " took " + str(i+1) + " tries to guess " + "**" + word + "**" + "\n"
            await ctx.send(out)
            break
        elif i != tries-1:
            await ctx.send("[" + player + "]\n" + "**Usable Letters**: " + toString(alphabet) + "\n**Guess**: " + response_text )
            await ctx.send(row)
            print(str(i+1) + " " + player + " -> " + response_text)

    
    if won == False:
        for i in range(len(board)):
            out = out + board[i] + "\n"
            #await ctx.send(board[i])
        out = out + player + "'s word was " + "**" + word + "**"
        #await ctx.send("The word was " + word)
        await ctx.send(out)
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



"""
#end of experimental / No Use



bot.run(TOKEN)
