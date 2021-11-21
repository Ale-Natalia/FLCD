class FA(object):
    def __init__(self, fileFA):
        self.__fileFA = fileFA
        self.__Q = []
        self.__S = []
        self.__Spositions = {}
        self.__F = []
        self.__q0 = "q0"
        self.__delta = {}
        self.__CORRESPONDENCES = {"Q": self.__Q, "S": self.__S, "F": self.__F}
        self.__readFA()

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

    def __readFA(self):
        contentFA = open(self.__fileFA, "r")
        linesFA = contentFA.readlines()
        if len(linesFA) < 4:
            raise ValueError("Not enough content to build FA or wrong format")
        qsf = linesFA[:3]
        for line in qsf:
            line = line.strip("\n").strip("\t")
            try:
                component, value = line.split("=")
            except ValueError:
                raise ValueError("{} is supposed to have only one = sign".format(line))
            if component not in self.__CORRESPONDENCES:
                raise ValueError("No component named {}".format(component))
            # self.__CORRESPONDENCES[component] = self.stringToList(value)
            if component == 'Q':
                self.__Q = self.stringToList(value)
                self.__q0 = self.__Q[0]
            elif component == 'S':
                self.__S = self.stringToList(value)
                for i in range(len(self.__S)):
                    alphabetElem = self.__S[i]
                    self.__Spositions.update({alphabetElem: i})
            elif component == 'F':
                self.__F = self.stringToList(value)
        print(self.__CORRESPONDENCES)
        delta = linesFA[3].strip("\n")
        if delta != "delta":
            raise ValueError("Should have delta on the 4th row")
        for line in linesFA[4:]:
            state, targetStates = line.strip("\n").split(":")
            targetStates = targetStates.split(";")
            for targetStateIndex in range(len(targetStates)):
                targetState = targetStates[targetStateIndex]
                targetStates[targetStateIndex] = self.stringToList(targetState)
            self.__delta.update({state: targetStates})

    def acceptSequence(self, sequence):
        currentState = self.__q0
        for char in sequence:
            if char not in self.__S:
                return False
            positionOfChar = self.__Spositions[char]
            try:
                targetState = self.__delta[currentState][positionOfChar][0]
            except IndexError:  # it means this character cannot be reached from the current state
                return False
            if targetState in self.__F:
                return True
            currentState = targetState
        return False

    def printTransitions(self):
        firstRow = "delta"
        for el in self.__S:
            firstRow += "  {}  ".format(el)
        print(firstRow)
        for transition in self.__delta:
            print(transition, self.__delta[transition])

    def menuFA(self):
        print("Menu for Finite Automata elements:\n")
        print("1. Set of states")
        print("2. Alphabet")
        print("3. Transitions")
        print("4. Final States")
        while True:
            option = int(input("Type in your option: "))
            if option == 1:
                print(self.__Q)
            elif option == 2:
                print(self.__S)
            elif option == 3:
                self.printTransitions()
            elif option == 4:
                print(self.__F)
            else:
                break


fa = FA("FA.in")
fa.menuFA()
print(fa.acceptSequence("100"))
print(fa.acceptSequence("1001"))
#fa.readFA()

