import random
from typing import Any

class ItemExistsException(Exception):
    pass

class NotFoundException(Exception):
    pass

class Node:
    def __init__(self, key=None, data=None):
        self.key = key
        self.data = data
        self.next: Node = None

class Bucket:
    def __init__(self):
        self.head: Node = None
        self.size = 0

    def insert(self, key: Any, data: Any) -> None:
        '''Inserts node into the bucket, if the key already exists a ItemExistsException is raised'''
        if self.head is None:  # bucket is empty
            self.head = Node(key, data)
            self.size += 1
            return

        prev, node = self.__traverseSLL(key)

        if node is not None:
            raise ItemExistsException()  # node already exists with this key

        prev.next = Node(key, data)  # insert new node
        self.size += 1



    def contains(self, key: Any) -> bool:
        '''Returns true iff a node in the bucket exists with the key passed in, else false is returned'''
        _, node = self.__traverseSLL(key)
        return node is not None



    def __traverseSLL(self, key: Any = None) -> tuple[Node]:
        '''Looks for the key entered in a singly linked list. Returns a tuple (previousNode, currentNode) where currentNode has the matching key or None.'''
        if self.head is None:
            return None, None

        cur: Node = self.head
        prev: Node = None

        while cur is not None:
            if cur.key == key:
                return prev, cur
            prev = cur
            cur = cur.next

        return prev, None

class HashMap:
    def __init__(self, size: int = 10):
        self.buckets = [Bucket() for _ in range(size)]
        self.bucketSize = size
        self.size = 0

    def insert(self, key: Any, data: Any) -> None:
        '''Insert Node into the hash map, if key is already in the hashmap then a ItemExistsException is raised'''
        index = self._hash(key)
        try:
            self.buckets[index].insert(key, data)
        except ItemExistsException:
            pass
        
        self.size += 1

        if self.size >= 1.2 * self.bucketSize:  # check if we need to resize the hash map
            self.__rebuild()



    def contains(self, key: Any) -> bool:
        '''Returns true iff there exists a node in the hash map that matches the key passed in, else false'''
        index = self._hash(key)
        return self.buckets[index].contains(key)


    def _hash(self, key: Any):
        return hash(key) % self.bucketSize

    def __rebuild(self):
        '''Resizes the hash map list, creating a new list twice the size of the previous.'''
        self.bucketSize = self.bucketSize * 2
        newBuckets = [Bucket() for _ in range(self.bucketSize)]
        for bucket in self.buckets:
            nodeCurr = bucket.head
            while nodeCurr is not None:
                hashVal = self._hash(nodeCurr.key)
                newBuckets[hashVal].insert(nodeCurr.key, nodeCurr.data)
                nodeCurr = nodeCurr.next
        self.buckets = newBuckets

    def getRandomValue(self) -> Any:
        if self.size == 0:
            raise NotFoundException("HashMap is empty")

        non_empty_buckets = [bucket for bucket in self.buckets if bucket.head is not None]
        chosen_bucket = random.choice(non_empty_buckets)

        rand_index = random.randrange(chosen_bucket.size)
        current = chosen_bucket.head
        for _ in range(rand_index):
            current = current.next
        return current.data


                    
        