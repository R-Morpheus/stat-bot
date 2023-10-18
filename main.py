import logging
import discord
from discord.ext import commands
import config

intents = discord.Intents.default()
intents.message_content = True


# Setup the logger
logging.basicConfig(level=logging.INFO, format='%(asctime)s %(message)s')


async def log_command(interaction):
    logging.info(f'User {interaction.user.name} ({interaction.user.id}) executed command {interaction.command_name}')


bot = commands.Bot(command_prefix='.', intents=intents)

# Загружаем расширения (коги)
for extension in config.extensions:
    bot.load_extension(extension)

if __name__ == '__main__':
    bot.run(config.TOKEN)
