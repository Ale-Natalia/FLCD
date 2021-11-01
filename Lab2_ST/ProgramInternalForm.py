class PIFEntry:
    def __init__(self, tokenType, position):
        self.tokenType = tokenType
        self.position = position

    def __str__(self):
        return str(self.tokenType) + " " + str(self.position)


class ProgramInternalForm:
    def __init__(self):
        self.__table = []

    def add(self, tokenType, position):
        self.__table.append(PIFEntry(tokenType, position))

    def __str__(self):
        strResult = " "
        for pifEntry in self.__table:
            strResult += str(pifEntry) + "\n"
        return strResult
