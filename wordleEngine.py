import random

class NoWordExists(Exception):
    pass


class WordleEngine:
    def __init__(self) -> None:
        self.wordDict = self.__readWordBank()
        
    def getWord(self, length: int) -> str:
        '''returns a word from word bank that matches the length entered, A NoWordExists error is raised if nothing is found '''
        try:
            return random.choice(self.wordDict[length])
        except (KeyError, IndexError):
            raise NoWordExists()
                
    def __readWordBank(self) -> dict:
        '''Reads from word bank into a dictionary where keys are word lengths and values are a list of words'''
        words = {}
        with open('wordBank.txt', 'r') as file:
            for word in file:
                cleanedWord = word.strip().lower()
                wordLength = len(cleanedWord)
                if wordLength in words: # word length key exists, append to that list
                    if cleanedWord not in words[wordLength]:
                        words[wordLength].append(cleanedWord)
                else:
                    words[wordLength] = [cleanedWord] # word key does not exist, create new word lenght key
        return words

    @staticmethod
    def validateGuess(word: str, lettersCount: int) -> bool:
        '''validates guess, true is returned if the guess is of correct length and is only letters, else false'''
        return len(word) == lettersCount and word.isalpha()
    
    @staticmethod
    def generateHint(secret: str, guess: str) -> str:
        '''Generates a wordle hint, C is in correct position, c not correct position, - not in word'''
        secret, guess = secret.lower(), guess.lower()
        hint = ['-'] * len(secret)
        letterCount = {}

        for ch in secret: # dictionary that counts how many times each letter appears
            if ch in letterCount:
                letterCount[ch] += 1
            else:
                letterCount[ch] = 1

        for i in range(len(secret)): # loop trough word and add a C if letter is in correct position and also subtract from the dictionary
            if guess[i] == secret[i]:
                hint[i] = 'C'
                letterCount[guess[i]] -= 1

        for i in range(len(secret)): # loop trough word again, add a lowercase c iff word is in secret and the dictionary number for letter is larger than 0
            if hint[i] != 'C' and guess[i] in letterCount and letterCount[guess[i]] > 0:
                hint[i] = 'c'
                letterCount[guess[i]] -= 1

        # Color codes 
        GREEN = "\033[92m"
        YELLOW = "\033[93m"
        RESET = "\033[0m"

        coloredHint = "" # loop trough the hint to create a colored hint
        for ch in hint:
            if ch == 'C':
                coloredHint += f"{GREEN}C{RESET}"
            elif ch == 'c':
                coloredHint += f"{YELLOW}c{RESET}"
            else:
                coloredHint += ch

        return coloredHint
    
    @staticmethod
    def isWinner(wordHint: str, letterCount: int) -> bool:
        '''returns true iff the word hint is all upper case green C's'''
        GREEN_C = "\033[92mC\033[0m" # this is basically what a green C represents, word is correct if it is this times the word length
        return wordHint == GREEN_C * letterCount

    def validateWordLength(self, value: str) -> bool:
        'validates the word length of a game, returns true iff word length is 3-8 '
        if not value.isdigit():
            return False
        length = int(value)
        return 3 <= length <= 8

    def validateGuessCount(self, value: str) -> bool:
        '''validates the number passed for a guess count, number must be a digit and be 1-10'''
        if not value.isdigit():
            return False
        count = int(value)
        return 1 <= count <= 10
    
    
    def addNewWord(self, newWord):
        '''new word is added to the word bank, if word is empty then nothing is returned'''
        if not newWord: 
            return
        
        newWordLength = len(newWord)
        
        try:
            self.wordDict[newWordLength].append(newWord) # add word to dict
        except KeyError:
            self.wordDict[newWordLength] = [newWord]
            
        
        with open('wordBank.txt', 'w') as file: # rewrite all words into the file includin the new word, 
            for key in self.wordDict:
                for word in self.wordDict[key]:
                    file.write(word + '\n')
    
    @staticmethod
    def validateNewWord(word):
        wordLength = len(word)
        return word.isalpha() and 3 <= wordLength <= 8



