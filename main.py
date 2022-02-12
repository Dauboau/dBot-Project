import os
import discord
import numpy as np

# Help(instructions) commands
dhelp={'dregras','dRegras','dHelp','dhelp'}

class MyClient(discord.Client):
    async def on_ready(self):
        print('Logged on as {0}!'.format(self.user))

    async def on_message(self, message):
        print('Message from {0.author}: {0.content}'.format(message))
        if message.content in dhelp:
          await message.channel.send(f"{message.author.name}, digite o dado que deseja jogar Ex: d12")

        elif message.content[0]=="d":
          a=message.content
          a=a.replace('d','')
          try: # try transforming into an int
            a=int(a)
            await message.channel.send(f"{np.random.randint(1,a+1)}")
          except: # if it fails,
            pass # it does not do anything

        elif message.content[0]=="+":
          b=message.content
          b=b.replace('+','')
          try:
            b=int(b)
            await message.channel.send(f"{np.random.randint(1,b+1)+a}")
          except:
            pass


intents=discord.Intents.default()
intents.members=True

client = MyClient(intents=intents)

# Bot token - private
client.run(os.environ['DISCORD_TOKEN'])
