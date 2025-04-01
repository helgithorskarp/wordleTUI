import random
from hashMap import HashMap

class NoWordExists(Exception):
    pass

class wordAlreadyExists(Exception):
    pass

class wordNotInDict(Exception):
    pass


class WordleEngine:
    def __init__(self) -> None:
        self.wordDict = self.__readWordBank()
        
    def getWord(self, length: int) -> str:
        '''returns a word from word bank that matches the length entered, A NoWordExists error is raised if nothing is found '''
        try:
            return self.wordDict[length].getRandomValue()
        except NoWordExists:
            raise NoWordExists()
                
    def __readWordBank(self) -> dict:
        wordLengthDict: dict[int, HashMap] = {}

        with open('wordBankLarge.txt', 'r') as file:
            for line in file:
                word = line.strip().lower()
                length = len(word)
                
                if length not in wordLengthDict:
                    wordLengthDict[length] = HashMap()
                
                wordLengthDict[length].insert(word, word)
        
        return wordLengthDict


    def validateGuess(self, word: str, lettersCount: int) -> bool:
        '''validates guess, true is returned if the guess is of correct length and is only letters, else false'''
        if not self.wordDict[lettersCount].contains(word):
            raise wordNotInDict()
            
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

        for i in range(len(secret)): # loop trough word and add a upper case C if letter is in correct position and also subtract from the dictionary
            if guess[i] == secret[i]:
                hint[i] = 'C'
                letterCount[guess[i]] -= 1
                
        for i in range(len(secret)): # loop trough word again, add a lowercase c iff word is in secret and the dictionary number for letter is larger than 0
            if hint[i] != 'C' and guess[i] in letterCount and letterCount[guess[i]] > 0:
                hint[i] = 'c'
                letterCount[guess[i]] -= 1
                
        # ---- Here below I turn the hint genereated into a hint that has colours----
        GREEN = "\033[92m" 
        YELLOW = "\033[93m"
        RESET = "\033[0m" 

        coloredHint = "" 
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
        
        if self.wordDict[len(newWord)].contains(newWord):
            raise wordAlreadyExists()
        
        newWordLength = len(newWord)
        
        try:
            self.wordDict[newWordLength].insert(newWord, newWord) # add word to Worddict
        except KeyError:
            pass
            
        
        # Append the new word to the file
        with open('wordBankLarge.txt', 'a') as file:
            file.write(newWord + '\n')

        
    @staticmethod
    def validateNewWord(word):
        wordLength = len(word)
        return word.isalpha() and 3 <= wordLength <= 8
    


