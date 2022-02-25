import os
import discord
import numpy as np
import schedule
import sys
import subprocess
from AVL import AVLTree
from SQL import load_stored_data,update_user_data,insert_user_data,database_cleanup

# Help(instructions) commands
dhelp={'dregras','dRegras','dHelp','dhelp'}

# Binary tree with user_data
users_tree = AVLTree()

# Database
DATABASE_URL = os.environ['DATABASE_URL']

# Schedule Maintenance
def maintenance():
  subprocess.call([sys.executable, os.path.realpath(__file__)] +
sys.argv[1:])

schedule.every(180).days.do(maintenance)

class MyClient(discord.Client):

    # Bot startup procedure
    async def on_ready(self):
      print('Logged on as {0}!'.format(self.user))
      database_cleanup(DATABASE_URL)
      load_stored_data(DATABASE_URL,users_tree)

    # Bot process commands when receives messages
    async def on_message(self, message):
        print('Message from {0.author}: {0.content}'.format(message))

        # Help Command
        if message.content in dhelp:
          #print(clientuser.locale)
          await message.channel.send(f"{message.author.name}, digite o dado que deseja jogar Ex: d12")
          return

        # Main_Output
        inp=message.content
        inp=inp.split('+')
        inp=[value for value in inp if value != '']
      
        if len(inp)>1:
          output=0
          output_list=[]
          for i in inp:
            if len(message.content)>=2 and i[0]=="d":
              a=i
              a=a.replace('d','')
              try: # try transforming into an int
                a=int(a)
                rand=np.random.randint(1,a+1)
                output+=rand
                output_list.append(rand)
              except:
                break
      
            elif len(i)>=3 and i[1]=="d":
              try:
                a=int(i[0])
                b=i
                aux=(i[0])
                
                b=b.replace(aux,'',1)
                b=b.replace('d','')
                b=int(b)
      
                dices=[]
      
                for i in range(a):
                  dices.append(np.random.randint(1,b+1))
      
                output+=sum(dices)
                output_list=output_list+dices
      
              except:
                break
      
          if output!=0:
            await message.channel.send(f"Os dados foram: {output_list} com total: {output}")
      
            user_data=users_tree.search(message.author.name)
      
            if user_data==None:
              users_tree.insert(message.author.name)
              user_data=users_tree.search(message.author.name)
              user_data.total_dice=output
              insert_user_data(DATABASE_URL,message,output)
            else:
              user_data.total_dice=output
              update_user_data(DATABASE_URL,message,output)
            
        else:
      
          if len(message.content)>=2 and message.content[0]=="d":
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
                insert_user_data(DATABASE_URL,message,rand)
              else:
                user_data.total_dice=rand
                update_user_data(DATABASE_URL,message,rand)
      
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
                await message.channel.send(f"{user_data.total_dice-rand}+{rand}={user_data.total_dice}")
                insert_user_data(DATABASE_URL,message,rand)
              else:
                user_data.total_dice+=rand
                await message.channel.send(f"{user_data.total_dice-rand}+{rand}={user_data.total_dice}")
                update_user_data(DATABASE_URL,message,user_data.total_dice)
      
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
                insert_user_data(DATABASE_URL,message,total)
              else:
                user_data.total_dice=total
                update_user_data(DATABASE_URL,message,total)
      
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
                await message.channel.send(f"{user_data.total_dice-total} + os dados: {dices} = {user_data.total_dice}")
                insert_user_data(DATABASE_URL,message,total)
              else:
                user_data.total_dice+=total
                await message.channel.send(f"{user_data.total_dice-total} + os dados: {dices} = {user_data.total_dice}")
                update_user_data(DATABASE_URL,message,user_data.total_dice)

            except:
              pass
          
          else: # Only trigged when no command was sent to the bot
            # Schedule Verification
            schedule.run_pending()

intents=discord.Intents.default()
intents.members=True

client = MyClient(intents=intents)

# Bot token - private
client.run(os.environ['DISCORD_TOKEN'])