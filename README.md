WordleTUI: Terminal-based Wordle Game

A fully interactive, terminal-based Wordle game implemented in Python. This version includes user profiles, customizable game settings, persistent storage, and an engaging textual user interface (TUI).

Pip installs required:
      nothing to install! — it all runs with standard Python! 😄

Features
  Interactive Terminal Interface: Play Wordle directly from your terminal with intuitive prompts and colorful hints.
  User Profiles: Create multiple user profiles to track individual progress, scores, and game history.
  Persistent Data Storage: User information and word banks are stored persistently between sessions.
  Customizable Settings: Choose the length of the secret word (3–8 letters) and number of allowed guesses (1–10).
  Color-Coded Feedback: Clear hints indicating correct letters and placements using colored output.
  Game History: View your previous games, including scores and outcomes.

Installation and Setup
  1. Installation
    Clone this repository:
    git clone https://github.com/helgithorskarp/wordleTUI.git
    Navigate to the project directory:
    cd wordleTUI


  2. Running the Game
    To start the game, simply run the main script:
    python main.py 
    # or
    python3 main.py 

  3. ENJOY :D


How to Play:
  Choose or create a username
  Select your preferred game settings (word length and number of guesses).
  Enter your guesses. After each guess, you'll receive feedback:
  green (C): Correct letter in the correct position.
  Yellow (c): Correct letter in the wrong position.
  Dash (-): Letter not present in the secret word.

Additional Info about how the game decides what is C (yellow)/ c (green).
  When you enter a word in Wordle, each letter is checked against the correct word. If a letter is in the correct position, it turns green. If a letter exists in the correct word but is in the wrong position, it turns yellow. However, if the correct word only contains that letter once, and you guess it multiple times in different positions, only one of them will turn yellow — the rest will remain gray. This is because the game only gives credit for the exact number of times a letter appears in the correct word.


Author
Helgi Þór Skarphéðinsson
