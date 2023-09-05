import os
import discord
from discord import app_commands
from discord.ext import commands
import pandas as pd
import json
import logging
from dotenv import load_dotenv
from datetime import datetime



intents = discord.Intents.default()
intents.message_content = True

load_dotenv()

TOKEN = os.getenv("TOKEN")
EXCEL_ALLOWED_USER_ID_MORPHEY = 446232887214342144
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
async def excel(ctx):
    if len(ctx.message.attachments) == 0:
        await ctx.send("Please attach an Excel file to the command.")
        return

    attachment = ctx.message.attachments[0]
    if not attachment.filename.endswith('.xlsx'):
        await ctx.send("Please attach an Excel file with the '.xlsx' extension.")
        return

    try:
        # Download the Excel file
        file_path = os.path.join(os.getcwd(), attachment.filename)
        await attachment.save(file_path)

        # Read the Excel file into a dictionary of pandas DataFrames
        dfs = pd.read_excel(file_path, sheet_name=None)

        # Convert the dictionary of DataFrames to a dictionary of dictionaries and save it as JSON
        dict_of_dicts = {sheet: df.to_dict(orient='records') for sheet, df in dfs.items()}
        json_filename = "data.json"
        with open(json_filename, 'w') as f:
            json.dump(dict_of_dicts, f, indent=4, sort_keys=True)

        await ctx.send("Data successfully converted and saved as JSON.")
    except Exception as e:
        await ctx.send(f"An error occurred while processing the Excel file: {e}")
    finally:
        # Clean up by removing the Excel file
        if os.path.exists(file_path):
            os.remove(file_path)


def get_player_stats(governor_id):
    # Load the data from the JSON file
    with open('data.json', 'r') as f:
        data = json.load(f)

    for player in data['29Aug23-20h19m']:
        if player["Governor ID"] == governor_id:
            return player
    return None

def get_player_stats_kvk(governor_id):
    # Load the data from the JSON file
    with open('data.json', 'r') as f:
        data = json.load(f)

    for player in data['KVK ']:
        if player["Governor ID"] == governor_id:
            return player
    return None
# def get_player_stats_zone_6(governor_id):
#     # Load the data from the JSON file
#     with open('data.json', 'r') as f:
#         data = json.load(f)
#
#     for player in data['score War zone 6']:
#         if player["Governor ID"] == governor_id:
#             return player
#     return None


@bot.tree.command(name='governor')
@app_commands.describe(governor_id='The ID of the governor')
async def player_stats(interaction: discord.Interaction, governor_id: int):
    player = get_player_stats(governor_id)
    player_kvk = get_player_stats_kvk(governor_id)

    if player_kvk is None:
        await interaction.response.send_message(f"No player KVK stats found with Governor ID {governor_id}")
        return

    t4_kills_kvk = player_kvk.get('T4-Kills-gained-kvk', 0)
    t5_kills_kvk = player_kvk.get('T5-Kills-gained-kvk', 0)
    dead_troops = dead_troops_gained_kvk = player_kvk.get('Dead-troops-gained-kvk', 0)

    if player is None:
        await interaction.response.defer()
        await interaction.followup.send(f"No player found with Governor ID {governor_id}.")
    else:
        guild = interaction.guild
        embed = discord.Embed(title=f"{player['exactName']}", description=f'ID {player["Governor ID"]}', color=discord.Color.red())
        embed.add_field(name="Stats", value=f"POWER: {format(int(str(player['Power']).replace(' ', '')), ',')}\n"
                                            f"KP: {format(int(str(player['Kill Points']).replace(' ', '')), ',')}\n"
                                            , inline=False)
        embed.add_field(name="L7 STATS", value= f"T4-KILLS-GAINED: {format(int(player_kvk['T4-Kills-L7']), ',')}\n"
                                                f"T5-KILLS-GAINED: {format(int(player_kvk['T5-Kills-L7']), ',')}\n"
                                                f"DEAD TROOPS: {format(int(player_kvk['Dead Troops-L7']), ',')}\n"
                                                , inline=False)

        embed.add_field(name="KVK STATS", value=f"RANK: {format(int(str(player_kvk['Rank']).replace(' ', '')), ',')}\n"
                                                f"T4-KILLS-GAINED: {format(int(t4_kills_kvk), ',')}\n"
                                                f"T5-KILLS-GAINED: {format(int(t5_kills_kvk), ',')}\n"
                                                f"DEAD TROOPS: {format(int(dead_troops), ',')}\n"
                                                f"SCORE: {format(int(player_kvk['Score']), ',')}\n", inline=False)

        await interaction.response.defer()
        await interaction.followup.send(embed=embed, ephemeral=False)



try:
    with open('old/linkme_old.json', 'r') as f:
        linkme_data = json.load(f)
except FileNotFoundError:
    linkme_data = {}


def format_date(date_string):
    # Convert the date string to a datetime object
    date_time_obj = datetime.strptime(date_string, "%d%b%y-%Hh")

    # Format the datetime object to the desired format
    formatted_date = date_time_obj.strftime("%d.%m %H:%M")

    return formatted_date


@bot.tree.command(name='linkme')
@app_commands.describe(governor_id='The ID of the governor')
async def linkme(interaction: discord.Interaction, governor_id: int):
    linkme_data[str(interaction.user.id)] = governor_id
    with open('old/linkme_old.json', 'w') as f:
        json.dump(linkme_data, f)
    await interaction.response.send_message(f"Linked Discord ID {interaction.user.id} with Governor ID {governor_id}")

@bot.tree.command(name='mystats')
async def stats(interaction: discord.Interaction):
    user_id = str(interaction.user.id)
    if user_id not in linkme_data:
        await interaction.response.defer()
        await interaction.followup.send("You have not linked a Governor ID yet. Please write /linkme")
        return

    governor_id = int(linkme_data[user_id])
    player = get_player_stats(governor_id)
    player_kvk = get_player_stats_kvk(governor_id)

    if player_kvk is None:
        await interaction.response.send_message(f"No player KVK stats found with Governor ID {governor_id}")
        return

    t4_kills_kvk = player_kvk.get('T4-Kills-gained', 0)
    t5_kills_kvk = player_kvk.get('T5-Kills-gained', 0)
    dead_troops = player_kvk.get('Dead-troops-gained', 0)

    if player is None:
        await interaction.response.send_message(f"No player found with Governor ID {governor_id}")
    else:
        guild = interaction.guild
        embed = discord.Embed(title=f"{player['exactName']}", description=f'ID {player["Governor ID"]}',
                              color=discord.Color.red())
        embed.add_field(name="Stats", value=f"POWER: {format(int(str(player['Power']).replace(' ', '')), ',')}\n"
                                            f"KP: {format(int(str(player['Kill Points']).replace(' ', '')), ',')}\n"
                                            f"Dead Troops: {format(int(str(player['Dead Troops']).replace(' ', '')), ',')}\n"
                                            , inline=False)

        embed.add_field(name="L7 STATS", value= f"T4-KILLS-GAINED: {format(int(player_kvk['T4-Kills-L7']), ',')}\n"
                                                f"T5-KILLS-GAINED: {format(int(player_kvk['T5-Kills-L7']), ',')}\n"
                                                f"DEAD TROOPS: {format(int(player_kvk['Dead Troops-L7']), ',')}\n"
                                                , inline=False)

        embed.add_field(name="KVK STATS", value=f"RANK: {format(int(str(player_kvk['Rank']).replace(' ', '')), ',')}\n"
                                                f"T4-KILLS-GAINED: {format(int(t4_kills_kvk), ',')}\n"
                                                f"T5-KILLS-GAINED: {format(int(t5_kills_kvk), ',')}\n"
                                                f"DEAD TROOPS: {format(int(dead_troops), ',')}\n"
                                                f"SCORE: {format(int(player_kvk['Score']), ',')}\n", inline=False)

        await interaction.response.defer()
        await interaction.followup.send(embed=embed, ephemeral=False)


@bot.tree.command(name='top10')
async def top10(interaction: discord.Interaction):
    # Load the data from the JSON file
    with open('data.json', 'r') as f:
        data = json.load(f)

    # Get the data from the specific sheet
    data_sheet = data['KVK ']

    # Filter out records without the "Rank" field
    data_with_rank = [record for record in data_sheet if "Rank" in record]

    # Sort the data by rank
    sorted_data = sorted(data_with_rank, key=lambda k: int(k["Rank"]))

    # Create an embed message
    embed = discord.Embed(title="Top 15 Players", color=discord.Color.red())


    # Loop through the top 10 players
    for i, player in enumerate(sorted_data[:15]):
        embed.add_field(name=f"Rank #{i+1}", value=f"Player: {player['Name']}\n"
                                                   f"T4-KILLS-GAINED: {format(int(player['T4-Kills-gained']), ',')}\n"
                                                   f"T5-KILLS-GAINED: {format(int(player['T5-Kills-gained']), ',')}\n"
                                                   f"DEAD TROOPS: {format(int(player['Dead-troops-gained']), ',')}\n"
                                                   f"SCORE: {format(int(player['Score']), ',')}\n", inline=False)
    await interaction.response.defer()
    await interaction.followup.send(embed=embed, ephemeral=False)



if __name__ == '__main__':
    bot.run(TOKEN)