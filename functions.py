import numpy as np

def help(message,dhelp):
  if message.content in dhelp:
    return (f"{message.author.name}, digite o dado que deseja jogar Ex: d12")


def main_output(message,users_tree):
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
      return (f"Os dados foram: {output_list} com total: {output}")

      user_data=users_tree.search(message.author.name)

      if user_data==None:
        users_tree.insert(message.author.name)
        user_data=users_tree.search(message.author.name)
        user_data.total_dice=output
      else:
        user_data.total_dice=output
      
  else:

    if len(message.content)>=2 and message.content[0]=="d":
      a=message.content
      a=a.replace('d','')
      try: # try transforming into an int
        a=int(a)
        rand=np.random.randint(1,a+1)
        return (f"{rand}")

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

        return (f"{user_data.total_dice-rand}+{rand}={user_data.total_dice}")

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

        return (f"Os dados foram: {dices} com total: {total}")

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

        return (f"{user_data.total_dice-total} + os dados: {dices} = {user_data.total_dice}")

      except:
        pass