def handle_response(message) -> str:
    p_message = message.lower()
    if p_message == '!register':
        return 'Cupid welcomes you onboard! You can start blind dating by using "!mingle"'

    elif p_message == '!match':
      return 'Finding a match.......👀'

    elif p_message == '!help':
        return "`You can try !mingle`"
      
    elif p_message == '!mingle':
        return ("Choose any 5 from the following. \n🎮 : Gaming \n🅰️ : Anime \n♟️ : Chess \n🎵 : Music \n📸 : Photography \n ⛹️ : Sports")
      
    else:
        return 'Yeah, I don\'t know. Try typing "!help".'