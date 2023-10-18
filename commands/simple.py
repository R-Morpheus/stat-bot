import discord

from main import bot


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

