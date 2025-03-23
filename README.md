WordleTUI: Terminal-based Wordle Game

A fully interactive, terminal-based Wordle game implemented in Python. This version includes user profiles, customizable game settings, persistent storage, and an engaging textual user interface (TUI).

Features
  Interactive Terminal Interface: Play Wordle directly from your terminal with intuitive prompts and colorful hints.
  User Profiles: Create multiple user profiles to track individual progress, scores, and game history.
  Persistent Data Storage: User information and word banks are stored persistently between sessions.
  Customizable Settings: Choose the length of the secret word (3–8 letters) and number of allowed guesses (1–10).
  Color-Coded Feedback: Clear hints indicating correct letters and placements using colored output.
  Game History: View your previous games, including scores and outcomes.

Installation and Setup
  Installation
  Clone this repository:
  git clone https://github.com/helgithorskarp/wordleTUI.git
  Navigate to the project directory:
  cd wordleTUI

  Running the Game
    To start the game, simply run the main script:
    python main.py 
    OR
    python3 main.py 


How to Play:
  Choose or create a username
  Select your preferred game settings (word length and number of guesses).
  Enter your guesses. After each guess, you'll receive feedback:
  green (C): Correct letter in the correct position.
  Yellow (c): Correct letter in the wrong position.
  Dash (-): Letter not present in the secret word.


Author
Helgi Þór Skarphéðinsson
