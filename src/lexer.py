import re
from tabulate import tabulate

delimiters=[" ","+","-","*","/","=",";","(",")","[","]","{","}","<",">","!","&","|","^","%","~","?",".",",","'","\""]
keywords=['int','main','begin','end','do','while','return']

kwd_dict={
    "int":"t",
    "main":"m()",
    "begin":"b",
    "end":"d",
    "do":"do",
    "while":"w",
    "return":"r",
    "+":"o",
    "-":"o",
    "*":"o",
    "/":"o",
    "=":"a",
    "expr":"e",
    "exp":"e",
    "n":"id"
}

def isKeyword(token):
    if token in keywords:
        return True
    return False

def isDelimiter(ch):
    if ch in delimiters:
        return True
    return False

print("------------------------ LEXICAL ANALYZER - TOKENIZER -----------------------")
tokentable_global=[]
tokentable_global.append(["Token No","Lexeme","Token","Line No"])
txt=open("question.txt","r") # Located in base directory
tokens=txt.read()
count=0
tkncount=0
delimit_flag=0
program = tokens.split("\n")

for line in program:
    err=0
    prevct=tkncount
    count = count + 1
    tokentable_local=[]
    print(f"At line {count}\nContent: {line}\n")

    tokens=line
    tokens=re.findall(r"[A-Za-z0-9_]+|[0-9]+|[(){}]|\S", tokens)

    print("Tokens found: ")
    tokentable=[]
    tokentable.append(["Lexeme","Token"])
    for token in tokens:
        if isDelimiter(token):
            if token in ["{","}","(",")",";",","]:
                tkncount+=1
                tokentable.append([token,"Delimiter"])
                tokentable_local.append([tkncount,token,"Delimiter",count])
                
            elif token in ["+","-","*","/","="]:
              if token in ["+","-","*","/"]:
                tkncount+=1
                tokentable.append([token,"Arithmetic Operator"])
                tokentable_local.append([tkncount,token,"Arithmetic Operator",count])
                
              elif token in ["="]:
                tkncount+=1
                tokentable.append([token,"Assignment Operator"])
                tokentable_local.append([tkncount,token,"Assignment Operator",count])
                
            else:
                tokentable.append([token,"Invalid Character [Error]"])
                print("Error Recovery: Line Ignored")
                err=1
                break
            continue
        else:

            if isKeyword(token):
                tkncount+=1
                tokentable.append([token,"Keyword"])
                tokentable_local.append([tkncount,token,"Keyword",count])
                
            else:
                if token.isnumeric():
                    tkncount+=1
                    tokentable.append([token,"Number"])
                    tokentable_local.append([tkncount,token,"Number",count])
                    
                else:        
                    if re.match("^[a-zA-Z][a-zA-Z0-9_]*", token) is not None:
                        tkncount+=1
                        tokentable.append([token,"Identifier"])
                        tokentable_local.append([tkncount,token,"Identifier",count])

                    else:
                        tokentable.append([token,"Invalid Character [Error]"])
                        print("Error Recovery: Line Ignored")
                        err=1
                        break
    delimit_flag=0                    
    if err != 1:
      for entry in tokentable_local:
        tokentable_global.append(entry)
    else:
      tkncount=prevct

    print(tabulate(tokentable, headers="firstrow", tablefmt="grid"))
    print("\n----------------------------------------------------")

print("\nGlobal Token Table: ")
print(tabulate(tokentable_global, headers="firstrow", tablefmt="grid"))

# For the parser tool
mth_flag=0
with open('tokens.txt', 'w') as f:
    str_to_load=""
    for token in tokentable_global[1:]:
        if mth_flag > 0:
            mth_flag-=1
            continue
        sym=kwd_dict.get(token[1]) if kwd_dict.get(token[1]) is not None else token[1]
        str_to_load+=str(sym)+" "
        if token[1] == "main":
            mth_flag=2
    f.write(f"{str_to_load}\n")