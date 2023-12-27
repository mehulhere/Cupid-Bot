#### Discord Blind Dating Bot
##### About Me:
Hii, I am Mehul Pahuja. This was my first project. I coded this in the first sem of my Btech

##### Overview
This Discord bot facilitates a blind dating system within Discord channels, allowing users to register, set up preferences, match with others based on interests and gender orientation, and communicate privately.

##### Features
- **Registration**: Users can register with the bot using `!register` and set up their gender orientation and interests.
- **Matching**: Initiate matching with other users using `!match` based on selected interests and gender preferences.
- **Chatting**: Communicate privately with matched partners using the `!chat` command in a dedicated private channel.
- **Interaction Handling**: Handles various commands for preferences, ending chats, reporting abuse, etc.

##### How to Use
1. **Registration**: Use `!register` to register with the bot and set up your preferences.
2. **Setting Preferences**: Use commands like `!gender`, `!mingle`, and react to messages to set gender and interests.
3. **Matching**: Initiate matching using `!match` to find a match based on your preferences.
4. **Chatting**: Once matched, use `!chat` to start a private chat with your match.
5. **Additional Commands**: `!end` to end a chat, `!report` to report abusive behavior, etc.

##### Technical Details
- The bot is written in Python using the `discord.py` library.
- Utilizes a JSON database (`database.json`) to store user information.
- Handles messages, reactions, and commands to manage the blind dating process.

##### Setup Instructions
1. Clone the repository.
2. Install necessary dependencies.
3. Configure environment variables (e.g., Discord Bot Token).
4. Run the bot script.

##### Contributions and Issues
For contributions or issues, feel free to raise a PR or open an issue in the repository.

##### Authors
Mehul Pahuja
