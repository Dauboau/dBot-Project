import os
import discord
import numpy as np
from AVL import *

# Help(instructions) commands
dhelp={'dregras','dRegras','dHelp','dhelp'}
users_tree = AVLTree()

class MyClient(discord.Client):
    async def on_ready(self):
        print('Logged on as {0}!'.format(self.user))

    async def on_message(self, message):
        print('Message from {0.author}: {0.content}'.format(message))
        if message.content in dhelp:
          await message.channel.send(f"{message.author.name}, digite o dado que deseja jogar Ex: d12")

        elif len(message.content)>=2 and message.content[0]=="d":
          a=message.content
          a=a.replace('d','')
          try: # try transforming into an int
            a=int(a)
            rand=np.random.randint(1,a+1)
            await message.channel.send(f"{rand}")

            user_data=users_tree.search(message.author.name)
            
            if user_data==None:
              users_tree.insert(message.author.name)
              user_data=users_tree.search(message.author.name)
              user_data.total_dice=rand
            else:
              user_data.total_dice=rand

          except: # if it fails,
            pass # it does not do anything

        elif len(message.content)>=3 and message.content[0]=="+" and message.content[1]=="d":
          a=message.content
          a=a.replace('+','')
          a=a.replace('d','')
          try:
            a=int(a)
            
            rand=np.random.randint(1,a+1)

            user_data=users_tree.search(message.author.name)

            if user_data==None:
              users_tree.insert(message.author.name)
              user_data=users_tree.search(message.author.name)
              user_data.total_dice=rand
            else:
              user_data.total_dice+=rand

            await message.channel.send(f"{user_data.total_dice-rand}+{rand}={user_data.total_dice}")

          except:
            pass

        elif len(message.content)>=3 and message.content[1]=="d":
          try:
            a=int(message.content[0])
            b=message.content
            aux=(message.content[0])
            
            b=b.replace(aux,'',1)
            b=b.replace('d','')
            b=int(b)

            dices=[]

            for i in range(a):
              dices.append(np.random.randint(1,b+1))

            total=sum(dices)

            await message.channel.send(f"Os dados foram: {dices} com total: {total}")

            user_data=users_tree.search(message.author.name)
            
            if user_data==None:
              users_tree.insert(message.author.name)
              user_data=users_tree.search(message.author.name)
              user_data.total_dice=total
            else:
              user_data.total_dice=total

          except:
            pass

        elif len(message.content)>=4 and message.content[0]=="+" and message.content[2]=="d":
          try:
            a=int(message.content[1])
            b=message.content
            aux=(message.content[1])
            
            b=b.replace('+','')
            b=b.replace(aux,'',1)
            b=b.replace('d','')
            b=int(b)

            print(a,b)

            dices=[]

            for i in range(a):
              dices.append(np.random.randint(1,b+1))

            total=sum(dices)

            user_data=users_tree.search(message.author.name)

            if user_data==None:
              users_tree.insert(message.author.name)
              user_data=users_tree.search(message.author.name)
              user_data.total_dice=total
            else:
              user_data.total_dice+=total

            await message.channel.send(f"{user_data.total_dice-total} + os dados: {dices} = {user_data.total_dice}")

          except:
            pass


intents=discord.Intents.default()
intents.members=True

client = MyClient(intents=intents)

# Bot token - private
client.run(os.environ['DISCORD_TOKEN'])
