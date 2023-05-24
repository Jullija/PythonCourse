import msvcrt
import time

UKLAD = []
num = 0

def NAND(wy,*we):
  UKLAD.append((wy,we))

STAN = {}
STAN['0'] = 0
STAN['1'] = 1

def nand(wy,we):
  for x in we:
    if STAN[x]==0: 
      STAN[wy] = 1
      return
  STAN[wy] = 0 

def inputs():
  if msvcrt.kbhit():
    k = msvcrt.getch().decode('utf-8')
    if k in STAN:
      STAN[k]=1-STAN[k]

def outputs():
  for k in STAN.keys():
    if k in "abcdefghijklmnopqrstuvwxyz":
      print(k,STAN[k],' ',end='')
  print()

def variables(*v):
  for x in v:
    STAN[x] = 0


def pin():
    global num
    num += 1
    v = f'p{num}'
    STAN[v] = 0
    return v


def sim():
  t1 = time.time()

  while True:
    if time.time() - t1 >= 1.0:
        STAN['z'] = 1 - STAN['z']
        t1 = time.time()

    inputs()
    for el in UKLAD:  nand(el[0],el[1])
    outputs()

variables('a','b','c','d')




def NOT(y, x):
    NAND(y, x, x)


def AND(c, a ,b):
    p = pin()
    NAND(p, a, b)
    NOT(c, p)

def XOR(c, a, b):
    p1 = pin()
    p2 = pin()
    p3 = pin()
    NAND(p1, a, b)
    NAND(p2, a, p1)
    NAND(p3, b, p1)
    NAND(c, p2, p3)


def XOR3(d, a ,b, c):
    p = pin()
    XOR(p, a, b)
    XOR(d, c, p)

def rs(a, b, c, d):
    NAND(c, a, d)
    NAND(d, b, c)

def JK(c, j, k, q, nq):
    p1 = pin()
    p2 = pin()
    p3 = pin()
    p4 = pin()
    p5 = pin()
    p6 = pin()
    nc = pin()
    NAND(nc, c)
    NAND(p1, j, c, nq)
    NAND(p2, k, q, c)
    NAND(p3, p1, p4)
    NAND(p4, p2, p3)
    NAND(p5, p3, nc)
    NAND(p6, p4, nc)
    NAND(q, p5, nq)
    NAND(nq, p6, q)

def licznik(c, q0, q1, q2, q3):
    nq0 = pin()
    nq1 = pin()
    nq2 = pin()
    nq3 = pin()
    JK(c, '1', '1', q0, nq0)
    JK(q0, '1', '1', q1, nq1)
    JK(q1, '1', '1', q2, nq2)
    JK(q2, '1', '1', q3, nq3)

def licznik10(c, q0, q1, q2, q3):
    nq0 = pin()
    nq1 = pin()
    nq2 = pin()
    nq3 = pin()
    p = pin()
    JK(c, '1', '1', q0, nq0)
    JK(q0, nq3, '1', q1, nq1)
    JK(q1, '1', '1', q2, nq2)
    JK(q2, p, '1', q3, nq3)
    AND(p, q1, q2)



JK('z', '1', '1', 'c', 'd') # z to zegar
licznik('z', 'd', 'c', 'b', 'a')
#NAND('c','a','b')

sim()
