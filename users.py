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
        '''read all users into a dictionary, where the usernames are the keys and the values are instances of the account class'''
        userDict = {}
        try:
            with open('users.json', 'r') as file: #
                data: Dict[str, Any] = json.load(file)
                for userName, userData in data.items(): # for all key(username) value(records) pairs in the json file, set the key to username and value to a instance of accounts
                    records = userData["records"]
                    userDict[userName] = account(userName, records)
        except FileNotFoundError:
            pass
        
        return userDict

    def addNewUser(self, userName: str) -> None:
        '''adds a new user to the json file and users.usersDict, if username already exists, a error userNameExists is raised, if username is empty a invalidUserName is raised'''
        if userName in self.usersDict:
            raise userNameExists(f"User '{userName}' already exists.")

        if not userName:
            raise invalidUserName("Username is invalid.")

        new_account = account(userName, [])
        self.usersDict[userName] = new_account # add to the userDict
        self.__saveUsers(userName) # call a function that stores the new user perminently in a json file

    def __saveUsers(self, userName: str) -> None:
        with open('users.json', 'r') as file:
            data: Dict[str, Any] = json.load(file) # load the intire json file

        data[userName] = {"records": []} # add the record to the data and then dump that data into the file again

        with open('users.json', 'w') as file:
            json.dump(data, file, indent=4)
            
    def addNewRecordToUser(self, username: str, wordLength: int, guesses: List[Any],guessesNeeded: int, isWinner: bool) -> None:
        '''adds a new record to the user pased in , if the userName does not exist then nothing is done'''
        with open('users.json', 'r') as file:
            data: Dict[str, Any] = json.load(file) # load the entire file
        
        if username not in data:
            return
        
        if not isWinner: 
            newScore = 0
        else:
            newScore = (wordLength ** 2) / guessesNeeded # SCORE IS CALCULATED WWITH THE FOLLOWING FORMULA

        data[username]['records'].append({ ## add new record to the data
            "wordLength": wordLength,
            "guesses": guesses,
            "guessesNeeded": guessesNeeded,
            "win": isWinner
        })

        if newScore > self.recordScore: # update record score and user record score if it applies
            self.recordScore = newScore
        if newScore > self.usersDict[username].maxScore:
            self.usersDict[username].maxScore = newScore
            
        with open('users.json', 'w') as file: # dump data back into file
            json.dump(data, file, indent=4)
        
        recordScore = newScore  
        newGameKey = f'game {len(self.usersDict[username].scores)}' #update userDict
        self.usersDict[username].scores[newGameKey] = recordScore

class account:
    def __init__(self, userName: str, records: List[Dict[str, Any]]) -> None:
        self.userName: str = userName
        self.scores: Dict[str, float] = self.__getScores(records)
    
    def __getScores(self, records: List[Dict[str, Any]]) -> Dict[str, float]:
        '''all scores are returned for a users records that are passed in, a dictionary is returned with the keys being the games, and values score'''
        if not records: # no records -> empty dict returned
            self.maxScore = 0
            return {}

        recordsDict = {}
        maxScore = 0
        counter = 0 # counter too keep track of games

        for record in records:
            try:
                wordLength = int(record["wordLength"])
                guessesNeeded = int(record["guessesNeeded"])
            except (ValueError, AttributeError):
                continue

            if not record['win']: # if the user didnt win the round the score is auto 0
                score = 0
            else:
                score = (wordLength ** 2) / guessesNeeded # formula used to calculate score

            if score > maxScore:
                maxScore = score

            recordsDict[f'game {counter}'] = score
            counter += 1

        self.maxScore = maxScore
        return recordsDict
