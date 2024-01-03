import discord
from discord.ext import commands
from discord.ui import Button, View
import os

intents = discord.Intents.all()
intents.messages = True
intents.reactions = True

bot = commands.Bot(command_prefix='!', intents=intents)

# Dict to store user data
user_data = {}


@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name} ({bot.user.id})')


@bot.command(name='start')
async def start(ctx):
    # Check if user already exists in data
    if ctx.author.id in user_data:
        await ctx.send("You've already started the RPG!")
        return

    await ctx.send("Welcome to DB Legends RPG! Click the button to set your name.")
    view = View()
    view.add_item(Button(style=discord.ButtonStyle.primary, label="Set Name", custom_id="set_name"))
    await ctx.send("Click the button to set your name.", view=view)


@bot.command(name='grind')
async def grind(ctx):
    # Check if user has started the RPG
    if ctx.author.id not in user_data:
        await ctx.send("You need to start the RPG first. Use `!start`.")
        return

    # Simulate grinding and get random chrono crystals
    chrono_crystals = 10  # replace this with a random value between 10 and 150
    character_url = get_random_character()

    # Send embed with chrono crystals and character
    embed = discord.Embed(title=f"You grinded {chrono_crystals} Chrono Crystals!", color=discord.Color.green())
    embed.set_image(url=character_url)

    # Check if the user leveled up
    if ctx.author.id in user_data:
        user_data[ctx.author.id]['exp'] += 1
        if user_data[ctx.author.id]['exp'] % 10 == 0:
            level = user_data[ctx.author.id]['exp'] // 10
            character_url = get_level_up_character(level)
            embed.set_image(url=character_url)
            user_data[ctx.author.id]['cc'] += 10
            embed.description = f"Congratulations! You leveled up to level {level} and gained 10 Chrono Crystals."

    await ctx.send(embed=embed)


# Helper function to get a random character URL
def get_random_character():
    characters = [
        "https://dblegends.net/assets/card_cutins/BChaCut_0540_Jiren_540.webp",
        "https://dblegends.net/assets/card_cutins/BChaCut_0534_Cell2nd_534.webp",
        "https://dblegends.net/assets/card_cutins/BChaCut_0577_GoldenFrieza_577.webp",
        "https://dblegends.net/assets/card_cutins/BChaCut_0565_GokuTeen_565.webp",
        "https://dblegends.net/assets/card_cutins/BChaCut_0543_Champa_543.webp",
        "https://dblegends.net/assets/card_cutins/BChaCut_0400_Vegeta_400.webp"
    ]
    return characters[random.randint(0, len(characters) - 1)]


# Helper function to get a character URL based on the user's level
def get_level_up_character(level):
    # Assume the character list is in the same order as provided in the question
    characters = [
        "https://dblegends.net/assets/card_cutins/BChaCut_0540_Jiren_540.webp",
        "https://dblegends.net/assets/card_cutins/BChaCut_0534_Cell2nd_534.webp",
        "https://dblegends.net/assets/card_cutins/BChaCut_0577_GoldenFrieza_577.webp",
        "https://dblegends.net/assets/card_cutins/BChaCut_0565_GokuTeen_565.webp",
        "https://dblegends.net/assets/card_cutins/BChaCut_0543_Champa_543.webp",
        "https://dblegends.net/assets/card_cutins/BChaCut_0400_Vegeta_400.webp"
    ]
    return characters[(level // 10) % len(characters)]

@bot.event
async def on_message(message):
    # Ignore messages from the bot itself
    if message.author.bot:
        return

    # Check if the user has started the RPG
    if message.author.id in user_data:
        user_data[message.author.id]['exp'] += 1
        current_exp = user_data[message.author.id]['exp']

        # Calculate the required XP for the next level (adjust the growth rate as needed)
        required_exp = 10 * (2 ** (current_exp // 10))

        if current_exp >= required_exp:
            level = current_exp // 10
            character_url = get_level_up_character(level)
            embed = discord.Embed(
                title=f"Congratulations, {message.author.display_name}!",
                description=f"You leveled up to level {level} and gained 10 Chrono Crystals.",
                color=discord.Color.green()
            )
            embed.set_image(url=character_url)
            user_data[message.author.id]['cc'] += 10
            await message.channel.send(embed=embed)

    await bot.process_commands(message)
  
TOKEN = os.getenv("TOKEN")

# Start the bot
bot.run(TOKEN)
