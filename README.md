Discord Bot

This project is a Discord bot developed in Python using the discord.py library. The bot provides a set of commands that allow interaction with Discord server members as well as processing data from Excel files and storing them in JSON format.

Key Features

1.Responding to greeting commands and providing server information.

2.Fetching player statistics by their Governor ID.

3.Linking a Discord user's ID to a game player's ID.

4.Converting data from Excel files to JSON format.

4.Logging of executed commands.

5.Protecting the Excel processing command with a permissions system.



Installation and Running


First of all, make sure you have Python 3.8 or higher installed.

Install the required dependencies:

`pip install discord.py python-dotenv pandas openpyxl`

In the root directory of the project, create a .env file with the following content:

`TOKEN=your_bot_token`
`EXCEL_ALLOWED_USER_ID=user_id_for_excel_processing`

Run the bot with the command:

`python bot.py`

Usage
After the bot is up and connected to your Discord server, you can use its commands. Here are some of them:

`/hello`: A greeting command.

`/say`: Makes the bot echo your message.

`/ping`: Gets the bot's ping latency.

`/serverinfo`: Fetches server information.

`/governor`: Fetches a player's statistics by the Governor ID.

`/linkme`: Links a Discord user's ID to a Governor ID.

`/mystats`: Fetches a linked player's statistics based on your Discord user ID.


Warnings

The bot is intended for educational purposes and should not be used for commercial purposes without further validation and testing.
Do not divulge your bot's token. This is sensitive data that can be used to control your bot. If you accidentally published your token, invalidate it immediately in your bot's settings on the Discord Developer Portal.
The bot uses a linkme.json file to store links between Discord user IDs and Governor IDs. This file should be kept secure and backed up regularly.


License

This project is licensed under the MIT license. Details can be found in the LICENSE file.
