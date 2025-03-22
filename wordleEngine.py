import random

class NoWordExists(Exception):
    pass


class WordleEngine:
    def __init__(self) -> None:
        self.wordDict = self.__readWordBank()
        
    def getWord(self, length: int) -> str:
        try:
            return random.choice(self.wordDict[length])
        except (KeyError, IndexError):
            raise NoWordExists()
                
    def __readWordBank(self) -> dict:
        words = {}
        with open('wordBank.txt', 'r') as file:
            for word in file:
                cleanedWord = word.strip().lower()
                wordLength = len(cleanedWord)
                if wordLength in words:
                    if cleanedWord not in words[wordLength]:
                        words[wordLength].append(cleanedWord)
                else:
                    words[wordLength] = [cleanedWord]
        return words

    @staticmethod
    def validateGuess(word: str, lettersCount: int) -> bool:
        return len(word) == lettersCount and word.isalpha()
    
    @staticmethod
    def generateHint(secret: str, guess: str) -> str:
        secret, guess = secret.lower(), guess.lower()
        hint = ['-'] * len(secret)
        letterCount = {}
        for ch in secret:
            if ch in letterCount:
                letterCount[ch] += 1
            else:
                letterCount[ch] = 1
                
        for i in range(len(secret)):
            if guess[i] == secret[i]:
                hint[i] = 'C'
                letterCount[guess[i]] -= 1
                
        for i in range(len(secret)):
            if hint[i] != 'C' and guess[i] in letterCount and letterCount[guess[i]] > 0:
                hint[i] = 'c'
                letterCount[guess[i]] -= 1
        return "".join(hint)
    
    @staticmethod
    def isWinner(wordHint: str, letterCount: int) -> bool:
        return wordHint == 'C' * letterCount
    
    def validateWordLength(self, value: str) -> bool:
        if not value.isdigit():
            return False
        length = int(value)
        return 3 <= length <= 8

    def validateGuessCount(self, value: str) -> bool:
        if not value.isdigit():
            return False
        count = int(value)
        return 1 <= count <= 10
    
    
    def addNewWord(self, newWord):
        if not newWord:
            return
        
        newWordLength = len(newWord)
        
        try:
            self.wordDict[newWordLength].append(newWord)
        except KeyError:
            self.wordDict[newWordLength] = [newWord]
            
        
        with open('wordBank.txt', 'w') as file:
            for key in self.wordDict:
                for word in self.wordDict[key]:
                    file.write(word + '\n')
    
    @staticmethod
    def validateNewWord(word):
        wordLength = len(word)
        return word.isalpha() and 3 <= wordLength <= 8



n = WordleEngine()

n.addNewWord('messi')