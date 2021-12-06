import copy

from Lab5.Grammar import Grammar


class LL_Parser(object):
    def __init__(self, grammar:Grammar):
        self.__grammar = grammar
        self.__firstTable = {}
        self.__followTable = {}
        self.EPSILON = "eps"

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

    def printFirst(self):
        print("FIRST:")
        print(self.__firstTable)

    def printFollow(self):
        print("FOLLOW:")
        print(self.__followTable)

#grammar = Grammar("g1.txt")
grammar = Grammar("g_seminar9.txt")
#grammar = Grammar("g_hw10.txt")
#grammar = Grammar("g2.txt", True)
ll_parser = LL_Parser(grammar)
ll_parser.first()
ll_parser.printFirst()
ll_parser.follow()
ll_parser.printFollow()
