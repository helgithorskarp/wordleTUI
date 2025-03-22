import os
from typing import List, Tuple
from wordleEngine import *
from users import *

class UI:
    def __init__(self) -> None:
        self.wordleEngine = WordleEngine()
        self.users = Users()
    
    def gameMenu(self) -> None:
        userName = self.__logInMenu()
        
        hasUserQuit = False
        while not hasUserQuit:
            hasUserQuit = self.__printMainScreen(userName)
            if hasUserQuit:
                continue
            letterCount, guessCount = self.__getGameInfo()
            try:
                secret = self.wordleEngine.getWord(letterCount)
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
            
    def __startGameMenu(self, secret: str, lettersCount: int, guessesAllowed: int, name: str) -> bool:
        isWinner = False
        guessScore = 0
        errMessage = ''
        guesses: List[Tuple[str, str]] = []
        body = f'Welcome To wordle {name}\nPlease guess a {lettersCount} letter word!'
        while not isWinner and guessScore != guessesAllowed:
            self.__printScreen(body, f'{lettersCount}-letter word: ', errMessage)
            userWord = input()
            
            if not self.wordleEngine.validateGuess(userWord, lettersCount):
                errMessage = f'Your guess must only contain letters and be of length {lettersCount}\n'
                continue
            
            hint = self.wordleEngine.generateHint(secret, userWord)
            guesses.append((hint, userWord))
            if self.wordleEngine.isWinner(hint, lettersCount):
                guessScore += 1
                isWinner = True
                continue
            
            errMessage = ''
            guessScore += 1
            body = self.__generatebody(guesses)
        
        self.users.addNewRecordToUser(name, lettersCount, guessesAllowed, guessScore, isWinner)
        return self.__closingMenu(isWinner, guesses, secret)
        
    def __generatebody(self, guesses: List[Tuple[str, str]]) -> str:
        # Generate game body text with previous guesses and hints.
        return '\n'.join([f'{guess[0]}       {guess[1].upper()}' for guess in guesses])
    
    def __closingMenu(self, didUserWin: bool, guesses: List[Tuple[str, str]], secret: str) -> bool:
        body = self.__generatebody(guesses)
        
        if didUserWin:
            body += f'\n\nCongratulations you won 🎉!\nYour score was: {len(secret) ** 2 / len(guesses)}'
        else:
            body += f'\n\nBetter luck next time!\nThe correct word was: {secret}'
        
        self.__printScreen(body, 'Enter q to quit, or press enter to restart the game!: ')
        userInput = input()
        if userInput.lower() == 'q':
            return True
        return False

    def __getGameInfo(self) -> Tuple[int, int]:
        validWordLength = False
        errMessage = ''
        while not validWordLength:
            self.__printScreen('Set word length (3–8):', '', errMessage)
            userWordLength = input('Your length: ')
            if self.wordleEngine.validateWordLength(userWordLength):
                validWordLength = True
                errMessage = ''
            else:
                errMessage = 'Please enter a number between 3 and 8\n'
        
        validGuessCount = False
        errMessage = ''
        while not validGuessCount:
            self.__printScreen('Set guess count (1–10):', '', errMessage)
            userGuessCount = input('Your guess count: ')
            if self.wordleEngine.validateGuessCount(userGuessCount):
                validGuessCount = True
                errMessage = ''
            else:
                errMessage = 'Please enter a number between 1 and 10\n'
        
        return (int(userWordLength), int(userGuessCount))
    
    def __logInMenu(self) -> str:
        userDict = self.users.usersDict

        # Get a valid option: '1' to add a new user, '2' to log in as an existing user.
        option = ''
        while option not in ['1', '2']:
            self.__printScreen(
                'Welcome to the Ultimate PA6 Wordle Challenge!\n\n'
                '1. Add a new user\n'
                '2. Log in with an existing user',
                'Choose an option: '
            )
            option = input()

        # Option 2: Existing user login
        if option == '2':
            username = ''
            while username not in userDict:
                self.__printScreen(
                    'Choose a username from the following options:\n' + '\n'.join(userDict.keys()),
                    'Your choice: '
                )
                username = input()
            return username

        # Option 1: Add a new user
        errMessage = ''
        username = ''
        while not username or username in userDict:
            self.__printScreen(
                'Ready to test your wordle skills?\nEnter your username to create a account and begin your adventure!',
                'Your username: ',
                errMessage
            )
            username = input()
            errMessage = 'This username has already been taken!\n' if username in userDict else ''
        self.users.addNewUser(username)
        return username

    def __printMainScreen(self, name):
        highScore = self.users.usersDict[name].maxScore
        userChoice = 'h'
        
        while userChoice.lower() in ['h', 'w']:
            self.__printScreen(
                f"""
    🎉 Welcome to Wordle, {name}!
    🏆 Your High Score: {highScore}  |  🌟 World Record: {self.users.recordScore}

    🔍 Use logic to guess the word!
    ✅ Feedback:  C = correct | c = misplaced | - = wrong

    📌 Options:
        [Enter]  ▶️  Start Game
        [H]      📜  Game History
        [W]      ➕  Add Word to Word Bank
        [Q]      🚪  Quit""","Your choice: ")



            userChoice = input().strip()
            if userChoice.lower() == 'h':
                self.__showGameHistory(name)
            elif userChoice.lower() == 'w':
                self.__addWordToWordBank()  
            
        return True if userChoice.lower() == 'q' else False

                
    def __showGameHistory(self, name: str) -> None:
        gameHistoryList = [
            f"{game}: {points} points, {'win' if points > 0 else 'loss'}" 
            for game, points in self.users.usersDict[name].scores.items()
        ]
        gameHistoryStr = 'GAME HISTORY\n\n' + '\n'.join(gameHistoryList)
        self.__printScreen(gameHistoryStr, 'Press enter to continue: ')
        input()
        
    
    def __addWordToWordBank(self):
        newWordFound = False
        errMessage = ''
        while not newWordFound:
            self.__printScreen("Enter a new word for the collection!", "New word: ", errMessage)
            newWord = input()
            newWordFound = self.wordleEngine.validateNewWord(newWord)
            errMessage = 'Word must only contain letters and be between 3 and 8 characters long.\n'
        
        self.wordleEngine.addNewWord(newWord)
        self.__printScreen(f"New word '{newWord}' has been created! 🚀", "Press enter to continue: ")

        input()

            

    
    def __printScreen(self, body: str, Input: str, errMessage: str = '') -> None:
        self.__clearScreen()
        menu = f'''
-----------------------------------------------------------------
                           WORDLE PA6
-----------------------------------------------------------------
{body}
-----------------------------------------------------------------
{errMessage + Input}'''
        print(menu, end='')
    
    @staticmethod
    def __clearScreen() -> None:
        os.system('cls' if os.name == 'nt' else 'clear')
