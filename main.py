import discord
import numpy as np

dhelp={'dregras','dRegras','dHelp','dhelp'} #legal
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
client.run('OTAyNjk2MzM1OTYxMTIwNzg5.YXiLeQ.qRPEdADXaTr1ip1ejCnriVMdTF4')

#async def on_message(self, message): recebe a mensagem (message) com o nome do autor, e o conteudo ...


# await.message.channel.send //envia no canal
# await.message.author.send // envia no pessoal