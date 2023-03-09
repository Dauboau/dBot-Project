import os
import discord
from input_handling import user_input

# Help(instructions) commands
dhelp={'dregras','dRegras','dHelp','dhelp'}

class MyClient(discord.Client):

    # Bot startup procedure
    async def on_ready(self):
      print('Logged on as {0}!'.format(self.user))

    # Bot process commands when receives messages
    async def on_message(self, message):

        # Ignora mensagens do bot
        if(message.author.id == 902696335961120789):
          return
      
        print('Message from {0.author}:{0.content}'.format(message))

        output = user_input(message)

        if(len(output)>0):
          await message.channel.send(output)

intents=discord.Intents.all()
intents.members=True

client = MyClient(intents=intents)

# Bot token - private
client.run(os.environ['DISCORD_TOKEN'])