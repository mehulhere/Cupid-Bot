import discord
import os
import responses
import json
import threading
lock = threading.Lock()

# Future Changelogs:
# better UI-stickers, emojis

# !feedback- save
# action on reports
# ice-breaking games

cupidChannel = '105656085145847001' #Can be altered based on the server, cupid is added.
emojilist = ['🎮', '🅰️', '♟️', '🎵', '📸', '⛹️'] #all interest emoji's
gender=['🧑','👸','🌈','🧑‍🤝‍🧑']
numgender=['1️⃣','2️⃣','3️⃣']
tickwrong=['✅','❎']
ticktok=['☑️','❌']
intents = discord.Intents().all()
intents.message_content = True
client = discord.Client(intents=intents)
try:
  with open("database.json", "r") as f:
      database = json.load(f)
      print(database)
except FileNotFoundError as e:
  print(e)
  database = {}



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
  if "wants to reveal their identity" in message.content:
      await add_emojis(message, ticktok)


#handles "!register" response
async def handle_register_message(message,user_id, private):
  if (private):
    await message.channel.send(message.author.mention + " You are registered for Blind Dating💍")
  else:
    await message.channel.send(message.author.mention + " You are registered for Blind Dating💍, check your dm.")
  print(f"user{len(database)+1} registered")
  database[str(user_id)]=[None, None, None, len(database)+1, [None], [0,0,0]] #GendersUser/Pref, Interests, PairID, UserSID, RepeatedMatchedUsers(if on), MatchingOn/ChatReqAccepted
  save(database)
  await send_message(message, "!register", is_private=True)

async def endChatHandler(user_id, pair_id):
    requestorSID = database[str(user_id)][3]  
    pairSID = database[str(pair_id)][3] 
    await privateChat(
      f'Your Chat with user00{pairSID} has ended. Use "!match" to start search for a new match or use !stop to stop further matching.', user_id)
    await privateChat(f'User00{requestorSID} has ended the chat', pair_id)
    await privateChat('Use "!match" to start search for a new match or use !stop to stop further matching.', pair_id)

    if database[str(user_id)][5][2]==1: #if repeated matching off 
      database[str(user_id)][4].append(pair_id)
    if database[str(pair_id)][5][2]==1: #if repeated matching off (pair)
      database[str(pair_id)][4].append(user_id)

    #Updating Database
    database[str(user_id)][2] = None 
    database[str(pair_id)][2] = None
    database[str(user_id)][5][1] = 0
    database[str(pair_id)][5][1] = 0
    save(database)


#finds matches for the user
async def start_matching(user_id, message):
    print("Matching started.....")
    await send_message(message, "!match", is_private=True) #Message notifying user that matching has started
    interestSet = database[str(user_id)][1] #Retrives Interests
    genderlist = database[str(user_id)][0] #Retrieves Gender of user
    matchmade = await match(user_id, interestSet) #Searching for match
    if matchmade is None:
        print("No match")
        await message.author.send(
            "No match found yet. We will inform you, if someone gets matched with you🤗")
    else:
        userItem, rating = matchmade
        await message.author.send("Match made with user00" +str(database[str(userItem)][3]) + " (Matching Qualities: " + str(rating) + "/5)")
        await matchinfo(user_id, userItem)
        print("Matching Done")
        await message.author.send(
            f'Your chat with user00{database[str(userItem)][3]} starts after they accept the match.'
        )
        database[str(userItem)][5][1] = 1
        print(database)
        save(database)


async def privateChat(message, userch): #sends a message to user
  user = client.get_user(int(userch))
  await user.send(message)


def save(my_dict):
  json_str = json.dumps(my_dict)
  with open('database.json', 'w') as f:
      f.write(json_str)


async def match(userid, userEmojiList): #finds match and changes database[userid1][2] to userid
  with lock: #Multithreading Safe now, while the matching is happening for one user, it cant be happening simultaneously for other user.
    user_genderPreference=database[str(userid)][0][1] 
    user_gender=database[str(userid)][0][0] 
    bufferMatch = [] #If not all interests match
    for i,(itemUserid,itemDatabase) in enumerate(database.items()): 
      userNotMatched = True if itemDatabase[2] is None else False
      matchingwithItself = int(userid)==int(itemUserid)
      matchingTurnedon = itemDatabase[5][0] #Checking if matching is enabled
      if userNotMatched and not matchingwithItself and matchingTurnedon:
        emojiset = itemDatabase[1]
        gendcrit1, gendcrit2= False, False #Both should be true for successful matching
        itemUserGender = itemDatabase[0][0] #Iterating User gender
        itemUserGenderPreference = itemDatabase[0][1] #Iterating User gender preference

        if user_genderPreference==itemUserGender or user_genderPreference==3:
          gendcrit1=True

        if itemUserGenderPreference==user_gender or itemUserGenderPreference==3:
          gendcrit2=True
        print(type(itemUserid))
        print(type(userid))
        if gendcrit1 and gendcrit2 and userid not in itemDatabase[4] and int(itemUserid) not in database[str(userid)][4]: #Incase of Repeated Matching off
          rating = len(set(emojiset).intersection(set(userEmojiList))) #Based on how many interests match
          if rating == 5: #Match made instanteneously
            database[str(userid)][2] = int(itemUserid)
            return (itemUserid, 5)
          elif rating == 4:
            bufferMatch.append(itemUserid)
    if len(bufferMatch) > 0: #when no 5 rating, is found in the whole data
      database[str(userid)][2] = int(bufferMatch[0])
      return (bufferMatch[0], 4)


async def matchinfo(user1, user2): #in the data of user2, change database[user2][2] to user1 and notify user1 
  user = client.get_user(int(user2))
  database[str(user2)][2]=int(user1)
  save(database)
  await user.send(f'You have been matched with user00{database[str(user1)][3]} 👀')
  await user.send('To start chatting use \"!chat\".')


async def chat(user1): #user1 accepts the match, confirmation.
  user2=database[str(user1)][2]
  database[str(user1)][5][1] = 1 #Chatting Enabled
  database[str(user2)][5][1] = 1 #Chatting Enabled for User2
  save(database)
  # print(database)
  await privateChat(f"User 00{database[str(user1)][3]} has accepted the match. Use !help for knowing all available commands.\n Your chat starts below 👇 ", user2)

@client.event
async def on_ready(): #runs when bot is online
  print("Ready for launch. I am {0.user}".format(client))


async def send_message(message, user_message, is_private, user_id=None): #sending message
  try:
    response = responses.handle_response(user_message)
    await message.author.send(
      response) if is_private else await message.channel.send(response)

  except Exception as e:
    print(e)

#main
#dictionary={userid:[gender, emoji, matchid]}

@client.event 
async def on_message(message): #Called when any message is recieved  
  # print(message)
  # print(database)
  user_message = str(message.content)
  if message.author == client.user: #if author is cupid
    # Adding Emojis to each message
    await handle_my_sex_message(message)
    await handle_chat_with_message(message)
    await handle_repeated_match_message(message)
    await handle_choose_5_from_message(message)
    await handle_reveal_identity_message(message)
    return 
  username = str(message.author) #username
  channels = str(message.channel) #channel
  user_id = message.author.id

  if message.channel.id == cupidChannel or message.guild == None: #all other messages except cupid channel or DM's are ignored.
    private = message.guild == None
    if user_message == "!register": #responds to "!register" message in public discord channel chats
      await handle_register_message(message, user_id, private)
    elif message.guild == None: #conditional programming for private DMs
      existingUser = str(user_id) in database

      if (existingUser):
        user_paired =  True if (type(database[str(user_id)][2])) is int else False #checking if the user is paired (DMs will be forwarded to pair)
        if (user_paired): 
          pair_id = database[str(user_id)][2]
          chatEnabled = True if(database[str(user_id)][5][1] == 1 and database[str(pair_id)][5][1] == 1) else False
          if (not chatEnabled): #Chat Disabled
            if user_message == "!chat" and database[str(user_id)][5][1] == 1: 
              print("Chat Starting...")
              await message.author.send("Use !help for knowing all available commands.\nYour chat starts below 👇")
              await chat(user_id)
            elif user_message == "!end": #stop the chat
              await endChatHandler(user_id, pair_id)
            else:
              await message.channel.send('Invalid command, use "!end" to end the chat')
              return

          else: #Chat Enabled
            secondUserID = database[str(user_id)][2]
            if user_message[0] != '!' and database[str(secondUserID)][2] == user_id and database[str(secondUserID)][5][1]==1 and database[str(user_id)][5][1]==1 : #double checks
              print(f"{user_id} to {secondUserID}:", user_message)
              await privateChat(user_message, secondUserID) #Sends message to the pair
              return 

          #Conditional programming for Cupid Commands when paired
            elif user_message=="!reveal":
              userch=database[str(user_id)][2]
              await privateChat(f"Asking user00{database[str(userch)][3]} to reveal their identity(discord_id). -Cupid Bot",user_id)
              await privateChat(f"user00{database[str(user_id)][3]} wants to reveal their identity(discord_id). Do you want to reveal your identity? - Cupid",userch)

            elif user_message == "!report":
                messages = []
                async for msg in message.channel.history(limit=20): #Gets last 20 messages
                    messages.append(msg.content)
                with open("reports.txt", "a") as f:
                    f.write(f"{database[str(user_id)][2]} is reported by {user_id} for the following messages:\n")
                    f.write("\n".join(messages))
                await message.author.send("Last 20 messages of your match have been reported. If you want to end the chat, use !end.")

            elif user_message == "!help":
              await message.channel.send('Commands:\n !end- To end the chat\n !reveal- To reveal your identity if both agree\n !report- To report abusive behaviour or harrasment\n')

            elif user_message == "!end": #stop the chat
              await endChatHandler(user_id, pair_id)

            else:
              await message.channel.send('Invalid command, use "!help" to get a list of all commands')



        #User Unpaired
        elif user_message[0] == '!' and str(user_id) in database: #Command Conditional Code
          print(f"{username} said: '{user_message}' ({channels})") # Debug printing

          interestSet = database[str(user_id)][1]
          genderlist = database[str(user_id)][0]
          interestSetVerify = True if interestSet is not None and len(interestSet) == 5 else False
          genderlistVerify = True if genderlist is not None and len(genderlist) == 2 else False

          if user_message == "!mingle": 
              database[str(user_id)][1] = []  #creating new interest for old users
              await send_message(message, user_message, is_private=True)

          elif user_message=="!gender" and interestSetVerify: #change gender interests
              await privateChat("My Sexual Orientation is: \n1️⃣. Male\n2️⃣. Female\n3️⃣. Others",user_id)

          elif user_message == "!match" and interestSetVerify and genderlistVerify:    
            database[str(user_id)][5][0] = 1 #Matching Enabled
            save(database)
            await start_matching(user_id, message)

          elif user_message == "!stop": #Stops Future Matching
            database[str(user_id)][5][0] = 0 #Matching Disabled
            save(database)
            await message.channel.send('Matching Profile Deactivated')

          else:
            await message.channel.send('Invalid command, use "!mingle"')
          return

        else:
            await message.channel.send('Invalid command, use "!mingle" to change interests or wait for sometime⏳')
            return
      else:
          await message.channel.send('You haven\'t registered yet, use "!register"')       
    else:
        await message.channel.send('Invalid command, use "!register"')


@client.event
async def on_raw_reaction_add(payload): #adds interests to database
    userid = payload.user_id
    cupidId = 1056298996290834503
    if userid != cupidId and payload.guild_id is None: #If DM
      emojiicon=str(payload.emoji) #Get Emoji Icon

      if emojiicon in emojilist: #If Emoji in interest list
        emoji = emojilist.index(emojiicon)

        if database[str(userid)] is not None:  #Incase of non-first emoji insertion
          database[str(userid)][1].append(emoji)
          save(database)

        else:  #First Emoji Insertion
          emojicode = []
          emojicode.append(emoji)
          database[str(userid)][1]=emojicode
          save(database)

      elif emojiicon in numgender: #If Emoji in genderList1
        database[str(userid)][0]=[numgender.index(emojiicon)]
        save(database)

      elif emojiicon in gender: #If Emoji is genderList2
        database[str(userid)][0].append(gender.index(emojiicon))
        save(database)

      elif emojiicon in tickwrong: #If emoji is tick or wrong
        database[str(userid)][5][2]=tickwrong.index(emojiicon)
        database[str(userid)][4]=[None]
        save(database)

      elif emojiicon in ticktok: #If emoji is tick2 or wrong2 (Reveal IDs)
          paired_user=database[str(userid)][2]
          if ticktok.index(emojiicon)==0:
            await privateChat(f'You are chatting with <@{paired_user}>', userid)
            await privateChat(f'You are chatting with <@{userid}>', paired_user)
          else:
            await privateChat("Identities are unrevealed - Cupid",userid)
            await privateChat("Identities are unrevealed - Cupid", paired_user)



@client.event
async def on_reaction_add(reaction, user):
  if str(user) != "Cupid Bot#9612" and reaction.message.guild is None: #Emoji in DM

    if len(database[str(user.id)][1]) == 5: #If 5 Interests are chosen
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
async def on_raw_reaction_remove(payload): #For misclicking Interests(On Emoji Removal)
  if payload.guild_id is None: #If DM
    userid = payload.user_id
    emoji = emojilist.index(str(payload.emoji))
    database[str(userid)][1].remove(emoji)
    save(database)
    print(database)


client.run(os.getenv('TOKEN')) #Runs the bot using discord BOT Token