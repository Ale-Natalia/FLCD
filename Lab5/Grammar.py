class Grammar(object):
    def __init__(self, fileGrammar):
        self.__fileGrammar = fileGrammar
        self.__N = []
        self.__E = []
        self.__S = None
        self.__P = {}
        self.__readGrammar()

    @staticmethod
    def stringToList(inputString):
        if len(inputString) < 2:
            raise ValueError("{} is too short to be a list".format(inputString))
        if inputString[0] != "[" or inputString[-1] != "]":
            raise ValueError("{} must be of shape [elem1,elem2,...,elemn]".format(inputString))
        if len(inputString) == 2:
            return []
        elements = inputString[1:-1].split(",")
        return elements

    def checkCFG(self, nonterminal, productions):
        if nonterminal not in self.__N:
            raise ValueError("{} is not a non-terminal, so this is not a context-free grammar")
        for production in productions:
            for character in production:
                if character not in self.__N and character not in self.__E:
                    raise ValueError("Not found")

    def __readGrammar(self):
        contentGrammar = open(self.__fileGrammar, "r")
        linesGrammar = contentGrammar.readlines()
        if len(linesGrammar) < 4:
            raise ValueError("Not enough content to build Grammar or wrong format")
        self.__N = linesGrammar[0].strip("\n").split("=")[1].split(",")
        self.__S = self.__N[0]
        self.__E = linesGrammar[1].strip("\n").split("=")[1].split(",")
        p = linesGrammar[2].strip("\n")
        if p != "P:":
            raise ValueError("Should have P: on the 3rd row")
        for line in linesGrammar[3:]:
            nonterminal, productions = line.strip("\n").split("=")
            productions = productions.split("|")
            self.checkCFG(nonterminal, productions)
            self.__P.update({nonterminal: productions})

    def printProductions(self):
        firstRow = "P:\n"
        print(firstRow)
        for production in self.__P:
            print(production, "->", self.__P[production])

    def productionsForNonterminal(self, nonterminal):
        print(self.__P[nonterminal])

    def menu(self):
        print("Menu for Grammar elements:\n")
        print("1. Set of nonterminals")
        print("2. Set of terminals")
        print("3. Set of productions")
        print("4. Productions for given nonterminal")
        while True:
            option = int(input("Type in your option: "))
            if option == 1:
                print(self.__N)
            elif option == 2:
                print(self.__E)
            elif option == 3:
                self.printProductions()
            elif option == 4:
                nonterminal = input("nonterminal:")
                self.productionsForNonterminal(nonterminal)
            else:
                break


grammar = Grammar("g1.txt")
grammar.menu()
