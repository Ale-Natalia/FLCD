# this should be in lexical analyzer
def isConstant(symbol):
    digits = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    if symbol[0] == "\"":
        return True
    if symbol[0] in digits:
        return True


class SymbolTable(object):
    def __init__(self, size):
        self.__size = size
        self.__table = [[] for _ in range(self.__size)]
        self.__currentPosition = 0

    @property
    def Table(self):
        return self.__table

    @staticmethod
    def asciiSum(symbol):
        """
        Computes the sum of the ASCII values of the characters of the symbol
        :param symbol: the input symbol (str)
        :return: the sum of the ASCII values of the characters of the symbol (int)
        """
        asciiS = 0
        for character in symbol:
            asciiS += ord(character)
        return asciiS

    def hash(self, symbol):
        """
        Hash function based on modulo and size of table
        :param symbol: the input symbol to be hashed (str)
        :return: the hash (int)
        """
        return self.asciiSum(symbol) % self.__size

    def search(self, symbol):
        """
        Searches for a symbol in the symbol table
        :param symbol: the input symbol (str)
        :return: tuple of two integers: the position of the bucket in the table
                 and the position of the symbol in the bucket
                 if the symbol does not exist, the return tuple is (-1, -1)
        """
        position = self.hash(symbol)
        bucket = self.__table[position]
        positionInBucket = 0
        for element in bucket:
            if element == symbol:
                return position, positionInBucket
            positionInBucket += 1
        return -1, -1

    def symbolAtPosition(self, positionInTable, positionInBucket):
        """
        Finds the symbol at a given pair of positions (of the bucket in the table and of the element in the bucket)
        :param positionInTable: the position of the bucket in the table (int)
        :param positionInBucket: the position of the element in the bucket (int)
        :return: the symbol if it was found / False if the
        """
        try:
            return self.__table[positionInTable][positionInBucket]
        except RuntimeError:
            return False

    def add(self, symbol):
        """
        Adds a symbol to the symbol table (the raw add function, without performing checks for existence of symbol)
        :param symbol: the symbol to be added (str)
        :return: The position of the symbol - (int, int) tuple
        """
        position = self.hash(symbol)
        bucket = self.__table[position]
        bucket.append(symbol)
        return position, len(bucket) - 1

    def addSymbolIfNotExists(self, symbol):
        """
        Adds a symbol to the symbol table if it does not already exist in the symbol table
        :param symbol: the symbol to be added (str)
        :return: True if the element was added now/False if not (it already existed) (boolean)
        """
        symbolPosition = self.search(symbol)
        exists = symbolPosition[0]
        if exists == -1:
            position = self.add(symbol)
            return position
        return symbolPosition

    def remove(self, symbol):
        """
        Removes a symbol from the symbol table -> it sets the value to an invalid one
        in order to keep the other positions the same
        :param symbol: the symbol to be removed (str)
        :return: None
        """
        position = self.hash(symbol)
        bucket = self.__table[position]
        positionInBucket = 0
        for element in bucket:
            if element == symbol:
                bucket[positionInBucket] = None
            positionInBucket += 1

    def __str__(self):
        return str(self.__table)
