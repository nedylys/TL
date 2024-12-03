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
    # print("@", repr(ch))  # decommenting this line may help debugging
    if ch in V or ch == END:
        return ch
    raise Error('character ' + repr(ch) + ' unsupported')

############
# Question 1 : fonctions nonzerodigit et digit

def nonzerodigit(char):
    assert (len(char) <= 1)
    # RMQ: on n'utilise pas 1 <= int(char) <= 9 car cela échoue sur la chaîne vide
    return '1' <= char <= '9'

def digit(char):
    assert (len(char) <= 1)
    return '0' <= char <= '9'


############
# Question 2 : integer et pointfloat sans valeur
int_value=None
def integer_Q2():
    init_char()
    return integer_Q2_state_0()

def integer_Q2_state_0():
    ch = next_char()
    if ch!=END and ch.isdigit():
        int_value=int(ch)
        print(int_value)
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

def pointfloat_Q2(int_value):
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
val_finale=int_value*10**(-exp_value)

def integer():
    init_char()
    return integer_state_0(),int_value


def integer_state_0():
    global int_value
    ch = next_char()
    if ch!=END and ch.isdigit():
       int_value=int(ch)
       print(int_value)
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
       print(int_value)
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
       print(int_value)
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
    global val_finale
    init_char()
    return pointfloat_Q2_state_0(),int_value
def pointfloat_state_0():
    global int_value
    global exp_value
    global val_finale
    ch=next_char()
    if digit(ch):
        int_value=int(ch)
        print(int_value)
        print(val_finale)
        return pointfloat_state_2()
    if ch=='.':
        exp_value=0
        return pointfloat_state_1()
    val_finale=None
    return False

def pointfloat_state_1():
    global int_value
    global exp_value
    global val_finale
    ch=next_char()
    if digit(ch):
        int_value=int(str(int_value)+ch)
        return pointfloat_state_3()
    val_finale=None
    return False
def pointfloat_state_2():
    global int_value
    global exp_value
    global val_finale
    ch=next_char()
    cpt=0
    if digit(ch):
        int_value=int(str(int_value)+ch)
        print(int_value)
        print(val_finale)
        return pointfloat_state_2()
    if ch=='.':
        cpt+=1
        exp_value=cpt
        print(val_finale)
        return pointfloat_state_3()
    val_finale=None
    return False
def pointfloat_state_3():
    global int_value
    global exp_value
    global val_finale
    ch=next_char()
    if digit(ch):
        int_value=int(str(int_value)+ch)
        print(int_value)
        print(val_finale)
        return pointfloat_state_3()
    elif ch==END:
        return True
    val_finale=None
    return False

# Définir ici les fonctions manquantes


############
# Question 8 : exponent, exponentfloat et number

# La valeur du signe de l'exposant : 1 si +, -1 si -
sign_value =0
exposant=0
exponentfloat=0
def exponent():
    global exposant
    global sign_value
    sign_value =0
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
def exponent_float():
    init_char()
    return exponent_float_state_0()
def exponent_float_state_0():
    global exponentfloat
    ch=next_char()
    if pointfloat_Q2(ch) or digit(ch):
        exponentfloat=float(ch)
        return exponent_float_state_1()
    return False
def exponent_float_state_1():
    global exponentfloat
    ch=next_char()
    if ch=='e' or ch=='E':
        return exponent_float_state_2()
    if digit(ch):
        exponentfloat=float(str(exponentfloat)+ch)
        return exponent_float_state_1()
    return False
def exponent_float_state_2():
    global exposant
    global sign_value
    global expo
    ch=next_char()
    if ch=='+' :
        sign_value=1
        return exponent_float_state_2()
    if ch=='-':
        sign_value=-1
        return exponent_float_state_2()
    elif digit(ch):
        exposant=int(ch)
        return exponent_float_state_3()
    return False
def exponent_float_state_3():
    global exposant
    ch=next_char()
    if ch==END:
        if sign_value==1:
            print(exponentfloat*10**exposant)
        else:
            print(exponentfloat*10**(-exposant))
        return True
    if digit(ch):
        exposant=int(str(exposant)+ch)
        return exponent_float_state_3()
    return False
def number():
    init_char()
    return number_state_0()
def number_state_0():
    ch=next_char()
    if ch=='0':
        return number_state_1()
    if nonzerodigit(ch):
        return number_state_2()
    if ch=='.':
        return number_state_3()
    return False
def number_state_1():
    ch=next_char()
    if ch=='0':
        return number_state_1()
    if ch==END or ch=='_':
        return True
    if digit(ch):
        return number_state_5()
    if ch=='E' or ch=='e':
        return number_state_6()
    if ch=='.':
        return number_state_4()
    return False
def number_state_2():
  ch=next_char()
  if ch==END or ch=='_':
    return True
  if nonzerodigit(ch):
    return number_state_2()
  if ch=='E' or ch=='e':
    return number_state_6()
  if ch=='.':
    return number_state_4()
  return False
def number_state_3():
    ch=next_char()
    if nonzerodigit(ch):
        return number_state_4()
    return False
def number_state_4():
    ch=next_char()
    if ch==END or ch=='_':
        return True
    if nonzerodigit(ch):
        return number_state_4()
    if ch=='E' or ch=='e':
        return number_state_6() 
    return False
def number_state_5():
    ch=next_char()
    if nonzerodigit(ch):
        return number_state_5()
    if ch=='E' or ch=='e':
        return number_state_6()
    if ch=='.':
        return number_state_4()
    return False
def number_state_6():
    ch=next_char()
    if nonzerodigit(ch):
        return number_state_8()
    if ch=='+' or ch=='-':
        return number_state_7()
    return False
def number_state_7():
    ch=next_char()
    if nonzerodigit(ch):
        return number_state_8()
    return False
def number_state_8():
    ch=next_char()
    if nonzerodigit(ch):
        return number_state_8()
    if ch==END or ch=='_':
        return True
    return False



########################
#####    Projet    #####
########################


V = set(('.', 'e', 'E', '+', '-', '*', '/', '(', ')', ' ')
        + tuple(str(i) for i in range(10)))


############
# Question 10 : eval_exp

def eval_exp():
    ch = next_char()
    if ch=='':
        n1=eval_exp()
        n2=eval_exp()
        return n1*n2     
    if ch == '+':
        n1 = eval_exp()
        n2 = eval_exp()
        return n1 + n2
    if ch=='-':
        n1 = eval_exp()
        n2 = eval_exp()
        return n1 -n2
    if ch=='/':
       n1=eval_exp()
       n2=eval_exp()
       return n1/n2
    print(ch)
    return number()
eval_exp()

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


def number_v2():
    print("@ATTENTION: number_v2 à finir !") # LIGNE A SUPPRIMER


def eval_exp_v2():
    print("@ATTENTION: eval_exp_v2 à finir !") # LIGNE A SUPPRIMER


############
# Question 14 : automate pour Lex

operator = set(['+', '-', '*', '/'])

def FA_Lex():
    print("@ATTENTION: FA_lex à finir !") # LIGNE A SUPPRIMER


############
# Question 15 : automate pour Lex avec token

# Token
NUM, ADD, SOUS, MUL, DIV, OPAR, FPAR = range(7)
token_value = 0



def FA_Lex_w_token():
    print("@ATTENTION: FA_lex_w_token à finir !") # LIGNE A SUPPRIMER



# Fonction de test
if __name__ == "__main__":
    print("@ Test interactif de l'automate")
    print("@ Vous pouvez changer l'automate testé en modifiant la fonction appelée à la ligne 'ok = ... '.")
    print("@ Tapez une entrée:")
    try:
        ok,value = pointfloat() # changer ici pour tester un autre automate sans valeur
        # ok, val = integer() # changer ici pour tester un autre automate avec valeur
        # ok, val = True, eval_exp() # changer ici pour tester eval_exp et eval_exp_v2
        if ok:
            print("Accepted!")
            print(value)
            # print("value:", val) # décommenter ici pour afficher la valeur (question 4 et +)
        else:
            print("Rejected!")
            print(value)
            # print("value so far:", int_value) # décommenter ici pour afficher la valeur en cas de rejet
    except Error as e:
        print("Error:", e)
