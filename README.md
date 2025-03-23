🟩 WordleTUI: Terminal-based Wordle Game

A fully interactive, terminal-based Wordle game implemented in Python. This version includes user profiles, customizable game settings, persistent storage, and an engaging textual user interface (TUI).

🚀 Features

Interactive Terminal Interface: Play Wordle directly from your terminal with intuitive prompts and colorful hints.

User Profiles: Create multiple user profiles to track individual progress, scores, and game history.

Persistent Data Storage: User information and word banks are stored persistently between sessions.

Customizable Settings: Choose the length of the secret word (3–8 letters) and number of allowed guesses (1–10).

Color-Coded Feedback: Clear hints indicating correct letters and placements using colored output.

Game History: View your previous games, including scores and outcomes.

🛠️ Installation and Setup

Prerequisites

Python 3.8 or higher

Installation

Clone this repository:

git clone https://github.com/helgithorskarp/wordleTUI.git

Navigate to the project directory:

cd wordleTUI

(Optional) Create and activate a virtual environment:

python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

Install any dependencies (if required, usually standard Python libraries are enough):

pip install -r requirements.txt

Note: If there is no requirements.txt, the project uses only built-in Python libraries.

▶️ Running the Game

To start the game, simply run the main script:

python main.py 

OR

python3 main.py 

You will be prompted to create a new user or log in with an existing one.

📖 How to Play

Choose or create a username.

Select your preferred game settings (word length and number of guesses).

Enter your guesses. After each guess, you'll receive feedback:

Green (C): Correct letter in the correct position.

Yellow (c): Correct letter in the wrong position.

Dash (-): Letter not present in the secret word.

Try to guess the secret word within your allowed attempts!

💾 Data Storage

wordBank.txt: Contains all available words.

users.json: Stores user profiles, game history, and high scores.

These files are automatically updated during gameplay.

🎯 Project Structure

wordleTUI/
├── main.py                 # Entry point for the application
├── UI.py                   # Handles user interaction and menus
├── wordleEngine.py         # Core game logic
├── users.py                # User profile management and data persistence
├── wordBank.txt            # Word list
├── users.json              # User data and game records
└── README.md               # Project documentation

🚧 Potential Improvements

Implement a graphical user interface (GUI).

Develop a web-based or mobile app version.

Add online multiplayer capabilities.

👤 Author

Helgi Þór Skarphéðinsson
