# implementation taken from 
# https://coderbook.com/@marcus/how-to-create-a-hash-table-from-scratch-in-python/

import hashlib

class HashTable(object):
    def __init__(self, length=4):
        # Initiate our array with empty values.
        self.array = [None] * length
    
    def hash(self, key):
        """Get the index of our array for a specific string key"""
        length = len(self.array)
        
        # modified to use hash function from PSI protocol
        h = hashlib.sha256((key).encode('utf-8'))
        return int(h.hexdigest(), 16) % length
        
    def add(self, key, value):
        index = self.hash(key)
        # print(index)
        if self.array[index] is not None:
            for kvp in self.array[index]:
                if kvp[0] == key:
                    kvp[1] = value
                    break
            else:
                self.array[index].append([key, value])
        else:
            self.array[index] = []
            self.array[index].append([key, value])
            # print(self.array[index])
    
    def get(self, key):
        """Get a value by key"""
        index = self.hash(key)
        if self.array[index] is None:
            raise KeyError()
        else:
            for kvp in self.array[index]:
                if kvp[0] == key:
                    return kvp[1]
            raise KeyError()
    def is_full(self):
        """Determines if the HashTable is too populated."""
        items = 0
        for item in self.array:
            if item is not None:
                items += 1
        return items > len(self.array)/2
        
    def double(self):
        """Double the list length and re-add values"""
        ht2 = HashTable(length=len(self.array)*2)
        for i in range(len(self.array)):
            if self.array[i] is None:
                continue
            for kvp in self.array[i]:
                ht2.add(kvp[0], kvp[1])
        self.array = ht2.array