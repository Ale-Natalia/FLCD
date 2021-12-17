import copy
import queue
from collections import deque

from Lab5.Grammar import Grammar


class LL_TableCell:
    def __init__(self, productionRhs=None, productionNumber=None, action=None):
        self.productionRhs = productionRhs
        self.productionNumber = productionNumber
        self.action = action

    def __str__(self):
        return '(' + str(self.productionNumber) + ') ' + str(self.productionRhs) + ': ' + str(self.action)


class LL_Parser(object):
    def __init__(self, grammar:Grammar):
        self.__grammar = grammar
        self.__firstTable = {}
        self.__followTable = {}
        self.__LLTable = {}
        self.EPSILON = "eps"
        self.__inputStack = []
        self.__workStack = []
        self.__productionString = []
        self.__derivationString = []

    def initializeTable(self, table, isFollow=False):
        for nonterminal in self.__grammar.N:
            table.update({nonterminal: set()})
        if isFollow:
            table[self.__grammar.S].add(self.EPSILON)

    def first(self):
        previousFirstTable = {}
        self.initializeTable(previousFirstTable)
        self.initializeTable(self.__firstTable)
        while True:
            for nonterminal in self.__firstTable:
                for productionNumber in self.__grammar.ProductionsLeftToRight[nonterminal]:
                    production = self.__grammar.Productions[productionNumber]
                    productionFirstToken = production.rightHandSide[0]
                    if productionFirstToken in self.__grammar.E or productionFirstToken == self.EPSILON:
                        self.__firstTable[nonterminal].add(productionFirstToken)
                    else:  # it means that the first token of the production is a nonterminal
                        self.__firstTable[nonterminal].update(previousFirstTable[productionFirstToken])
            if previousFirstTable == self.__firstTable:
                break
            previousFirstTable = copy.deepcopy(self.__firstTable)

    def follow(self):
        previousFollowTable = {}
        self.initializeTable(previousFollowTable, True)
        self.initializeTable(self.__followTable, True)
        while True:
            for nonterminal in self.__followTable:
                if nonterminal in self.__grammar.ProductionsRightToLeft:
                    for productionNumber in self.__grammar.ProductionsRightToLeft[nonterminal]:
                        production = self.__grammar.Productions[productionNumber]
                        # look for the nonterminal in the production rhs tokens
                        for index, token in enumerate(production.rightHandSide):
                            if token == nonterminal:
                                # if there is nothing following the nonterminal,
                                # we take the previous iteration of follow for the leftHandSide
                                if index == len(production.rightHandSide) - 1:
                                    self.__followTable[nonterminal].update(previousFollowTable[production.leftHandSide])
                                else:
                                    followingToken = production.rightHandSide[index + 1]
                                    # if the following token is a terminal, we add it
                                    if followingToken in self.__grammar.E:
                                        self.__followTable[nonterminal].add(followingToken)
                                    # if the following token is a nonterminal,
                                    # we add the tokens from the corresponding first table,
                                    # but if epsilon is contained, instead of adding epsilon,
                                    # we take the previous iteration of follow for the leftHandSide
                                    else:
                                        for firstToken in self.__firstTable[followingToken]:
                                            if firstToken != self.EPSILON:
                                                self.__followTable[nonterminal].add(firstToken)
                                            else:
                                                self.__followTable[nonterminal].update(previousFollowTable[production.leftHandSide])
            if previousFollowTable == self.__followTable:
                break
            previousFollowTable = copy.deepcopy(self.__followTable)

    def initializeLLTable(self):
        for row in self.__grammar.N + self.__grammar.E + ['$']:
            self.__LLTable.update({row: {}})
            for column in self.__grammar.E + ['$']:
                self.__LLTable[row].update({column: {}})
                if row == column:
                    if row != '$':
                        self.__LLTable[row][column] = LL_TableCell(action='pop')
                    else:
                        self.__LLTable[row][column] = LL_TableCell(action='acc')
                else:
                    self.__LLTable[row][column] = LL_TableCell(action='err')

    def buildTable(self):
        self.initializeLLTable()
        for nonterminal in self.__grammar.ProductionsLeftToRight:
            for productionIndex in self.__grammar.ProductionsLeftToRight[nonterminal]:
                productionRhs = self.__grammar.Productions[productionIndex].rightHandSide
                productionRhsFirst = productionRhs[0]
                if productionRhsFirst in self.__grammar.E:
                    if self.__LLTable[nonterminal][productionRhsFirst].action != 'err':
                        raise ValueError("There is a conflict at row {}, column {}".format(nonterminal, productionRhsFirst))
                    self.__LLTable[nonterminal][productionRhsFirst] = LL_TableCell(productionRhs=productionRhs, productionNumber=productionIndex)
                elif productionRhsFirst in self.__grammar.N:
                    for terminal in self.__firstTable[productionRhsFirst]:
                        if self.__LLTable[nonterminal][terminal].action != 'err':
                            raise ValueError("There is a conflict at row {}, column {}".format(nonterminal, terminal))
                        if terminal != self.EPSILON:
                            self.__LLTable[nonterminal][terminal] = LL_TableCell(productionRhs=productionRhs, productionNumber=productionIndex)
                        else:
                            for otherTerminal in self.__followTable[nonterminal]:
                                if otherTerminal == self.EPSILON:
                                    otherTerminal = '$'
                                self.__LLTable[nonterminal][otherTerminal] = LL_TableCell(productionRhs=productionRhs, productionNumber=productionIndex)
                elif productionRhsFirst == self.EPSILON:
                    for otherTerminal in self.__followTable[nonterminal]:
                        if otherTerminal == self.EPSILON:
                            otherTerminal = '$'
                        self.__LLTable[nonterminal][otherTerminal] = LL_TableCell(productionRhs=productionRhs,
                                                                                  productionNumber=productionIndex)

    def initializeInputStack(self, sequence):
        self.__inputStack = ['$'] + sequence.split(' ')[::-1]

    def initializeWorkStack(self):
        self.__workStack = ['$', self.__grammar.S]

    def initializeProductionString(self):
        # self.__productionString.append(self.EPSILON)
        pass

    def parseInputSequence(self, sequence):
        self.initializeInputStack(sequence)
        self.initializeWorkStack()
        self.initializeProductionString()
        while True:
            try:
                currentCellTable = self.__LLTable[self.__workStack[-1]][self.__inputStack[-1]]
            except:
                print(self.__inputStack[-1] + " not found in grammar")
                break
            if currentCellTable.action == 'err':
                print("Syntax error!")
                break
            elif currentCellTable.action == 'acc':
                print("Accepted sequence!")
                break
            elif currentCellTable.action == 'pop':
                self.__workStack.pop(-1)
                self.__inputStack.pop(-1)
            elif currentCellTable.action is None:
                self.__workStack.pop(-1)
                if currentCellTable.productionRhs != [self.EPSILON]:
                    self.__workStack += currentCellTable.productionRhs[::-1]
                self.__productionString.append(currentCellTable.productionNumber)

    def buildDerivationString(self):
        for productionNumber in self.__productionString:
            self.__derivationString.append(self.__grammar.Productions[productionNumber])

    def printLLTable(self):
        print("LL Parsing Table")
        for row in self.__LLTable:
            fullRow = ''
            fullRow += '{}: '.format(row)
            for column in self.__LLTable[row]:
                fullRow += '{}: {} ... '.format(column, self.__LLTable[row][column])
            print(fullRow)

    def printFirst(self):
        print("FIRST:")
        print(self.__firstTable)

    def printFollow(self):
        print("FOLLOW:")
        print(self.__followTable)

    def printProductionString(self):
        print(self.__productionString)

#grammar = Grammar("g1.txt")
#grammar = Grammar("g_seminar9.txt")
#grammar = Grammar("g_hw10.txt")
grammar = Grammar("g2.txt", True)
ll_parser = LL_Parser(grammar)
ll_parser.first()
ll_parser.printFirst()
ll_parser.follow()
ll_parser.printFollow()
ll_parser.buildTable()
ll_parser.printLLTable()
ll_parser.parseInputSequence('a * ( a + a )')
ll_parser.printProductionString()
ll_parser.parseInputSequence('a * a ( a + a )')
ll_parser.parseInputSequence('a * ab ( a + a )')
