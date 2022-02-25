import psycopg2
from datetime import date
from AVL import *

def load_stored_data(DATABASE_URL,users_tree):
  conn = psycopg2.connect(DATABASE_URL, sslmode='require')
  cursor = conn.cursor()
  
  cursor.execute("SELECT user_name, total_dice FROM dBotRPG_data ORDER BY user_name;")
  
  row = cursor.fetchall()
  
  for i in range(len(row)):
    users_tree.insert(row[i][0])
    user_data=users_tree.search(row[i][0])
    user_data.total_dice=row[i][1]
    
  cursor.close()
  conn.close()

def update_user_data(DATABASE_URL,message,dice):
  conn = psycopg2.connect(DATABASE_URL, sslmode='require')
  cursor = conn.cursor()
  
  cursor.execute(f"UPDATE dBotRPG_data SET total_dice = {dice},last_usage_date = '{date.today().month}-{date.today().day}-{date.today().year}' WHERE user_name = '{message.author.name}';")
  # Month-Day-Year
  
  conn.commit()
  cursor.close()
  conn.close()

def insert_user_data(DATABASE_URL,message,dice):
  conn = psycopg2.connect(DATABASE_URL, sslmode='require')
  cursor = conn.cursor()
  
  cursor.execute(f"insert into dBotRPG_data(user_name,total_dice) values ('{message.author.name}',{dice});")
  
  conn.commit()
  cursor.close()
  conn.close()
  
  return

def database_cleanup(DATABASE_URL):
  conn = psycopg2.connect(DATABASE_URL, sslmode='require')
  cursor = conn.cursor()

  cursor.execute("SELECT last_usage_date,user_name FROM dBotRPG_data ORDER BY last_usage_date;")

  row = cursor.fetchall()

  for i in range(len(row)):
    last_usage=row[i][0]
    if(age_in_days(last_usage)>=30): # The data is stored for 30 days until it is deleted from storage
      try:
        cursor.execute(f"delete from dBotRPG_data where last_usage_date='{last_usage}';")
      except:
        pass
    else:
      break

  conn.commit()
  cursor.close()
  conn.close()

def age_in_days(creation_date):
  
  actual_date = date.today()

  time_difference = actual_date - creation_date
  age = time_difference.days

  return age
