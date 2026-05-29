import os
import discord
import asyncio
from input_handling import user_input

class MyClient(discord.Client):

    # Bot startup procedure
    async def on_ready(self):
      print('Logged on as {0}!'.format(self.user))

    # Bot process commands when receives messages
    async def on_message(self, message):

        # Igores messages from any bots
        if(message.author.bot == True):
          return
      
        print('Message from {0.author}:{0.content}'.format(message))

        output = await asyncio.to_thread(user_input, message)

        if(output is not None and len(output)>0):
          await message.channel.send(output)

intents=discord.Intents.all()
intents.members=True

client = MyClient(intents=intents)

# Bot token - private
client.run(os.environ['DISCORD_TOKEN_DBOTRPG'])