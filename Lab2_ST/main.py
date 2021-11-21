from SymbolTable import SymbolTable
from Scanner import Scanner

'''
st = SymbolTable(5)
st.addSymbolIfNotExists("val")
st.addSymbolIfNotExists("lav")
st.addSymbolIfNotExists("number")
st.addSymbolIfNotExists("nbremu")
print(st.Table)
print(st.search("lav"))
st.remove("nbremu")
print(st.Table)
'''


scanner = Scanner("lab1b_tokens.txt", "p2.txt")
scanner.scanProgram()
print(scanner.ConstantsSymbolTable)
print(scanner.IdentifiersSymbolTable)
print(scanner.ProgramInternalForm)

"""
scanner = Scanner("lab1b_tokens.txt", "p1.txt")
scanner.scanProgram()
print(scanner.ConstantsSymbolTable)
print(scanner.IdentifiersSymbolTable)
print(scanner.ProgramInternalForm)

scanner = Scanner("lab1b_tokens.txt", "p3.txt")
scanner.scanProgram()
print(scanner.ConstantsSymbolTable)
print(scanner.IdentifiersSymbolTable)
print(scanner.ProgramInternalForm)

scanner = Scanner("lab1b_tokens.txt", "perr.txt")
scanner.scanProgram()
print(scanner.ConstantsSymbolTable)
print(scanner.IdentifiersSymbolTable)
print(scanner.ProgramInternalForm)
"""