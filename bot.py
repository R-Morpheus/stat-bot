import os
import discord
from discord import app_commands
from discord.ext import commands
import pandas as pd
import json
import logging
from dotenv import load_dotenv


intents = discord.Intents.default()
intents.message_content = True

load_dotenv()

TOKEN = os.getenv("TOKEN")
EXCEL_ALLOWED_USER_ID_MORPHEY = os.getenv("EXCEL_ALLOWED_USER_ID_MORPHEY")
EXCEL_ALLOWED_USER_ID_CINNA = os.getenv("EXCEL_ALLOWED_USER_ID_CINNA")



bot = commands.Bot(command_prefix='.', intents=intents)

# Load the data from the JSON file
with open('data.json', 'r') as f:
    data = json.load(f)

def is_allowed_user(ctx):
    return ctx.author.id == EXCEL_ALLOWED_USER_ID_MORPHEY

# Setup the logger
logging.basicConfig(level=logging.INFO, format='%(asctime)s %(message)s')

async def log_command(interaction):
    logging.info(f'User {interaction.user.name} ({interaction.user.id}) executed command {interaction.command_name}')


@bot.event
async def on_ready():
    print('Bot is Up Ready!')
    try:
        await bot.tree.sync()
        print(f"Commands synced")
    except Exception as e:
        print(f"Error syncing commands: {e}")



@bot.tree.command(name="hello")
async def hello(interaction: discord.Interaction):
    await interaction.response.send_message(f'Hey, {interaction.user.mention}! This is slash command', ephemeral=True)




@bot.tree.command(name='say')
@app_commands.describe(thing_to_say='What should i say?')
async def say(interaction: discord.Interaction, thing_to_say: str):
    await interaction.response.send_message(f"hey, {interaction.user.name}, said: `{thing_to_say}`!")




@bot.tree.command(name="ping")
async def serverinfo(interaction: discord.Interaction):
    """FETCHES PING"""
    await interaction.response.send_message(f"Ping{bot.latency*1000:.2f}ms")




@bot.tree.command(name="serverinfo")
async def serverinfo(interaction: discord.Interaction):
    """FETCHES THE SERVER"""
    guild = interaction.guild
    embed = discord.Embed(title="Server information", description=guild.name, color=discord.Color.blue())
    thumbnail_url = guild.icon.url if guild.icon else discord.utils.MISSING
    embed.set_thumbnail(url=thumbnail_url)
    embed.add_field(name="Owner", value="cinnamon2191")
    embed.add_field(name="Member Count", value=guild.member_count, inline=False)
    await interaction.response.send_message(embed=embed, ephemeral=False)




@bot.command()
@commands.check(is_allowed_user)
async def excel_to_json(ctx):
    if len(ctx.message.attachments) == 0:
        await ctx.send("Please attach an Excel file to the command.")
        return

    attachment = ctx.message.attachments[0]
    if not attachment.filename.endswith('.xlsx'):
        await ctx.send("Please attach an Excel file with the '.xlsx' extension.")
        return

    try:
        # Download the Excel file
        await attachment.save(attachment.filename)

        # Read the Excel file into a pandas DataFrame
        df = pd.read_excel(attachment.filename)

        # Convert the DataFrame to a dictionary and save it as JSON
        json_filename = "data.json"
        df.to_json(json_filename, orient='records')

        await ctx.send("Data successfully converted and saved as JSON.")
    except Exception as e:
        await ctx.send(f"An error occurred while processing the Excel file: {e}")
    finally:
        # Clean up by removing the Excel file
        os.remove(attachment.filename)

def get_player_stats(governor_id):
    for player in data:
        if player["Governor ID"] == governor_id:
            return player
    return None



@bot.tree.command(name='governor')
@app_commands.describe(governor_id='The ID of the governor')
async def player_stats(interaction: discord.Interaction, governor_id: int):
    player = get_player_stats(governor_id)
    if player is None:
        await interaction.response.send_message(f"No player found with Governor ID {governor_id}")
    else:
        guild = interaction.guild
        embed = discord.Embed(title=f"{player['Name']}", description=f'ID {player["Governor ID"]} Date 20.07', color=discord.Color.red())
        embed.add_field(name="Stats", value=f"POWER: {format(player['Power'], ',')}\n"
                                            f"T4-KILLS: {format(player['T4-Kills'], ',')}\n"
                                            f"T5-KILLS: {format(player['T5-Kills'], ',')}\n"
                                            f"DEAD: {format(player['Dead troops'], ',')}\n"
                                            f"SCORE: {format(player['Score'], ',')}", inline=False)
        await interaction.response.send_message(embed=embed, ephemeral=False)



try:
    with open('linkme.json', 'r') as f:
        linkme_data = json.load(f)
except FileNotFoundError:
    linkme_data = {}


@bot.tree.command(name='linkme')
@app_commands.describe(governor_id='The ID of the governor')
async def linkme(interaction: discord.Interaction, governor_id: int):
    linkme_data[str(interaction.user.id)] = governor_id
    with open('linkme.json', 'w') as f:
        json.dump(linkme_data, f)
    await interaction.response.send_message(f"Linked Discord ID {interaction.user.id} with Governor ID {governor_id}")

@bot.tree.command(name='mystats')
async def stats(interaction: discord.Interaction):
    user_id = str(interaction.user.id)
    if user_id not in linkme_data:
        await interaction.response.send_message("You have not linked a Governor ID yet.")
        return

    governor_id = int(linkme_data[user_id])
    player = get_player_stats(governor_id)
    if player is None:
        await interaction.response.send_message(f"No player found with Governor ID {governor_id}")
    else:
        guild = interaction.guild
        embed = discord.Embed(title=f"{player['Name']}", description=f'ID {player["Governor ID"]}',
                              color=discord.Color.red())
        embed.add_field(name="Stats", value=f"POWER: {format(int(player['Power'].replace(' ', '')), ',')}\n"
                                            f"T4-KILLS: {format(int(player['T4-Kills']), ',')}\n"
                                            f"T5-KILLS: {format(int(player['T5-Kills']), ',')}\n"
                                            f"DEAD: {format(int(player['Dead troops']), ',')}\n"
                                            f"SCORE: {format(int(player['Score']), ',')}", inline=False)
        embed.add_field(name="Updated on 20.07", value='')
        await interaction.response.send_message(embed=embed, ephemeral=False)

if __name__ == '__main__':
    bot.run(TOKEN)