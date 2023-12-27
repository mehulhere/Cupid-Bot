# import discord
# import os
# import numpy as np

# intents = discord.Intents().all()
# intents.message_content = True
# client = discord.Client(intents=intents)

# database = np.load("database.npy", allow_pickle=True)
# database = database.tolist()

# def findindex(user_id):
#   count = -1
#   for i in database:
#     count += 1
#     if i[0] == user_id:
#       return count
#   else:
#     return False

# @client.event
# async def on_ready():
#   print("Ready for launch. I am {0.user}".format(client))

# async def dm(user_id):
#   user = client.get_user(int(user_id))
#   await user.send(f'You can now talk to user00{database[findindex(user_id)][2]} by typing messages here. You can use !stop to end the chat. Say !hello to cupid for finding a new match.')
  
# @client.event
# async def on_message(message):
#   if message.author == client.user:
#     return
#     # Get data about the user
#   user_message = str(message.content)
#   if user_message:
#     username = str(message.author)
#     channels = str(message.channel)
#     user_id = message.author.id
#     # Debug printing
#     print(f"{username} said: '{user_message}' ({channels})")
#     # Send messages
# client.run(os.getenv('tokenmbd'))
