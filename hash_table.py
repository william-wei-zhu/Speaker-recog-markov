'''
MPCS 51042 S'20: Markov models and hash tables

William Zhu (wzhu4@uchicago.edu)
'''

from map import Map


class Hashtable(Map):
    '''
    This class builds attributes and methods for hashtable.
    '''
    
    def __init__(self, capacity, defVal, loadfactor, growthFactor):
        self._capacity = capacity
        self._cells = [None]*self._capacity 
        self.defVal = defVal 
        self.loadfactor = loadfactor
        self.growthFactor = growthFactor
        self.pair_size = 0

    def _hash(self, key):
        '''
        The hash method takes in a key and returns a hashvalue
        '''
        multiplier = 37 
        hash_value = 0
        for c in key:
            hash_value = (hash_value*multiplier + ord(c)) % self._capacity
        return hash_value
      
    def insert(self, key, value):
        '''
        The insert method takes in a key and a value.
        It inserts the key-value pair in the hashtable.
        '''
        cell_index = self._hash(key)
        self.pair_size += 1
        while self._cells[cell_index] is not None:
            if self._cells[cell_index][0] == key:
                self.pair_size -= 1
                break
            else:
                cell_index += 1
                if cell_index >= self._capacity:
                    cell_index = 0
        self._cells[cell_index] = (key, value, True)  


    def rehashing(self):
        '''
        The rehasing method expand the capacity of the hashtable
        by the growthFactor.
        ''' 
        self._capacity = self._capacity * self.growthFactor
        keys = self.keys()
        values = self.values()
        self._cells = [None]*self._capacity
        for key, value in zip(keys, values):
            self.insert(key, value)

    
    def __getitem__(self,key):
        '''
        Similiar to the __getitem__ method for a Python dictionary, this will 
        return the value associated with key in the map. 
        '''
        cell_index = self._hash(key)
        while self._cells[cell_index] is not None:
            if self._cells[cell_index][0] != key:
                cell_index += 1 
                if cell_index >= self._capacity:
                    cell_index = 0
            else:
                break
        if self._cells[cell_index] is None:
            return self.defVal
        elif self._cells[cell_index][2] == False:
            return self.defVal
        else:
            return self._cells[cell_index][1]



    def __setitem__(self,key,value):
        ''' 
        Similiar to the __setitem__ method for a Python dictionary, this will 
        add or update the key-value pairing inside the map. 
        ''' 
        self.insert(key, value)
        if float(self.pair_size/self._capacity)> self.loadfactor:
            self.rehashing()
        

    def __delitem__(self,key):
        '''
        Similiar to the __delitem__ method for a Python dictionary, this will 
        remove the key-value pairing inside the map. 
        ''' 
        cell_index = self._hash(key)
        while self._cells[cell_index] is not None:
            if self._cells[cell_index][0] != key:
                cell_index += 1 
                if cell_index >= self._capacity:
                    cell_index = 0
            else:
                break
        if self._cells[cell_index] is not None:
            if self._cells[cell_index][0] == key:
                self._cells[cell_index] = (self._cells[cell_index][0], self._cells[cell_index][1], False)
                self.pair_size -= 1


    def __contains__(self, key):
        ''' 
        Similiar to the __contains__ method for a Python dictionary, this will 
        return true if the key-value pairing is inside the map; otherwise, if not
        then return false. 
        '''
        return self.__getitem__(key) != self.defVal

    def keys(self):
        '''
        Returns an iterable object (of your choosing) with all the keys inside 
        the map.
        ''' 
        out = []
        for item in self._cells:
            if item is not None:
                if item[2] == True:
                    out.append(item[0])
        return out 
    
    def values(self):
        ''' 
        Returns an iterable object (of your choosing) with all the values inside
        the map. 
        ''' 
        out = []
        for item in self._cells:
            if item is not None:
                if item[2] == True:
                    out.append(item[1])
        return out

    def __len__(self):
        '''   
           Returns the number items in the map. 
           It needs no parameters and returns an integer.
        ''' 
        return len(self.keys()) 
    
    def __bool__(self):
        '''   
           Returns whether the map is empty or not. 
           it needs no parameters and returns a bool.
        ''' 
        return len(self.keys()) != 0


    def __iter__(self):
        '''   
           Returns an iterator of the objects inside the map. The iterator returns 
           the key-value pair as tuple. 
        ''' 
        return iter(list(zip(self.keys(), self.values())))