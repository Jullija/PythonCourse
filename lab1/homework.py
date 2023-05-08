import string

operators = '&|>^'
VAR = string.ascii_lowercase 


#function to change T into 1 and F into 0
def TFChange(expr):
    for i in range (len(expr)):
        if expr[i] == 'T':
            expr = expr.replace(expr[i], '1')
        elif expr[i] == 'F':
            expr = expr.replace(expr[i], '0')
    
    return expr



def deleteDoubleNegations(expr):
    for i in range (1, len(expr)-1, 1):
        if expr[i] == '~' and expr[i-1] == '~':
            expr = expr.replace('~', '')
    
    return expr


def check(expr):
    bracketsCounter = 0
    state = True # False -oczekiwanie na operator lub nawias zamykający; True - oczekiwanie na zmienną lub nawias otwierający lub znak negacji;
    for i in expr:
        if state:
            if i =='~':
                pass
            else:
                if i not in VAR + '(' + '10':
                    return False
                if i in VAR + '10':
                    state = not state
        else:
            if i == '~':
                return False
            else:
                if i not in operators + ')':
                    return False
                elif i in operators:
                    state = not state

    
    for i in expr:
        if i == '(':
            bracketsCounter += 1
        elif i == ')':
            bracketsCounter -= 1

        if bracketsCounter < 0:
            return False
    
    return bracketsCounter == 0 and not state



def brackets(expr):
    while expr[0] == '(' and expr[-1] == ')' and check(expr[1:-1]):
        expr = expr[1:-1]
    return expr



def bal(expr, operator):
    bracketCounter = 0
    for i in range(len(expr)-1, -1, -1):
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
    if p is not False:
        return onp(expr[:p])+onp(expr[p+1:])+expr[p]

    p = bal(expr, '&|')
    if p is not False:
        return onp(expr[:p])+onp(expr[p+1:])+expr[p]
    
    p = bal(expr, '^')
    if p is not False:
        return onp(expr[:p])+onp(expr[p+1:])+expr[p]
    
    p = bal(expr, '~')
    if p is not False:
        return onp(expr[p+1:])+expr[p]
    
    return expr



def map(w, vec):
    arg = ''.join(sorted(list(set(w).intersection(set(VAR))))) 
    for i in range (len(arg)):
        w = w.replace(arg[i], vec[i])
    return w

    

def val(w):
    stos = []
    for i in range(len(w)):
        if w[i] in '01':
            stos.append(w[i])

        elif w[i] == '~':
            tmp = stos.pop()
            if tmp == '1':
                stos.append('0')
            else:
                stos.append('1')
        
        else:
            tmp1 = stos.pop()
            tmp2 = stos.pop()
            ans = '0'

            if w[i] == '|' and (tmp1 == '1' or tmp2 == '1'):
                ans = '1'
            elif w[i] == '&' and (tmp1 == '1' and tmp2 == '1'):
                ans = '1'
            elif w[i] == '>' and (tmp1 == '1' or tmp2 == '0'):
                ans = '1'
            elif w[i] == '^' and (tmp1 != tmp2):
                ans = '1'
            
            stos.append(ans)

    return stos[0]




def gen(n):
    if n == 0:
        return []

    elif n == 1:
        return [['0'], ['1']]
    
    else:
        sequences = []
        for seq in gen(n-1):
            sequences.append(seq + ['0'])
            sequences.append(seq + ['1'])
    
    return sequences





def tautology(expr):

    expr = TFChange(expr)
    expr = deleteDoubleNegations(expr)

     #check if correct -> change to onp 
    if (check(expr)):
        expr = onp(expr)

        #find all variables
        variables = set()
        for i in range(len(expr)):
            if expr[i] in VAR:
                variables.add(expr[i])
        
        howManyVariables = len(variables)

        #generating all sequences of 01
        sequences = gen(howManyVariables)

        for seq in sequences: 
            #creating a vector
            vec = ''
            for i in range (len(seq)):
                vec += seq[i]
            
            #map the expression to the vector and check the value
            expr = map(expr, vec)
            if val(expr) == '0':
                print("NIE")
                return 

        if len(sequences) == 0:
            if val(expr) == '0':
                print("NIE")
                return
            else:
                print("TAK")
                return
        
        print("TAK")
        return
    
    else:
        print("ERROR")
        return
    
while True:
    expr = input(">>")
    tautology(expr)



