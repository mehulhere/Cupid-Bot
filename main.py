import discord
import os
import responses
import json

# Future Changelogs:
# better UI-stickers, emojis

# !feedback- save
# action on reports
# ice-breaking games

emojilist = ['🎮', '🅰️', '♟️', '🎵', '📸', '⛹️'] #all interest emoji's
gender=['🧑','👸','🌈','🧑‍🤝‍🧑']
numgender=['1️⃣','2️⃣','3️⃣']
tickwrong=['✅','❎']
ticktok=['☑️','❌']
intents = discord.Intents().all()
intents.message_content = True
client = discord.Client(intents=intents)
with open("database.json", "r") as f:
    database = json.load(f)
#dictionary={userid:[gender, emoji, matchid,sno]}
print(database)


# Function to add emojis from emojilist
async def add_emojis(message, emojilist):
    for emoji in emojilist:
        await message.add_reaction(emoji)

# Function to handle gender
async def handle_my_sex_message(message):
  if message.content.startswith("My Sex"):
      await add_emojis(message, numgender)

# Function to handle gender of interest
async def handle_chat_with_message(message):
  if message.content.startswith("Chat with"):
      await add_emojis(message, gender)

# Function to handle repeated match settting 
async def handle_repeated_match_message(message):
  if message.content.startswith("Repeated Match"):
      await add_emojis(message, tickwrong)

# Function to handle interests
async def handle_choose_5_from_message(message):
  if message.content.startswith("Choose any 5 from"):
      await add_emojis(message, emojilist)

# Function to handle "reveal identity" message
async def handle_reveal_identity_message(message):
  if "wants to reveal their identity. Do you want to reveal your identity? - Cupid" in message.content:
      await add_emojis(message, ticktok)


#handles "!register" response
async def handle_register_message(message,user_id):
  await message.channel.send(message.author.mention + " You are registered for Blind Dating💍, check your dm.")
  database[str(user_id)]=[None, None, None, len(database)+1, None]
  save(database)
  await send_message(message, "!register", is_private=True)

#finds matches for the user
async def start_matching(user_id, message):
    print("Matching started.....")
    await send_message(message, "!match", is_private=True)
    dataset = database[str(user_id)][1]
    genderlist = database[str(user_id)][0]
    if len(dataset) == 5:
      if len(genderlist)==2:
        matchmade = await match(user_id, dataset)
        if matchmade is None:
            print("No match")
            await message.author.send(
                "No match found yet. We will inform you, if someone gets matched with you🤗")
        else:
            userch, rating = matchmade
            await message.author.send("Match made with user00" +str(database[str(userch)][3]) + " (Matching Qualities: " + str(rating) + "/5)")
            await matchinfo(user_id, userch)
            print("Matching Done")
            await message.author.send(
                f'Your chat with user00{database[str(userch)][3]} starts after they accept the match.'
            )
            print(database)
            save(database)
      else:
        await message.author.send("You have not selected gender properly. Please use !gender")
                                  
    else:
        await message.author.send("You have selected only " +
                                  str(len(dataset)) + " interests")

async def prichat(message, userch): #sends a message to user
  user = client.get_user(int(userch))
  await user.send(message)


def save(my_dict):
  json_str = json.dumps(my_dict)
  with open('database.json', 'w') as f:
      f.write(json_str)


async def match(userid, emjmatchlist): #finds match and changes database[userid1][2] to userid
  genprefmain=database[str(userid)][0][1]
  genmain=database[str(userid)][0][0]
  
  for i,(userch,uservalue) in enumerate(database.items()):
    if uservalue[2] is None:
      emojiset = uservalue[1]
      rat4 = []
      gendcrit1, gendcrit2= False, False
      gendetail=uservalue[0]
      
      if genprefmain==gendetail[0] or genprefmain==3:
        gendcrit1=True
        
      if gendetail[1]==genmain or gendetail[1]==3:
        gendcrit2=True
      
      if gendcrit1 and gendcrit2 and len(emojiset) == 5 and userid != int(userch) and int(userch) not in uservalue[4] and int(userid) not in database[str(userid)][4]:
        rating = len(set(emojiset).intersection(set(emjmatchlist)))
        if rating == 5:
          database[str(userid)][2] = int(userch)
          return (userch, 5)
        elif rating == 4:
          rat4.append(userch)
    if len(rat4) > 0: #when no 5 rating, is found in the whole data
      database[str(userid)][2] = rat4[0]
      return (rat4[0], 4)


async def matchinfo(user1, user2): #in the data of user2, change database[user2][2] to user1 and notofy user1 
  user = client.get_user(int(user2))
  database[str(user2)][2]=str(user1)
  save(database)
  await user.send(f'You have been matched with user00{database[str(user1)][3]} 👀')
  await user.send('To start chatting use \"!chat\".')


async def chat(user1): #user1 accepts the match, confirmation.
  user2=database[str(user1)][2]
  database[str(user1)][2]=int(user2)
  save(database)
  print(database)
  await prichat(f"User 00{database[str(user1)][3]} has accepted the match. Use !help for knowing all available commands.\n Your chat starts below 👇 ", user2)
  
@client.event
async def on_ready():
  print("Ready for launch. I am {0.user}".format(client))


async def send_message(message, user_message, is_private, user_id=None): #sending message
  try:
    response = responses.handle_response(user_message)
    await message.author.send(
      response) if is_private else await message.channel.send(response)

  except Exception as e:
    print(e)

#main
@client.event #dictionary={userid:[gender, emoji, matchid]}
async def on_message(message): #what happends when a particular message is recieved
  user_message = str(message.content) #message
  if message.author == client.user: #if author=cupid
    # Handle each message type separately and Adding Emojis
    await handle_my_sex_message(message)
    await handle_chat_with_message(message)
    await handle_repeated_match_message(message)
    await handle_choose_5_from_message(message)
    await handle_reveal_identity_message(message)
    return 
  username = str(message.author) #author
  channels = str(message.channel) #channel
  user_id = message.author.id
  
  if message.channel.id == 1056560851458470018 or message.guild == None: #cupid channel/private

    if user_message == "!register" and message.guild != None: #!register
      print(user_message)
      await handle_register_message(message, user_id)

    elif message.guild == None: #private conversations, if secuserid exists
      try:
        secuserid = database[str(user_id)][2]
        if user_message[0] != '!' and type(secuserid) is int and database[str(secuserid)][2] == user_id: 
          print(f"{user_id} to {secuserid}:",user_message)
          await prichat(user_message, secuserid)
          return 
      except:
        pass
        
      if user_message[0] == '!' and str(user_id) in database:
        print(f"{username} said: '{user_message}' ({channels})") # Debug printing
        if database[str(user_id)][2] is None or database[str(user_id)][2] ==0: #if not matched

          if user_message == "!mingle": #!mingle
            database[str(user_id)][1] = []  #creating new interest for old users
            await send_message(message, user_message, is_private=True)
  
          elif user_message=="!gender" and len(database[str(user_id)][1])==5: #change gender interests
            await prichat("My Sexual Orientation is: \n1️⃣. Male\n2️⃣. Female\n3️⃣. Others",user_id)
  
          elif user_message == "!match": #!match    
            await start_matching(user_id, message)

          elif user_message == "!stop":
            database[str(user_id)][2]=0
            save(database)
          else:
            await message.channel.send('Invalid command, use "!mingle" or "!match"')
          return
          
        elif database[str(user_id)][2] != 0: #if matched already
          if user_message == "!chat" and type(database[str(user_id)][2]) is str: #!chat
            print("Chat Starting...")
            await message.author.send("Use !help for knowing all available commands.\nYour chat starts below 👇")
            await chat(user_id)
          elif user_message=="!reveal" and type(database[str(user_id)][2]) is not str:
            userch=database[str(user_id)][2]
            await prichat(f"Asking user00{database[str(userch)][3]} to reveal their identity. -Cupid Bot",user_id)
            await prichat(f"user00{database[str(user_id)][3]} wants to reveal their identity. Do you want to reveal your identity? - Cupid",userch)
  
          elif user_message == "!report":
              messages = []
              async for msg in message.channel.history(limit=20):
                  messages.append(msg.content)
              with open("reports.txt", "a") as f:
                  f.write(f"{database[str(user_id)][2]} is reported by {user_id} for the following messages:\n")
                  f.write("\n".join(messages))
              await message.author.send("Last 20 messages of the user has been saved. If you want to end the chat, use !end.")
  
          elif user_message == "!end": #stop the chat
            user1 = database[str(user_id)][3]
            user2_id = database[str(user_id)][2]
            user2 = database[str(user2_id)][3]
            await prichat(
              f'Your Chat with user00{user2} has ended. Use "!match" to start search for a new match or use !stop to stop further matching.', user_id)
            await prichat(f'User00{user1} has ended the chat', user2_id)
            await prichat('Use "!match" to start search for a new match or use !stop to stop further matching.', user2_id)
            
            if database[str(user2_id)][4][0]==1:
              database[str(user2_id)][4].append(user_id)
              
            if database[str(user_id)][4][0]==1:  
              database[str(user_id)][4].append(user2_id)
            database[str(user_id)][2] = None
            database[str(user2_id)][2] = None
            save(database)
          elif user_message == "!help":
            await message.channel.send('Commands:\n !end- To end the chat\n !reveal- To reveal your identity if both agree\n !report- To report abusive behaviour or harrasment\n')
          else:
            await message.channel.send('Invalid command, use "!help" to get a list of all commands')
        else:
          await message.channel.send('Invalid command, use "!mingle" to change interests or wait for sometime⏳')
      else:
        await message.channel.send('Invalid command, use proper commands')       
    else:
      await message.channel.send('Invalid command, use "!register"')
    

@client.event
async def on_raw_reaction_add(payload): #adds interests to database
    userid = payload.user_id
    
    if userid != 1056298996290834503 and payload.guild_id is None:
      emojiicon=str(payload.emoji)
      
      if emojiicon in emojilist:
        emoji = emojilist.index(emojiicon)
        
        if database[str(userid)] is not None:  #olduser
          database[str(userid)][1].append(emoji)
          save(database)
    
        else:  #new user
          emojicode = []
          emojicode.append(emoji)
          database[str(userid)][1]=emojicode
          save(database)
        print(database)
      
      elif emojiicon in numgender:
        database[str(userid)][0]=[numgender.index(emojiicon)]
        save(database)

      elif emojiicon in gender:
        database[str(userid)][0].append(gender.index(emojiicon))
        save(database)

      elif emojiicon in tickwrong :
        database[str(userid)][4]=[tickwrong.index(emojiicon)]
        save(database)

      elif emojiicon in ticktok:
          userch=database[str(userid)][2]
          if ticktok.index(emojiicon)==0:
            await prichat(f'You are chatting with <@{userch}>',userid)
            await prichat(f'You are chatting with <@{userid}>',userch)
          else:
            await prichat("Identities are unrevealed - Cupid",userid)
            await prichat("Identities are unrevealed - Cupid",userch)
          
      
        
@client.event
async def on_reaction_add(reaction, user): #proceeds after adding 5 interests
  if str(user) != "Cupid Bot#9612" and reaction.message.guild is None:
    
    if len(database[str(user.id)][1]) == 5:
      user_message=reaction.message.content
      
      if user_message.startswith("Choose"):
        await reaction.message.channel.send("You have selected 5 interests. ")
        await reaction.message.channel.send("My Sexual Orientation is: \n1️⃣. Male\n2️⃣. Female\n3️⃣. Others")
        
      elif user_message.startswith("My Sex"):
          await reaction.message.channel.send('Chat with: ')
        
      elif user_message.startswith("Chat wi"):
          await reaction.message.channel.send('Repeated Matching On/Off: ')
        
      elif user_message.startswith("Repeated Matc"):
          await reaction.message.channel.send('Type "!match" to find a match for you.😉')
          
          

@client.event
async def on_raw_reaction_remove(payload): #removes interests for a specific user
  if payload.guild_id is None:
    userid = payload.user_id
    emoji = emojilist.index(str(payload.emoji))
    database[str(userid)][1].remove(emoji)
    save(database)
    print(database)


client.run(os.getenv('TOKEN'))