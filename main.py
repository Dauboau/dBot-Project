import os
import discord
from AVL import AVLTree
from SQL import load_stored_data
from functions import main_output,help

# Help(instructions) commands
dhelp={'dregras','dRegras','dHelp','dhelp'}

# Binary tree with user_data
users_tree = AVLTree()

# Database
DATABASE_URL = os.environ['DATABASE_URL']

class MyClient(discord.Client):
    async def on_ready(self):
      print('Logged on as {0}!'.format(self.user))
      load_stored_data(DATABASE_URL,users_tree)

    async def on_message(self, message):
        print('Message from {0.author}: {0.content}'.format(message))
      
        try:
          await message.channel.send(help(message,dhelp))
          return
        except:
          pass

        try:
          await message.channel.send(main_output(message, users_tree))
          return
        except:
          pass

intents=discord.Intents.default()
intents.members=True

client = MyClient(intents=intents)

# Bot token - private
client.run(os.environ['DISCORD_TOKEN'])