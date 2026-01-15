import discord
from discord.ext import commands
import requests
from bs4 import BeautifulSoup
import random
import re
import json
import os
import io
import base64
from collections import Counter
from conversation_manager import load_conversations, save_conversations, update_conversation, get_conversation
import resources
import stocks

# Configuration from environment variables with defaults
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN', resources.TOKEN)
OLLAMA_URL = os.getenv('OLLAMA_URL', 'http://localhost:11434')
OLLAMA_MODEL = os.getenv('OLLAMA_MODEL', 'dolphin-llama3')
STABLE_DIFFUSION_URL = os.getenv('STABLE_DIFFUSION_URL', 'http://localhost:7860')
STABLE_DIFFUSION_API_URL = f'{STABLE_DIFFUSION_URL}/sdapi/v1/txt2img'

# Define intents
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

# Initialize bot with intents
bot = commands.Bot(command_prefix='!', intents=intents)


wordles = {}

# Load wordles from file
def setOfWordles():
    wordles_path = os.path.join(os.path.dirname(__file__), "wordles.txt")
    try:
        with open(wordles_path) as fn:
            for line in fn:
                wordles[line.strip().upper()] = True
        print(f"Loaded {len(wordles)} words for Wordle")
    except FileNotFoundError:
        print("Warning: wordles.txt not found. Wordle game will not work.")

setOfWordles()

# Utility function to check if a character is in the allowed ASCII range
def is_normal(s):
    forbidden_ascii_nums = [35, 36, 37, 28, 29, 43, 60, 61, 62, 64, 91, 93, 94, 123, 124, 125, 126]
    return all(ord(a) not in forbidden_ascii_nums for a in s)

# Quote command
@bot.command(name='quote', brief="Gives a Physics Quote")
async def quote(ctx):
    await ctx.trigger_typing()
    URL = "https://www.goodreads.com/quotes/tag/physics"
    num = random.randint(1, 25)
    if num > 1:
        URL += f"?page={num}"

    quotes = []
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, 'html.parser')
    res = soup.find_all(class_='quoteText')

    for a in res:
        if is_normal(a.text):
            quotes.append(a.text)

    if quotes:
        await ctx.send(quotes[random.randint(0, len(quotes) - 1)])
    else:
        await ctx.send("No quotes found.")

# Simple math operations
@bot.command(name='add', brief="Adds Two Numbers", description='Adds TWO numbers')
async def add(ctx, a: int, b: int):
    await ctx.send(a + b)

@bot.command(name='multiply', brief="Multiply Two Numbers", description='Multiplies TWO numbers')
async def multiply(ctx, a: int, b: int):
    await ctx.send(a * b)

# Stock and crypto price commands
@bot.command(name='crypto', brief="Returns Price of Cryptocurrency", description='Returns latest price of given cryptocurrency')
async def crypto(ctx, symbol: str):
    await ctx.trigger_typing()
    await ctx.send(stocks.getCrypto(symbol))

@bot.command(name='stock', brief="Returns Price of Stock", description='Returns latest price of given stock')
async def stock(ctx, symbol: str):
    await ctx.trigger_typing()
    await ctx.send(stocks.getLatestPrice(symbol))

# Test score generator
@bot.command(name='testScore', brief="Returns your test score", description='Returns your test score')
async def testScore(ctx):
    score = random.randint(0, 100)
    messages = [resources.message60, resources.message70, resources.message80, resources.message90, resources.message100]
    if score < 60:
        message = f"You scored a {score} - {messages[0]}"
    elif score < 70:
        message = f"You scored a {score} - {messages[1]}"
    elif score < 80:
        message = f"You scored a {score} - {messages[2]}"
    elif score < 90:
        message = f"You scored a {score} - {messages[3]}"
    else:
        message = f"You scored a {score} - {messages[4]}"
    
    await ctx.send(message)

# Greet command
@bot.command(name='greeting', description='Gives a random greeting')
async def greet(ctx):
    greetings = resources.greetings
    await ctx.send(greetings[random.randint(0, len(greetings) - 1)])

# Define command to look up word definitions
@bot.command(name="define", description="Define the word")
async def define(ctx, word: str):
    await ctx.trigger_typing()
    URL = f"https://merriam-webster.com/dictionary/{word}"
    regex = re.compile('.*sense .*')
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, 'html.parser')
    res = soup.find_all("div", {"class": regex})

    out = word
    count = 1

    for a in res:
        if is_normal(a.text) and len(a.text) > 5:
            for b in a.text.split("\n"):
                if len(b) > 5 and b.startswith(':') and count <= 5:
                    out += f"\n{count}{b}"
                    count += 1

    if out == word:
        await ctx.send(f"Sorry, but **{word}** couldn't be found in the dictionary.")
    else:
        await ctx.send(out)

# Wordle commands
@bot.command(name="iswordle", description="Checks if a word is a wordleable word!")
async def iswordle(ctx, word: str):
    if word.upper() in wordles:
        await ctx.send(f"{word} is a playable word!")
    else:
        await ctx.send(f"{word} is NOT a playable word!")
#########################################################

@bot.command(name="wordle", description="Play Wordle!")
async def wordle(ctx):
    green_square = ":green_square:"
    yellow_square = ":yellow_square:"
    black_square = ":white_square_button:"
    
    alphabet = list("ABCDEFGHIJKLMNOPQRSTUVWXYZ")  # Usable letters list

    def to_string(arr):
        return " ".join(arr)

    def result(guess, answer):
        out = ""
        is_green = [False] * len(guess)
        answer_count = Counter(answer)  # Count occurrences of each letter in the answer

        # First pass: Identify green squares (correct letter and correct position)
        for i in range(len(guess)):
            if guess[i] == answer[i]:
                is_green[i] = True
                answer_count[guess[i]] -= 1  # Reduce the count in answer for green matches

        # Second pass: Identify yellow squares (correct letter but wrong position)
        for i in range(len(guess)):
            if not is_green[i]:
                if guess[i] in answer_count and answer_count[guess[i]] > 0:
                    # Mark yellow if the letter exists in the answer and hasn't been used up
                    out += yellow_square
                    answer_count[guess[i]] -= 1  # Reduce the count for yellow matches
                else:
                    out += black_square
                    if guess[i] in alphabet:
                        # Cross out the letter in the alphabet if it's completely wrong
                        alphabet[alphabet.index(guess[i])] = f"~~{guess[i]}~~"
            else:
                out += green_square  # Green square for correct letters

        return out

    def get_word():
        return random.choice(list(wordles.keys()))

    word = get_word().upper()
    print(f"Word to guess: {word}")

    board = []
    won = False
    exit_game = False
    tries = 6
    out = ""

    def get_name(name):
        return name.split("#")[0]

    def check(msg):
        return msg.author == ctx.author and msg.channel == ctx.channel

    player = get_name(str(ctx.author))
    print(f"New Game: {player} -> {word}")

    for i in range(tries):
        await ctx.send(f'{player}, guess a 5-letter word. You have {tries - i} tries left!')

        response = await bot.wait_for('message', check=check)
        response_text = response.content.upper()

        if response_text == "QUIT":
            exit_game = True
            await ctx.send(f"{player} has quit the game.")
            break

        # Validate input is exactly 5 alphabetic characters
        while (len(response_text) != 5) or not response_text.isalpha():
            if not response_text.isalpha():
                await ctx.send(f'{player}, please use only letters. Try again!')
            else:
                await ctx.send(f'{player}, the word must be exactly 5 letters. Try again!')
            response = await bot.wait_for('message', check=check)
            response_text = response.content.upper()

            if response_text == "QUIT":
                exit_game = True
                await ctx.send(f"{player} has quit the game.")
                break

        if exit_game:
            break

        # Validate only 5-character words from the word list
        while len(response_text) == 5 and response_text not in wordles:
            await ctx.send(f'{player}, {response_text} is an invalid word. Try again!')
            response = await bot.wait_for('message', check=check)
            response_text = response.content.upper()

            if response_text == "QUIT":
                exit_game = True
                await ctx.send(f"{player} has quit the game.")
                break

        if exit_game:
            break

        row = result(response_text, word)
        board.append(row)

        if response_text == word:
            won = True
            out += "\n".join(board) + "\n"
            out += f"{player} guessed **{word}** in {i + 1} {'tries' if i != 0 else 'try'}!\n"
            await ctx.send(out)
            break
        else:
            usable_letters = to_string(alphabet)  # This will now include crossed-out letters
            await ctx.send(f"[{player}]\n**Usable Letters**: {usable_letters}\n**Guess**: {response_text}")
            await ctx.send(row)

    if not won and not exit_game:
        out += "\n".join(board) + "\n"
        out += f"{player}, the word was **{word}**."
        await ctx.send(out)








#########################################################
# Conversation handling and response from Ollama
context_timeout = 1200  # 20 minutes in seconds
active_conversations = load_conversations()

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    guild_id = message.guild.id if message.guild else "DM"  # Use "DM" for direct messages
    channel_id = message.channel.id

    if bot.user in message.mentions or (message.reference and message.reference.resolved and message.reference.resolved.author == bot.user):
        user_input = message.content.replace(f"<@{bot.user.id}>", "").strip()

        # Retrieve previous context if available
        previous_context = get_conversation(active_conversations, guild_id, channel_id, context_timeout)
        prompt = f"{previous_context}\nUser: {user_input}" if previous_context else f"User: {user_input}"

        url = f"{OLLAMA_URL}/api/generate"

        payload = {
            "model": OLLAMA_MODEL,
            "prompt": prompt
        }

        try:
            async with message.channel.typing():
                response = requests.post(url, json=payload, stream=True)
                response.raise_for_status()

                bot_response = ""
                for line in response.iter_lines():
                    if line:
                        json_data = line.decode('utf-8')
                        result = json.loads(json_data)

                        if "response" in result:
                            bot_response += result["response"]

                        if result.get("done", False):
                            break

                if bot_response:
                    update_conversation(active_conversations, guild_id, channel_id, user_input, bot_response)

                    if len(bot_response) > 2000:
                        chunks = [bot_response[i:i + 2000] for i in range(0, len(bot_response), 2000)]
                        for chunk in chunks:
                            await message.channel.send(chunk)
                    else:
                        await message.channel.send(bot_response)
                else:
                    await message.channel.send("No response received from Ollama.")
        except requests.exceptions.RequestException as e:
            await message.channel.send(f"Error: {e}")

    await bot.process_commands(message)

@bot.command(name='endconvo', help="Ends the current conversation and clears the context.")
async def end_conversation(ctx):
    guild_id = ctx.guild.id if ctx.guild else "DM"
    channel_id = ctx.channel.id
    key = f"{guild_id}-{channel_id}"

    if key in active_conversations:
        del active_conversations[key]
        save_conversations(active_conversations)
        await ctx.send("Conversation context cleared for this channel.")
    else:
        await ctx.send("No active conversation found for this channel.")



@bot.command()
async def generate(ctx, *, prompt: str):
    """
    Takes a prompt from the user, sends it to the Stable Diffusion server, and returns the generated image.
    """
    await ctx.send(f'Generating image for: "{prompt}"...')

    # Prepare the request payload for Stable Diffusion
    payload = {
        "prompt": prompt,
        "steps": 20  # Number of inference steps, can be adjusted
    }

    try:
        # Send POST request to Stable Diffusion API
        response = requests.post(STABLE_DIFFUSION_API_URL, json=payload)
        response.raise_for_status()

        # Get the generated image data (assuming the API returns it as base64)
        result = response.json()
        image_base64 = result['images'][0]  # Extract the first image

        # Decode the base64 string into image bytes
        image_data = io.BytesIO(base64.b64decode(image_base64))

        # Create a Discord file object from the image bytes
        image_file = discord.File(fp=image_data, filename="generated_image.png")

        # Send the image to the Discord channel
        await ctx.send(file=image_file)

    except Exception as e:
        await ctx.send(f'An error occurred: {str(e)}')


bot.run(DISCORD_TOKEN)
