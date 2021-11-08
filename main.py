import discord
import numpy as np

# Help(instructions) commands
dhelp={'dregras','dRegras','dHelp','dhelp'}

# Possible dice commands
ddados={'d4','d6','d8','d10','d12','d20','d100'}

class MyClient(discord.Client):
    async def on_ready(self):
        print('Logged on as {0}!'.format(self.user))

    async def on_message(self, message):
        print('Message from {0.author}: {0.content}'.format(message))
        if message.content in dhelp:
          await message.channel.send(f"{message.author.name}, digite o dado que deseja jogar Ex: d12")
        elif message.content in ddados:
          a=message.content
          a=a.replace('d','')
          a=int(a)
          await message.channel.send(f"{np.random.randint(1,a+1)}")


intents=discord.Intents.default()
intents.members=True

client = MyClient(intents=intents)

# Bot token
client.run('OTAyNjk2MzM1OTYxMTIwNzg5.YXiLeQ.HDVdmGVuU6Y0HYXJ3MxGjdhLZYs')