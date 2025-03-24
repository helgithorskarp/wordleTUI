import os
from typing import List, Tuple
from wordleEngine import *
from users import *

class UI:
    def __init__(self) -> None:
        self.wordleEngine = WordleEngine()
        self.users = Users()

    def gameMenu(self) -> None:
        userName = self.__loginMenu() 

        hasUserQuit = False
        while not hasUserQuit: # keeps going until user enters 'q'
            hasUserQuit = self.__displayMainScreen(userName) # main menu
            if hasUserQuit:
                continue # user pressed 'q'
            
            letterCount, guessCount = self.__getGameSettings()
            try:
                secret = self.wordleEngine.getWord(letterCount) # get random word from bank
                hasUserQuit = self.__startGameMenu(secret, letterCount, guessCount, userName)
            except NoWordExists:
                self.__printScreen(
                    'No words currently are being stored for this Length\nPlease try again later', ''
                )
                return

        self.__printScreen(
            f'\nWoohoo! Thanks for playing, {userName}! You totally rocked it! 🤩🎮\n'
            'Catch you next time... 👋😄\n',
            ''
        )

    def __loginMenu(self) -> str:
        '''Allows user to login or create new user, either way the username of logged in account is returned'''
        userDict = self.users.usersDict

        option = ''
        while option not in ['1', '2']: # user has two options either to add a new user or login
            self.__printScreen(
                '\n🚀 Welcome to the Ultimate PA6 Wordle Challenge! 🌟\n\n'
                '1. Add a new user ✨\n'
                '2. Log in with an existing user 🔑\n',
                '👉 Choose an option: '
            )
            option = input()

        if option == '2': # user picked to login, keep asking until a valid username is entered
            username = ''
            while username not in userDict:
                self.__printScreen(
                    '\n👤 Choose a username from the following options:\n   ' + '\n   '.join(userDict.keys()) + '\n',
                    '🎯 Your choice: '
                )
                username = input()
            return username

        errMessage = ''
        username = ''
        while not username or username in userDict: # ask for a new usedName until a unique name is chosen
            self.__printScreen(
                '\n🔥 Ready to test your Wordle skills? 🔥\n'
                'Enter your username to create an account and begin your epic adventure! 🏆\n',
                'Your username: ',
                errMessage
            )
            username = input()
            errMessage = '⚠️ This username has already been taken! Please try again.\n' if username in userDict else ''
        self.users.addNewUser(username)
        return username

    def __displayMainScreen(self, name: str) -> bool:
        '''Main menu allows user to start game, or navigate menu, true is returned if user quits, else true'''
        highScore = round(self.users.usersDict[name].maxScore, 3)
        userChoice = 'h'
        #Color codes
        GREEN = "\033[92m"
        YELLOW = "\033[93m"
        RESET = "\033[0m"

        while userChoice.lower() in ['h', 'w']: # keep asking the user for a option while he decides to look at history or add a word
            self.__printScreen(                 # this is done so that after user returns from either menu they are still at the main menu
                f"""
    🎉 Welcome to Wordle, {name}!
    🏆 Your High Score: {highScore}  |  🌟 World Record: {round(self.users.recordScore, 3)}

    🔍 Use logic to guess the word!
    ✅ Feedback:  {GREEN}C{RESET} = correct | {YELLOW}c{RESET} = misplaced | - = wrong
    📌 Options:
        [Enter]  ▶️  Start Game
        [H]      📜  Game History
        [W]      ➕  Add Word to Word Bank
        [Q]      🚪  Quit""", "Your choice: "
            )

            userChoice = input().strip()
            if userChoice.lower() == 'h':
                self.__showGameHistory(name) # user decides to look at game history menu
            elif userChoice.lower() == 'w':
                self.__addWordToWordBank() # user decides to look add a new word

        return True if userChoice.lower() == 'q' else False

    # --- Game Settings & Session ---
    def __getGameSettings(self) -> Tuple[int, int]:
        '''Asks user for both word length and the letter count of the game, a tuple is returned with both (int(wordLength, int(guessCount))'''
        
        validWordLength = False
        errMessage = ''
        while not validWordLength: # ask user fot a word length until a valid word length is entered
            self.__printScreen('\n🎲 Set word length (3–8): 🎯\n', '👉 Your length: ', errMessage)
            userWordLength = input()
            if self.wordleEngine.validateWordLength(userWordLength):
                validWordLength = True
                errMessage = ''
            else:
                errMessage = '⚠️ Please enter a number between 3 and 8\n'

        validGuessCount = False
        errMessage = ''
        while not validGuessCount:  # ask user fot a guess count until a valid word length is entered
            self.__printScreen('\n🎰 Set guess count (1–10): 🎲\n', '👉 Your guess count: ', errMessage)
            userGuessCount = input()
            if self.wordleEngine.validateGuessCount(userGuessCount):
                validGuessCount = True
                errMessage = ''
            else:
                errMessage = '⚠️ Please enter a number between 1 and 10\n'

        return (int(userWordLength), int(userGuessCount))

    def __startGameMenu(self, secret: str, lettersCount: int, guessesAllowed: int, name: str) -> bool:
        '''plays the wordle game, true is returned if user quits else false'''
        isWinner = False
        guessScore = 0
        errMessage = ''
        guesses: List[Tuple[str, str]] = []
        
        #main body that is printed
        body = f'Welcome To Wordle {name}\nPlease guess a {lettersCount} letter word!'
        
        # keep playing game until either user wins or the guess score matches the total allowed guesses
        while not isWinner and guessScore != guessesAllowed:
            self.__printScreen('\n\n' + body + '\n\n', f'{lettersCount}-letter word: ', errMessage)
            userWord = input() # ask for a word
            
            # if word is invalid then restart while loop
            if not self.wordleEngine.validateGuess(userWord, lettersCount):
                errMessage = f'Your guess must only contain letters and be of length {lettersCount}\n'
                continue

            # get hint from engine based on guess, if the hint is a winning hint then while loop ends
            hint = self.wordleEngine.generateHint(secret, userWord)
            guesses.append((hint, userWord))
            if self.wordleEngine.isWinner(hint, lettersCount):
                guessScore += 1
                isWinner = True # declared as winner
                continue

            errMessage = ''
            guessScore += 1
            body = self.__generateGameBody(guesses) # update body for next round

        # after game is finished new record is stored and closing menu is displayed
        self.users.addNewRecordToUser(name, lettersCount, guessesAllowed, guessScore, isWinner)
        return self.__closeGameMenu(isWinner, guesses, secret)

    def __generateGameBody(self, guesses: List[Tuple[str, str]]) -> str:
        '''Generate game body text with previous guesses and hints.'''
        return '\n'.join([f'{guess[0]}       {guess[1].upper()}' for guess in guesses])

    def __closeGameMenu(self, didUserWin: bool, guesses: List[Tuple[str, str]], secret: str) -> bool:
        '''Shows closing menu after a game has been finished, true is returned if user quits, true if not'''
        body = self.__generateGameBody(guesses)

        if didUserWin:
            body += f'\n\n🥳 Woohoo! You nailed it! 🎉\nYour score: {len(secret) ** 2 / len(guesses):.2f} 🚀'
        else:
            body += f'\n\n😅 So close! Better luck next round!\nThe secret word was: {secret.upper()} 📚'

        self.__printScreen(body, '✨ Press enter to go to main menu, or type "q" to quit! 🚪: ')
        userInput = input()
        return userInput.lower() == 'q'


    def __showGameHistory(self, name: str) -> None:
        '''Shows user his game history nothing is returned'''
        
        # body of all games
        gameHistoryList = [
            f"{game}: {points} points, {'win' if points > 0 else 'loss'}" 
            for game, points in self.users.usersDict[name].scores.items()
        ]
        gameHistoryStr = 'GAME HISTORY\n\n' + '\n'.join(gameHistoryList)
        self.__printScreen(gameHistoryStr, 'Press enter to continue: ')
        input()

    def __addWordToWordBank(self) -> None:
        '''shows word bank menu and allows user to add a new word'''
        
        newWordFound = False
        errMessage = ''
        # keep asking user for a word until a valid word is found
        while not newWordFound:
            self.__printScreen(
                "\n📝 Let's add a new word to your Word Bank!\n🔤 Must be 3–8 letters long and only contain letters.\n",
                "👉 Your word: ",
                errMessage
            )
            newWord = input()
            newWordFound = self.wordleEngine.validateNewWord(newWord)
            errMessage = '⚠️  Word must only contain letters and be between 3 and 8 characters long.\n'

        self.wordleEngine.addNewWord(newWord) # add new word to bank, display screen allowing the user to return 
        self.__printScreen(f"\nNew word '{newWord}' has been added to the Word Bank! 🚀\n", "Press enter to continue: ")
        input()
        

    # --- Utility Methods PRINTS screen and clears terminal ---
    def __printScreen(self, body: str, inputPrompt: str, errMessage: str = '') -> None:
        '''Prints screen based on the body and input prompt entered, nothing is returned'''
        self.__clearScreen()
        RED = '\033[91m'
        CYAN = '\033[96m'
        RESET = '\033[0m'
        
        menu = f'''
{RED}-----------------------------------------------------------------{RESET}
{CYAN}             █───█ █▀▀█ █▀▀█ █▀▀▄ █── █▀▀ 
             █▄█▄█ █──█ █▄▄▀ █──█ █── █▀▀ 
             ─▀─▀─ ▀▀▀▀ ▀─▀▀ ▀▀▀─ ▀▀▀ ▀▀▀ 𝑷𝑨6 🎲{RESET}
{RED}-----------------------------------------------------------------{RESET}
{body}
{RED}-----------------------------------------------------------------{RESET}
{errMessage + inputPrompt}'''
        print(menu, end='')

    @staticmethod
    def __clearScreen() -> None:
        os.system('cls' if os.name == 'nt' else 'clear')
