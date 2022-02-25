import psycopg2
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
  cursor.execute(f"UPDATE dBotRPG_data SET total_dice = {dice} WHERE user_name = '{message.author.name}';")
  conn.commit()
  cursor.close()
  conn.close()

def insert_user_data():
  return