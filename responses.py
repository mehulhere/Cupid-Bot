def handle_response(message) -> str:
    p_message = message.lower()
    if p_message == '!register':
        return 'Cupid welcomes you onboard! You can start blind dating by using "!mingle"'

    elif p_message == '!match':
      return 'Finding a match.......👀'

    elif p_message == '!help':
        return "`You can try !mingle`"
      
    elif p_message == '!mingle':
      return ("Welcome to the realm of love's guiding hand!💘\nChoose any 5 from the following. \n🅰️ : Anime \n🎨 : Art \n🍳 : Cooking\n🎮 : Gaming \n🎬 : Movies \n🎵 : Music \n📸 : Photography \n🐶 : Pets \n📚 : Reading \n⛹️ : Sports \n🧑‍💻 : Technology\n🎭 : Theater \n🧘 : Yoga")
      
    else:
        return 'Yeah, I don\'t know. Try typing "!help".'