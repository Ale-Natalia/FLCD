from SymbolTable import SymbolTable

st = SymbolTable(5)
st.addSymbolIfNotExists("val")
st.addSymbolIfNotExists("lav")
st.addSymbolIfNotExists("number")
st.addSymbolIfNotExists("nbremu")
print(st.Table)
print(st.search("lav"))
st.remove("nbremu")
print(st.Table)