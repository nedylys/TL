#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TP TL1: implémentation des automates
"""

import sys

###############
# Cadre général

V = set(('.', 'e', 'E', '+', '-')
        + tuple(str(i) for i in range(10)))

class Error(Exception):
    pass

INPUT_STREAM = sys.stdin
END = '\n' # ATTENTION: test_tp modifie la valeur de END

# Initialisation: on vérifie que END n'est pas dans V
def init_char():
    if END in V:
        raise Error('character ' + repr(END) + ' in V')

# Accès au caractère suivant dans l'entrée
def next_char():
    global INPUT_STREAM
    ch = INPUT_STREAM.read(1)
    print(f"Read char: {repr(ch)}")
    # print("@", repr(ch))  # decommenting this line may help debugging
    if ch in V or ch == END:
        return ch
    raise Error('character ' + repr(ch) + ' unsupported')

############
# Question 1 : fonctions nonzerodigit et digit

def nonzerodigit(char):
    assert len(char) <= 1
    # RMQ: on n'utilise pas 1 <= int(char) <= 9 car cela échoue sur la chaîne vide
    return '1' <= char <= '9'

def digit(char):
    assert len(char) <= 1
    return '0' <= char <= '9'


############
# Question 2 : integer et pointfloat sans valeur
int_value=None
def integer_Q2():
    """
    L'automate de integer_Q2
    """
    init_char()
    return integer_Q2_state_0()

def integer_Q2_state_0():
    ch = next_char()
    if ch!=END and ch.isdigit():
        int_value=int(ch)
    if not ch.isdigit():
        return False
    if ch=='0':
        return integer_Q2_state_1(int_value)
    if nonzerodigit(ch):
        return integer_Q2_state_2(int_value)
    if ch==END:
        return False

def integer_Q2_state_1(int_value):
    ch = next_char()
    if ch!=END and ch.isdigit():
        int_value=str(int_value)+ch
        print(int(int_value))
    if ch=='0':
        return integer_Q2_state_1(int_value)
    if ch==END:
        return True
    return False

def integer_Q2_state_2(int_value):
    ch = next_char()
    if ch!=END and ch.isdigit():
        int_value=str(int_value)+ch
        print(int(int_value))
    if digit(ch):
        return integer_Q2_state_2(int_value)
    if ch==END:
        return True
    return False

def pointfloat_Q2():
    init_char()
    return pointfloat_Q2_state_0()

def pointfloat_Q2_state_0():
    ch=next_char()
    if digit(ch):
        return pointfloat_Q2_state_2()
    if ch=='.':
        return pointfloat_Q2_state_1()
    return False

def pointfloat_Q2_state_1():
    ch=next_char()
    if digit(ch):
        return pointfloat_Q2_state_3()
    elif ch==END:
        return False
    return False
def pointfloat_Q2_state_2():
    ch=next_char()
    if digit(ch):
        return pointfloat_Q2_state_2()
    if ch=='.':
        return pointfloat_Q2_state_3()
    elif ch==END:
        return False
    return False
def pointfloat_Q2_state_3():
    ch=next_char()
    if digit(ch):
        return pointfloat_Q2_state_3()
    elif ch==END:
        return True
    return False
    

# Définir ici les fonctions manquantes


############
# Question 5 : integer avec calcul de la valeur
# si mot accepté, renvoyer (True, valeur)
# si mot refusé, renvoyer (False, None)

# Variables globales pour se transmettre les valeurs entre états
int_value = 0
exp_value = 0
pres_e=0


def integer():
    init_char()
    return integer_state_0(),int_value


def integer_state_0():
    global int_value
    ch = next_char()
    if ch!=END and ch.isdigit():
       int_value=int(ch)
    if not ch.isdigit():
        int_value=None
        return False
    if ch=='0':
        return integer_state_1()
    if nonzerodigit(ch):
        return integer_state_2()
    if ch==END:
        int_value=None
        return False 
  
def integer_state_1():
    global int_value
    ch = next_char()
    if ch!=END and ch.isdigit():
       int_value=int(str(int_value)+ch)
    if ch=='0':
        return integer_state_1()
    if ch==END:
        return True
    int_value=None
    return False

def integer_state_2():
    global int_value
    ch = next_char()
    if ch!=END and ch.isdigit():
       int_value=int(str(int_value)+ch)
    if digit(ch):
        return integer_state_2()
    if ch==END:
        return True
    int_value=None
    return False


############
# Question 7 : pointfloat avec calcul de la valeur

def pointfloat():
    global int_value
    global exp_value
    exp_value=0
    int_value='@'
    init_char()
    return pointfloat_state_0()
def pointfloat_state_0():
    global int_value
    global exp_value
    ch=next_char()
    if digit(ch):
        int_value=int(ch)
        return pointfloat_state_2()
    if ch=='.':
        exp_value=0
        return pointfloat_state_1()
    return False,None

def pointfloat_state_1():
    global int_value
    global exp_value
    ch=next_char()
    if digit(ch):
        exp_value=1
        int_value=0
        int_value=int(str(int_value)+ch)
        return pointfloat_state_3()
    return False,None
def pointfloat_state_2():
    global int_value
    global exp_value
    global pres_e
    ch=next_char()
    print(int_value)
    if digit(ch):
        int_value=int(str(int_value)+ch)
        return pointfloat_state_2()
    if ch=='.':
        return pointfloat_state_3()
    if ch=='e' or ch=='E':
        pres_e=1
        return False,None
    return False,None
def pointfloat_state_3():
    global int_value
    global exp_value
    global pres_e
    ch=next_char()
    if digit(ch):
        int_value=int(str(int_value)+ch)
        exp_value+=1
        return pointfloat_state_3()
    if ch==END:
        return True,int_value*10**(-exp_value)
    if ch=='e' or ch=='E':
        pres_e=2
        return False,None
    return False,None

# Définir ici les fonctions manquantes


############
# Question 8 : exponent, exponentfloat et number

# La valeur du signe de l'exposant : 1 si +, -1 si -
sign_value =0
exposant=0
def exponent():
    global int_value
    global exposant
    global sign_value
    int_value=0
    sign_value=0
    exposant=0
    init_char()
    return exponent_state_0()
def exponent_state_0():
    ch=next_char()
    if ch=='e' or ch=='E':
        return exponent_state_1()
    return False,None
def exponent_state_1():
    global exposant
    global sign_value
    ch=next_char()
    if ch=='+':
        if sign_value!=0:
            return False,None
        sign_value=1
        return exponent_state_1()
    if ch=='-':
        if sign_value!=0:
          return False,None
        sign_value=-1
        return exponent_state_1()
    elif digit(ch):
        if sign_value==0:
            sign_value=1
        exposant=int(ch)
        return exponent_state_2()
    return False,None
def exponent_state_2():
    global exposant
    global sign_value
    ch=next_char()
    if ch==END:
        return True,sign_value*exposant
    if digit(ch):
        exposant=int(str(exposant)+ch)
        return exponent_state_2()
    return False,None
def exponentfloat():
    global exp
    global sign_value
    global expf
    init_char()
    exp=0
    expf=0
    return exponentfloat_state_0()

def exponentfloat_state_0():
    global exp
    global sign_value
    global expf
    ch=next_char()
    if ch =='.':
        return exponentfloat_state_1()
    if digit(ch):
        expf=int(ch)
        return exponentfloat_state_2()
    return (False,None)

def exponentfloat_state_1():
    global exp
    global sign_value
    global expf
    ch=next_char()
    if digit(ch):
        expf=float('.'+ch)
        return exponentfloat_state_3()
    return (False,None)

def exponentfloat_state_2():
    global exp
    global sign_value
    global expf
    ch=next_char()
    if digit(ch):
        expf = int(str(expf)+ch)
        return exponentfloat_state_2()
    if ch == '.':
        return exponentfloat_state_3()
    if ch in 'eE':
        return exponentfloat_state_4()
    return (False,None)

def exponentfloat_state_3():
    global exp
    global sign_value
    global expf
    ch=next_char()
    s=0
    if digit(ch):
        if '.' not in str(expf):
            expf=float(str(expf)+'.'+ch)
            return exponentfloat_state_3()
        expf=float(str(expf)+ch)
        return exponentfloat_state_3()
    if ch in 'eE':
        return exponentfloat_state_4()
    return (False,None)

def exponentfloat_state_4():
    global exp
    global sign_value
    global expf
    ch=next_char()
    if ch == '+':
        sign_value=+1
        return exponentfloat_state_5()
    if ch == '-':
        sign_value=-1
        return exponentfloat_state_5()
    if digit(ch):
        exp=int(ch)
        return exponentfloat_state_6()
    return (False,None)

def exponentfloat_state_5():
    global exp
    global sign_value
    global expf
    ch=next_char()
    if digit(ch):
        exp=sign_value*int(str(exp)+ch)
        return exponentfloat_state_6()
    return (False,None)

def exponentfloat_state_6():
    global exp
    global expf
    ch=next_char()
    if digit(ch):
        exp=int(str(exp)+ch)
        return exponentfloat_state_6()
    if ch==END:
        expf=expf*(10**exp)
        return (True,expf)
    return (False,None)
def number():
    global int_value
    global exp_value
    global exposant
    int_value=0
    exp_value=0
    exposant=0
    init_char()
    return number_state_0()
def number_state_0():
    global int_value
    global exp_value
    ch=peek_char()
    if ch=='0':
        int_value=int(ch)
        return number_state_1()
    if nonzerodigit(ch):
        int_value=int(ch)
        return number_state_2()
    if ch=='.':
        return number_state_3()
    return False,None
def number_state_1():
    global int_value
    global exp_value
    ch=next_char()
    if ch=='0':
        int_value=int(str(int_value)+ch)
        return number_state_1()
    if ch==END or ch==' ':
        return True,int_value
    if digit(ch):
        int_value=int(str(int_value)+ch)
        return number_state_5()
    if ch=='E' or ch=='e':
        return number_state_6()
    if ch=='.':
        return number_state_4()
    return False,None
def number_state_2():
  global int_value
  global exp_value
  ch=next_char()
  if ch==END or ch==' ':
    return True,int_value
  if digit(ch):
    int_value=int(str(int_value)+ch)
    return number_state_2()
  if ch=='E' or ch=='e':
    return number_state_6()
  if ch=='.':
    return number_state_4()
  return False,None
def number_state_3():
    global int_value
    global exp_value
    ch=next_char()
    if digit(ch):
        int_value=int(str(int_value)+ch)
        exp_value+=1
        return number_state_4()
    return False,None
def number_state_4():
    global int_value
    global exp_value
    ch=next_char()
    if ch==END or ch==' ':
        return True,int_value*10**(-exp_value)
    if digit(ch):
        int_value=int(str(int_value)+ch)
        exp_value+=1
        return number_state_4()
    if ch=='E' or ch=='e':
        return number_state_6() 
    return False,None
def number_state_5():
    global int_value
    global exp_value
    ch=next_char()
    if nonzerodigit(ch):
        int_value=int(str(int_value)+ch)
        return number_state_5()
    if ch=='E' or ch=='e':
        return number_state_6()
    if ch=='.':
        return number_state_4()
    return False,None
def number_state_6():
    global exponent
    global sign_value
    ch=next_char()
    if digit(ch):
        sign_value=1
        exponent=int(ch)
        return number_state_8()
    if ch=='+':
        sign_value=1
        return number_state_7()
    if ch=='-':
        sign_value=-1
        return number_state_7()
    return False,None
def number_state_7():
    global exponent
    ch=next_char()
    if digit(ch):
        exponent=int(ch)
        return number_state_8()
    return False,None
def number_state_8():
    global exponent
    ch=next_char()
    if digit(ch):
        exponent=int(str(exponent)+ch)
        return number_state_8()
    if ch==END or ch=='_':
        return True,int_value*10**(sign_value*exponent-exp_value)
    return False,None



########################
#####    Projet    #####
########################


V = set(('.', 'e', 'E', '+', '-', '*', '/', '(', ')', ' ')
        + tuple(str(i) for i in range(10)))


############
# Question 10 : eval_exp

def eval_exp():
    ch = next_char()
    if ch=='*':
        n1=eval_exp()
        n2=eval_exp()
        return n1*n2     
    if ch == '+':
        n1 = eval_exp()
        n2 = eval_exp()
        print(n1)
        print(n2)
        return n1 + n2
    if ch=='-':
        n1 = eval_exp()
        n2 = eval_exp()
        return n1 -n2
    if ch=='/':
       n1=eval_exp()
       n2=eval_exp()
       return n1/n2
    _,nbr=number()
    return nbr


############
# Question 12 : eval_exp corrigé

current_char = ''

# Accès au caractère suivant de l'entrée sans avancer
def peek_char():
    global current_char
    if current_char == '':
        current_char = INPUT_STREAM.read(1)
    ch = current_char
    # print("@", repr(ch))  # decommenting this line may help debugging
    if ch in V or ch in END:
        return ch
    raise Error('character ' + repr(ch) + ' unsupported')

def consume_char():
    global current_char
    current_char = ''

def number_2():
    global int_value
    global exp_value
    global exposant
    int_value=0
    exp_value=0
    exposant=0
    init_char()
    return number_2_state_0()
def number_2_state_0():
    global int_value
    global exp_value
    ch=peek_char()
    print(ch+'etat0')
    if ch=='0':
        consume_char()
        int_value=int(ch)
        return number_2_state_1()
    if nonzerodigit(ch):
        consume_char()
        int_value=int(ch)
        return number_2_state_2()
    if ch=='.':
        consume_char()
        return number_2_state_3()
    return False,None
def number_2_state_1():
    global int_value
    global exp_value
    ch=next_char()
    if ch=='0':
        int_value=int(str(int_value)+ch)
        return number_2_state_1()
    if ch==END or ch==' ':
        return True,int_value
    if digit(ch):
        int_value=int(str(int_value)+ch)
        return number_2_state_5()
    if ch=='E' or ch=='e':
        return number_2_state_6()
    if ch=='.':
        return number_2_state_4()
    return False,None
def number_2_state_2():
  global int_value
  global exp_value
  ch=next_char()
  if ch==END or ch==' ':
    return True,int_value
  if digit(ch):
    int_value=int(str(int_value)+ch)
    return number_2_state_2()
  if ch=='E' or ch=='e':
    return number_2_state_6()
  if ch=='.':
    return number_2_state_4()
  return False,None
def number_2_state_3():
    global int_value
    global exp_value
    ch=next_char()
    if digit(ch):
        int_value=int(str(int_value)+ch)
        exp_value+=1
        return number_2_state_4()
    return False,None
def number_2_state_4():
    global int_value
    global exp_value
    ch=next_char()
    if ch==END or ch==' ':
        return True,int_value*10**(-exp_value)
    if digit(ch):
        int_value=int(str(int_value)+ch)
        exp_value+=1
        return number_2_state_4()
    if ch=='E' or ch=='e':
        return number_2_state_6() 
    return False,None
def number_2_state_5():
    global int_value
    global exp_value
    ch=next_char()
    if nonzerodigit(ch):
        int_value=int(str(int_value)+ch)
        return number_2_state_5()
    if ch=='E' or ch=='e':
        return number_state_6()
    if ch=='.':
        return number_2_state_4()
    return False,None
def number_2_state_6():
    global exponent
    global sign_value
    ch=next_char()
    if digit(ch):
        sign_value=1
        exponent=int(ch)
        return number_2_state_8()
    if ch=='+':
        sign_value=1
        return number_2_state_7()
    if ch=='-':
        sign_value=-1
        return number_2_state_7()
    return False,None
def number_2_state_7():
    global exponent
    ch=next_char()
    if digit(ch):
        exponent=int(ch)
        return number_2_state_8()
    return False,None
def number_2_state_8():
    global exponent
    ch=next_char()
    if digit(ch):
        exponent=int(str(exponent)+ch)
        return number_2_state_8()
    if ch==END or ch==' ':
        return True,int_value*10**(sign_value*exponent-exp_value)
    return False,None

def eval_exp_v2():
    ch = peek_char()
    print(ch)
    if ch==' ':
        consume_char()
        return eval_exp_v2()
    if ch=='*':
        consume_char()
        n1=eval_exp_v2()
        n2=eval_exp_v2()
        return n1*n2     
    if ch == '+':
        consume_char()
        n1 = eval_exp_v2()
        n2 = eval_exp_v2()
        return n1 + n2
    if ch=='-':
        consume_char()
        n1 = eval_exp_v2()
        n2 = eval_exp_v2()
        return n1-n2
    if ch=='/':
       consume_char()
       n1=eval_exp_v2()
       n2=eval_exp_v2()
       if n2==0:
           return None
       return n1/n2
    _,nbr=number_2()
    return nbr
#print(eval_exp_v2())

############
# Question 14 : automate pour Lex

operator = set(['+', '-', '*', '/'])

def FA_Lex():
    init_char()
    return FA_Lex_state_0()
def FA_Lex_state_0():
    ch=peek_char()
    if ch in operator or ch==')' or ch=='(':
        return True
    appartient_number,_=number()
    return appartient_number
    


############
# Question 15 : automate pour Lex avec token

# Token
NUM, ADD, SOUS, MUL, DIV, OPAR, FPAR = range(7)
token_value = 0



def FA_Lex_w_token():
    global token_value
    init_char()
    ch=peek_char()
    if ch=='+':
        return True,ADD
    if ch=='-':
        return True,SOUS
    if ch=='*':
        return True,MUL
    if ch=='/':
        return True,DIV
    if ch==')':
        return True,FPAR
    if ch=='(':
        return True,OPAR
    appartient_number,nbr=number()
    token_value=nbr
    return appartient_number,NUM

a=0
# Fonction de test
if __name__ == "__main__" and a==0:
    print("@ Test interactif de l'automate")
    print("@ Vous pouvez changer l'automate testé en modifiant la fonction appelée à la ligne 'ok = ... '.")
    print("@ Tapez une entrée:")
    try:
        #ok = eval_exp_v2() # changer ici pour tester un autre automate sans valeur
        # ok, val = integer() # changer ici pour tester un autre automate avec valeur
        ok, val = True, eval_exp_v2() # changer ici pour tester eval_exp et eval_exp_v2
        if ok:
            print("Accepted!")
            print(val)
            # print("value:", val) # décommenter ici pour afficher la valeur (question 4 et +)
        else:
            print("Rejected!")
            #print(value)
            # print("value so far:", int_value) # décommenter ici pour afficher la valeur en cas de rejet
    except Error as e:
        print("Error:", e)
