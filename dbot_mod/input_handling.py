from functions import help,checkMessageCommand,suggestBehaviorCommand,error

# Help(instructions) commands
dhelp={'dregras','dRegras','dHelp','dhelp'}

# Help(instructions) commands
dmod={'dmod','dMod'}

def user_input(message, mongoDB):

  if(message.content in dhelp):
    return help(message)

  if(message.content in dmod):
    return suggestBehaviorCommand(message, mongoDB)
    
  else:
    return checkMessageCommand(message, mongoDB)