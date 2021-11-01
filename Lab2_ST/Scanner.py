import string
import re
from SymbolTable import SymbolTable
from ProgramInternalForm import ProgramInternalForm


class Scanner(object):
    def __init__(self, tokenFile, programFile):
        self.__tokens = []
        self.__tokenFile = tokenFile
        self.__programFile = programFile
        self.__programTokens = []
        self.__constantsST = SymbolTable(10)
        self.__identifiersST = SymbolTable(10)
        self.__pif = ProgramInternalForm()

        self.__previousToken = None

        self.SIGNS = ["+", "-"]
        self.DIGITS = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
        self.NONZERO_DIGITS = ["1", "2", "3", "4", "5", "6", "7", "8", "9"]
        self.LETTERS = list(string.ascii_letters)
        self.UNDERSCORE = "_"
        self.CHARACTERS = self.DIGITS + self.LETTERS + [self.UNDERSCORE]
        self.BOOLEAN = ["true", "false"]
        self.ARITHMETIC_OPERATORS = ["+", "-", "*", "/", "%", "==", "!=", "=", "+=", "-=", "*=", "/=", "%=", ">", "<",
                                     ">=", "<="]
        self.BOOLEAN_OPERATORS = ["|", "&", "|=", "&="]
        self.OPERATORS = self.ARITHMETIC_OPERATORS + self.BOOLEAN_OPERATORS
        self.SEPARATORS = ["(", ")", "{", "}", "[", "]", ",", ";"]
        self.ALL_SEPARATORS = self.OPERATORS + self.SEPARATORS
        self.RESERVED_WORDS = ["let", "const", "if", "else", "then", "while", "for", "read", "print", "len", "sin", "cos"]
        self.__tokens = self.BOOLEAN + self.OPERATORS + self.SEPARATORS + self.RESERVED_WORDS

    @property
    def ProgramInternalForm(self):
        return self.__pif

    @property
    def ConstantsSymbolTable(self):
        return self.__constantsST

    @property
    def IdentifiersSymbolTable(self):
        return self.__identifiersST

    def scanProgram(self):
        # self.readTokens()
        self.readProgram()
        # self.analyzeLexic()

    def readTokens(self):
        tokenF = open(self.__tokenFile, "r")
        self.__tokens = tokenF.readlines()

    def readProgram(self):
        # currently assumes space always exists as a separator
        programF = open(self.__programFile, "r")
        programLines = programF.readlines()
        for line in programLines:
            lineTokens = line.strip("\n").strip("\t")  # .split(" ")
            self.analyzeLine(lineTokens)
            # self.__programTokens += lineTokens

    def findString(self, line, indexFirstQuote):
        if indexFirstQuote == len(line) - 1:
            return None, None
        constructedString = "\""
        indexEndingQuote = indexFirstQuote + 1
        for character in line[(indexFirstQuote + 1):]:
            if character == '"':
                constructedString += "\""
                return constructedString, indexEndingQuote
            else:
                constructedString += character
            indexEndingQuote += 1
        return None, None

    def findSeparator(self, character, line, indexCharacter):
        shortSeparatorFound = None
        longSeparatorFound = None
        for separator in self.ALL_SEPARATORS:
            if character == separator[0]:
                if len(separator) == 1:
                    shortSeparatorFound = separator
                elif len(separator) == 2:
                    if indexCharacter < len(line) - 1:
                        if line[indexCharacter + 1] == separator[1]:
                            longSeparatorFound = separator
        if longSeparatorFound is not None:
            return longSeparatorFound, indexCharacter + 1
        return shortSeparatorFound, indexCharacter

    def analyzeLine(self, line):
        resultedTokens = []
        currentToken = ""
        index = 0
        while index < len(line):
            character = line[index]
            if character == ' ':
                if currentToken not in [' ', '']:
                    valid = self.analyzeToken(currentToken)
                    if not valid:
                        raise ValueError("Lexical error at line {}, index {}".format(line, index))
                currentToken = ""
                index += 1
                continue
            if character == '"':
                foundString, indexEndingQuote = self.findString(line, index)
                if foundString is None:
                    raise ValueError("Invalid token at line {}, index {}".format(line, index))
                self.addConstant(foundString)
                index = indexEndingQuote + 1
                currentToken = ""
                continue
            separator, indexEndOfSeparator = self.findSeparator(character, line, index)
            if separator is not None:
                if currentToken not in [' ', '']:
                    valid = self.analyzeToken(currentToken)
                    if not valid:
                        raise ValueError("Lexical error at line {}, index {}".format(line, index))
                self.__pif.add(separator, -1)
                index = indexEndOfSeparator + 1
                currentToken = ""
                continue
            currentToken += character
            index += 1

    def analyzeLexic(self):
        for token in self.__programTokens:
            self.analyzeToken(token)

    def isInteger(self, token):
        return re.match(r'^[+-]?[1-9][0-9]*$|0', token)

    def isFloat(self, token):
        return re.match(r'^(^[+-]?[1-9][0-9]*$|0)\.[0-9]+$', token)

    def isBoolean(self, token):
        return token in self.BOOLEAN

    def isString(self, token):
        if len(token) < 2:
            return False
        if token[0] == "\"" and token[-1] == "\"":
            return True
        return False

    def isConstant(self, token):
        return self.isInteger(token) or self.isBoolean(token) or self.isFloat(token) or self.isString(token)

    def isIdentifier(self, token):
        return re.match('^([a-zA-Z_])+([a-zA-Z_0-9])*$', token)

    def addConstant(self, token):
        position = self.__constantsST.addSymbolIfNotExists(token)
        self.__pif.add("const", position)

    def addIdentifier(self, token):
        position = self.__identifiersST.addSymbolIfNotExists(token)
        self.__pif.add("id", position)

    def analyzeToken(self, token):
        if token in self.__tokens:
            self.__pif.add(token, -1)
            return True
        elif self.isIdentifier(token):
            self.addIdentifier(token)
            return True
        elif self.isConstant(token):
            if self.isString(token):
                self.addConstant("\"{}\"".format(token))
            else:
                self.addConstant(token)
            return True
        else:
            return False
