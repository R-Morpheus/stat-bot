import discord

from helpers import get_player
from main import bot
from discord import app_commands

@bot.tree.command(name='governor')
@app_commands.describe(governor_id='The ID of the governor')
async def player_stats(interaction: discord.Interaction, governor_id: int):
    [player, player_kvk] = get_player(governor_id, '../json/kvk1/data.json')

    if player | player_kvk is None:
        await interaction.response.defer()
        await interaction.followup.send(f"No player found with Governor ID {governor_id}.")
    else:
        embed = discord.Embed(title=f"{player['exactName']}", description=f'ID {player["Governor ID"]}', color=discord.Color.red())
        embed.add_field(name="Stats", value=f"POWER: {format(int(str(player['Power']).replace(' ', '')), ',')}\n"
                                            f"KP: {format(int(str(player['Kill Points']).replace(' ', '')), ',')}\n"
                                            , inline=False)

        embed.add_field(name="KVK STATS", value=f"RANK: {format(int(str(player_kvk['Rank']).replace(' ', '')), ',')}\n"
                                                f"T4-KILLS-GAINED: {format(int(t4_kills_kvk), ',')}\n"
                                                f"T5-KILLS-GAINED: {format(int(t5_kills_kvk), ',')}\n"
                                                f"DEAD TROOPS: {format(int(dead_troops), ',')}\n"
                                                f"SCORE: {format(int(player_kvk['Score']), ',')}\n", inline=False)

        await interaction.response.defer()
        await interaction.followup.send(embed=embed, ephemeral=False)

