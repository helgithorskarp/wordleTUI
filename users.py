import json
from typing import Dict, List, Any

class userNameExists(Exception):
    pass

class invalidUserName(Exception):
    pass

class Users:
    def __init__(self) -> None:
        self.usersDict: Dict[str, "account"] = self.__readAllUsers()
        
        if self.usersDict:
            self.recordScore: float = max(account.maxScore for account in self.usersDict.values())
        else:
            self.recordScore = 0

    def __readAllUsers(self) -> Dict[str, "account"]:
        userDict = {}
        try:
            with open('users.json', 'r') as file:
                data: Dict[str, Any] = json.load(file)
                for userName, userData in data.items():
                    records = userData["records"]
                    userDict[userName] = account(userName, records)
        except FileNotFoundError:
            pass
        
        return userDict

    def addNewUser(self, userName: str) -> None:
        if userName in self.usersDict:
            raise userNameExists(f"User '{userName}' already exists.")

        if not userName:
            raise invalidUserName("Username is invalid.")

        new_account = account(userName, [])
        self.usersDict[userName] = new_account
        self.__saveUsers(userName)

    def __saveUsers(self, userName: str) -> None:
        with open('users.json', 'r') as file:
            data: Dict[str, Any] = json.load(file)

        data[userName] = {"records": []}

        with open('users.json', 'w') as file:
            json.dump(data, file, indent=4)
            
    def addNewRecordToUser(self, username: str, wordLength: int, guesses: List[Any],
                           guessesNeeded: int, isWinner: bool) -> None:
        with open('users.json', 'r') as file:
            data: Dict[str, Any] = json.load(file)
        
        if username not in data:
            return
        
        if not isWinner:
            newScore = 0
        else:
            newScore = (wordLength ** 2) / guessesNeeded

        data[username]['records'].append({
            "wordLength": wordLength,
            "guesses": guesses,
            "guessesNeeded": guessesNeeded,
            "win": isWinner
        })

        if newScore > self.recordScore:
            self.recordScore = newScore
        if newScore > self.usersDict[username].maxScore:
            self.usersDict[username].maxScore = newScore
            
        with open('users.json', 'w') as file:
            json.dump(data, file, indent=4)
        
        recordScore = newScore  
        newGameKey: str = f'game {len(self.usersDict[username].scores)}'
        self.usersDict[username].scores[newGameKey] = recordScore

class account:
    def __init__(self, userName: str, records: List[Dict[str, Any]]) -> None:
        self.userName: str = userName
        self.scores: Dict[str, float] = self.__getScores(records)
    
    def __getScores(self, records: List[Dict[str, Any]]) -> Dict[str, float]:
        if not records:
            self.maxScore = 0
            return {}

        recordsDict = {}
        maxScore = 0
        counter = 0

        for record in records:
            try:
                wordLength = int(record["wordLength"])
                guessesNeeded = int(record["guessesNeeded"])
            except (ValueError, AttributeError):
                continue

            if not record['win']:
                score = 0
            else:
                score = (wordLength ** 2) / guessesNeeded

            if score > maxScore:
                maxScore = score

            recordsDict[f'game {counter}'] = score
            counter += 1

        self.maxScore = maxScore
        return recordsDict
