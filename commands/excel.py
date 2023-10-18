import json
import os
import pandas as pd
from config import EXCEL_ALLOWED_USER_ID_MORPHEY
from main import bot
from discord.ext import commands


def is_allowed_user(ctx):
    return ctx.author.id == EXCEL_ALLOWED_USER_ID_MORPHEY


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
        json_filename = "json/kvk1/data.json"
        with open(json_filename, 'w') as f:
            json.dump(dict_of_dicts, f, indent=4, sort_keys=True)

        await ctx.send("Data successfully converted and saved as JSON.")
    except Exception as e:
        await ctx.send(f"An error occurred while processing the Excel file: {e}")
    finally:
        # Clean up by removing the Excel file
        if os.path.exists(file_path):
            os.remove(file_path)

