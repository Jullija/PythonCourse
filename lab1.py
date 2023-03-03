import string
# a+b -> infiksowa
# +(a, b) -> prefiksowa
# a b + -> postfiksowa, odwrotna notacja polska, RPN

# Wybieramy ten operator o najmniejszym priorytecie niezagniezdzony w nawiasach będący najbardziej po prawej stronie
# a > b & c -> a b c & >
# a & b > c -> a b & c >
# (a > b) & c -> a b > c & 

#potrzebujemy czegoś, co zamieni infiksową na postfiksową
# """STRING """ - mozna mieć znak nowego wiersza


operators = '&|>'
VAR = string.ascii_lowercase #wszystkie literki

def check(expr):
    bracketsCounter = 0
    state = False # False - oczekiwanie na zmienną lub nawias otwierający; True - oczekiwanie na operator lub nawias zamykający
    
    for i in expr:
        if state:
            if i not in operators + ')':
                return False
            elif i != ')':
                state = not state
        else:
            if i in operators + ')':
                return False
            elif i in VAR:
                state = not state
        
        if i == '(':
            bracketsCounter += 1
        elif i == ')':
            bracketsCounter -= 1

        if bracketsCounter < 0:
            return False
    
    return bracketsCounter == 0 and state


# while True:
#     expr = input(">>")
#     print(check(expr))



def brackets(expr):
    while expr[0] == '(' and expr[-1] == ')' and check(expr[1:-1]):
        expr = expr[1:-1]
    return expr

# najbardziej prawa pozycja danego operatora niezagnieżdżonego w nawiasach
def bal(expr, operator):
    bracketCounter = 0
    for i in range(len(expr)-1, -1):
        if expr[i] == ')':
            bracketCounter += 1
        if expr[i] == '(':
            bracketCounter -= 1
        if expr[i] in operator and bracketCounter == 0:
            return i
    
    return False



def onp(expr):
    expr = brackets(expr)

    p = bal(expr, '>')
    if p:
        return onp(expr[:p])+onp(expr[p+1:])+expr[p]

    p = bal(expr, '&|')
    if p:
        return onp(expr[:p])+onp(expr[p+1:])+expr[p]
    
    return expr


# while True:
#     expr = input(">>")
#     if check(expr):
#         print(onp(expr))
#     else:
#         print("Oj głuptasku")


def map(w, vec):
    #pozbywanie się operatorów -> do pustego łańcucha konkatenuje inne losty
    ang = ''.join(sorted(list(set(w).intersection(set(VAR)))))


