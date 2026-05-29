import discord
import numpy as np
from pymongo import ReturnDocument
from classes import Guild, Moderation
from database import MongoDB
from hash import hash
import textwrap
from pymongo.collection import Collection
from datetime import datetime, timedelta, timezone

from genAI import checkGenAI, shouldModerateGenAI,suggestGenAI

def error():
  '''Standard error message.'''
  return ""

def help(message):
  '''Returns the help message for the bot.'''

  output = (f"{message.author.name}, Just keep chatting normally and I will analyze your messages in order to keep you and the server safe.")

  return output

def checkMessageCommand(message:discord.Message, mongoDB:MongoDB):
  '''Registers each incoming message in the server’s history and performs automatic behavior analysis using GenAI.'''

  try:

    guild = mongoDB.guild_table.find_one_and_update(
        {"_id": str(message.guild.id)},
        {
            "$setOnInsert": {
                "name": message.guild.name,
                "moderating_hystory":[]
            },
            "$push": {
                "message_hystory": {
                    "author_id": str(message.author.id),
                    "author_name": message.author.name,
                    "content": message.content,
                    "created_at": message.created_at
                }
            }
        },
        upsert=True,
        return_document=ReturnDocument.AFTER
    )

    # Keeps the last 20 messages in the history
    # and the last 5 moderating history messages
    # and removes the rest, updating the moderating history accordingly
    if len(guild["message_hystory"]) > 32:
      mongoDB.guild_table.update_one(
        {"_id": str(message.guild.id)},
        [
          {"$set": {
            "message_hystory": {
              "$slice": ["$message_hystory", -20]
            },
            "moderating_hystory": {
              "$slice": ["$moderating_hystory", -5]
            }
          }}
        ]
      )
    
    # Analyses the server messages every 4 messages
    elif len(guild["message_hystory"]) % 4 == 0:

      # analyze the last 12 messages
      messages = guild["message_hystory"][-12:]

      # Filter messages from the last 15 minutes
      now = datetime.now()
      five_minutes_ago = now - timedelta(minutes=15)
      messages = [msg for msg in messages if msg["created_at"] >= five_minutes_ago]

      print(len(messages), "Mensagens do servidor:", message.guild.name, "sendo analisadas")

      data = checkGenAI(messages)

      output = data["choices"][0]["message"]["content"].split("|")
      print(output)

      if len(output) != 6 or output[0][-1:] not in ["0", "1"]:
        return error()

      badBehavior = output[0][-1:] # 0 or 1
      problem = output[1] # None or Problem
      bad_user = output[2] # None or User ID
      suggestion = output[3] # None or Suggestion
      critical = output[4] # Yes or No
      adminInstructions = output[5] # None or AdminInstructions

      if badBehavior == "1":

        moderation:Moderation = Moderation()
        moderation.bad_author_id=bad_user
        moderation.problem=problem
        moderation.moderated_at=datetime.now()

        data = shouldModerateGenAI(moderation,guild["moderating_hystory"])
        output = data["choices"][0]["message"]["content"]
        print(output)

        # If the output is "False", it means that the user should not be moderated
        if output == "False":
          return ""

        mongoDB.guild_table.update_one(
          {"_id": str(message.guild.id)},
          {"$push": {
              "moderating_hystory": {
                  "bad_author_id": moderation.bad_author_id,
                  "problem": moderation.problem,
                  "moderated_at": moderation.moderated_at
              }
          }}
        )

      if badBehavior == "1" and critical == "No":
        return textwrap.dedent(f"""
          **User:** <@{bad_user}>
          **Problem:** {problem}
          **Suggestion:** {suggestion}
        """)
      
      elif badBehavior == "1" and critical == "Yes":
        return textwrap.dedent(f"""
          **User:** <@{bad_user}>
          **Problem:** {problem}
          **Required Action:** {adminInstructions}
        """)

      elif badBehavior == "0":
        print("Nenhum problema encontrado nas mensagens do servidor:", message.guild.name)
        return ""
      
      else:
        print("Erro na análise das mensagens do servidor:", message.guild.name)
        return error()
    
    else:
      return error()

  except Exception as e:
    print(e)
    return error()

def suggestBehaviorCommand(message:discord.Message, mongoDB:MongoDB):
  '''Analyzes the user’s behavior and suggests changes based on the server’s message history using GenAI.'''

  try:

    guild = mongoDB.guild_table.find_one(
        {"_id": str(message.guild.id)}
    )

    if len(guild["message_hystory"]) >= 10:

      print("Comportamento do usuario: ", message.author.name, " no servidor: ", message.guild.name," sendo analisado")

      user = message.author.name
      messages = guild["message_hystory"][-20:] # analyze the last 20 messages
      data = suggestGenAI(user,messages)

      output = data["choices"][0]["message"]["content"].split("|")
      print(output)

      if(len(output) == 2):
        Analysis = output[0]
        Suggestions = output[1]
        print("Comportamento do usuario: ", message.author.name, " no servidor: ", message.guild.name," analisado")
        return textwrap.dedent(f"""
          **User:** {message.author.mention}
          **Analysis:** {Analysis}
          **Suggestions:** {Suggestions}
        """)
        
      else:
        print("Erro na análise do usuario: ", message.author.name, " no servidor: ", message.guild.name)
        return error()
      
    else:
      return "Not enough context to analyze the behavior."

  except Exception as e:
    print(e)
    return error()