print()
print("------------Iter----------------------")
print()
lista = ["ala","ola", "ula"]
myit = iter(lista)
print(next(myit)) 
print(next(myit)) 
print(next(myit))

print()
print("------------MyNumbers----------------------")
print()

class MyNumbers:
  def __iter__(self):
    self.a = 1
    return self
  def __next__(self):
    x = self.a
    self.a += 1
    return x
myclass = MyNumbers()
myiter = iter(myclass)
print(next(myiter)) 
print(next(myiter)) 
print(next(myiter)) 
print(next(myiter)) 
print(next(myiter))

print()
print("------------Funkcja generująca----------------------")
print()

def podz(n): 
#”Funkcja generująca podzielniki właściwe liczby n” 
    for p in range(1,n):
        if n%p==0:
            yield p


for i in podz(120):
    print(i)


l = [ x for x in podz(24) ]
print(l)

print()
print("------------Generator----------------------")
print()

g = podz(24) #to jest generator
print(g)

print()
print("------------Wyrazenie generujace----------------------")
print()

n = 24
g = (p for p in range(1,n) if n%p==0)
print(g)

print()
print("------------Generator nieskończony----------------------")
print()

def fib():
    #”Funkcja generująca kolejne wyrazy ciągu Fibonacciego” 
    a,b = 1,1
    while True:
        yield a
        a,b = b,a+b

suma = 0
for w in fib():
    print(w)
    suma += w
    if suma>10000:
        break

print()
print("------------Liczby pierwsze----------------------")
print()

def primes():
#"Funkcja generuje kolejne liczby pierwsze" 
    lp = [2]
    p=2
    yield p
    while True:
        p += 1
        for d in lp:
            if p%d==0: break
        else:
            lp.append(p)
            yield p 
mem = -100
for w in primes():
    if w > 20000:
        break
    if w-mem == 2:
        print(mem,w) # to są liczby bliźniacze
    mem = w

print()
print("------------Liczby bliźniacze----------------------")
print()



def twins():
#"""Funkcja generuje kolejne liczby bliźniacze
#   ale gubi jedną parę"""
  g = primes()
  while True:
    w1 = next(g)
    w2 = next(g)
    if w2-w1==2:
      yield w1,w2


for a,b in twins():
  print(a,b)


print()
print("------------Generator rekurencyjny----------------------")
print()



def gen(n):
  if n==0:
    yield ""
  else:
    for c in gen(n-1):
      yield c+'0'
      yield c+'1'



print()
print("------------Permutacje----------------------")
print()

import string
VAR = string.ascii_lowercase

def perm(s):
#”Funkcja generuje permutacje liter w napisie s” 
    if len(s)==1:
        yield s 
    else:
        for p in perm(s[:-1]):
            for i in range(len(s)):
                yield p[:i]+s[-1]+p[i:]

for a in perm('ABCD'):
  print(a)


print()
print("------------Kombinacje----------------------")
print()


def komb(s,k):
#”Funkcja generuje k-elementowe kombinacje z napisu s”
    if k==1:
        for x in s: yield x
    elif len(s)==k:
        yield s
    else:
        for x in komb(s[1:],k): yield x
        for x in komb(s[1:],k-1): yield s[0]+x
    
for a in komb('ABCDE',3):
  print(a)
