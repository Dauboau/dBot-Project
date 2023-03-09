from functions import help,rollDiceCommand,sumDiceCommand,error

# Help(instructions) commands
dhelp={'dregras','dRegras','dHelp','dhelp'}

def user_input(message):

  if(message.content in dhelp):
    return help(message)

  if(message.content.find('d') != -1):
    
    if(message.content[0] == '+'):
      return sumDiceCommand(message)

    else:
      return rollDiceCommand(message)
    
  else:
    return error()