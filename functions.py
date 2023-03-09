import numpy as np
from hash import hash

# standart error output
def error():
  return ""

def help(message):

  output = (f"{message.author.name}, Type the dice you would like to roll. Ex: d12 or 3d20. Maybe use +d20 or +6d10 to add more dice to the ones you have already rolled or roll many different dice at the same time doing something like d10+2d20+d100.")

  return output

# Rolar um dado
def rollDice(dadoStr):

  try:
  
    parts = dadoStr.split('d')

    #print(parts)
    
    if(parts[0]==''):
      parts[0]="1"

    if(parts[1]==''):
      return -1
    
    result = []

    for i in range(int(parts[0])):
      result.append(np.random.randint(1,int(parts[1])+1))
    
    return result

  except:
    return -1

# Rolar vários dados
def rollDiceCommand(message):

  try:
  
    parts = message.content.split('+')

    #print(parts)
    
    dices=[]
  
    for part in parts:
      part = part.strip()
      
      result = rollDice(part)
      
      if(result==-1):
        raise Exception("Error Rolling Dice")
        
      dices += result
      
    hash[message.author.id] = sum(dices)
    
    return f"Os dados foram: {dices} com total: {sum(dices)}"

  except:
    return error()

def sumDiceCommand(message):

  try:
  
    parts = message.content.split('+')
    parts=parts[1:]

    #print(parts)
    
    dices=[]
  
    for part in parts:
      part = part.strip()
      
      result = rollDice(part)
      
      if(result==-1):
        raise Exception("Error Rolling Dice")
        
      dices += result

    # returns 0 if there the key is not found
    savedValue = hash.get(message.author.id,0)
    
    hash[message.author.id] = savedValue + sum(dices)
    
    return f"{savedValue} + os dados: {dices} = {hash[message.author.id]}"

  except:
    return error()