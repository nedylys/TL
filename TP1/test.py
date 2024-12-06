import sys

# Ensure the set V includes the necessary characters
V = set(('.', 'e', 'E', '+', '-')
        + tuple(str(i) for i in range(10)))

class Error(Exception):
    pass

# Ensure the input stream is defined
INPUT_STREAM = sys.stdin
END = '\n'  # End of input
sign_value=0
exposant=0
# Initialization: make sure END is not in V
def init_char():
    if END in V:
        raise Error('character ' + repr(END) + ' in V')

# Access the next character in the input stream
def next_char():
    global INPUT_STREAM
    ch = INPUT_STREAM.read(1)
    print(f"Read char in next_char: {repr(ch)}")  # Debugging print
    if ch in V or ch == END:
        return ch
    raise Error('character ' + repr(ch) + ' unsupported')

# Start function for processing exponent notation
def exponent_float():
    init_char()
    return exponent_float_state_0()

# State 0: Initial float parsing
def exponent_float_state_0():
    global exponentfloat
    ch = next_char()
    print(f"exponent_float_state_0: Read char: {repr(ch)}")  # Debugging print
    if ch == '.' or ch == '+' or ch == '-' or ch.isdigit():
        exponentfloat = float(ch)
        return exponent_float_state_1()
    return False, None

# State 1: Parsing digits and handling the 'e' character
def exponent_float_state_1():
    global exponentfloat
    ch = next_char()  # Read the next character
    print(f"exponent_float_state_1: Read char: {repr(ch)}")  # Debugging print
    if ch == 'e' or ch == 'E':  # If 'e' or 'E' (scientific notation) is found
        print("Found 'e' or 'E'. Transitioning to exponent_float_state_2()")  # Debugging print
        return exponent_float_state_2()  # Transition to exponent handling state
    if ch.isdigit():  # If a digit is found, append it to the float
        print(f"Adding digit {ch} to exponentfloat")  # Debugging print
        exponentfloat = float(str(exponentfloat) + ch)
        return exponent_float_state_1()  # Continue parsing the float
    return False, None

# State 2: Handling the exponent part
def exponent_float_state_2():
    global exposant
    global sign_value
    ch = next_char()
    print(f"exponent_float_state_2: Read char: {repr(ch)}")  # Debugging print
    if ch == '+':
        sign_value = 1
        return exponent_float_state_2()  # Stay in the same state until we get a digit
    elif ch == '-':
        sign_value = -1
        return exponent_float_state_2()  # Stay in the same state until we get a digit
    elif ch.isdigit():
        exposant = int(ch)
        return exponent_float_state_3()  # Move to parsing the exponent digits
    return False, None

# State 3: Finalizing the exponent calculation
def exponent_float_state_3():
    global exposant
    ch = next_char()
    print(f"exponent_float_state_3: Read char: {repr(ch)}")  # Debugging print
    if ch == END:  # If we've reached the end of input, calculate the result
        return True, exponentfloat * 10 ** (sign_value * exposant)
    if ch.isdigit():
        exposant = int(str(exposant) + ch)  # Add more digits to the exponent
        return exponent_float_state_3()  # Continue processing exponent digits
    return False, None
if __name__ == "__main__":
    print("@ Test interactif de l'automate")
    print("@ Vous pouvez changer l'automate testé en modifiant la fonction appelée à la ligne 'ok = ... '.")
    print("@ Tapez une entrée:")
    try:
        ok,value = exponent_float() # changer ici pour tester un autre automate sans valeur
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
def exponentfloat():
    global int_value
    global sign_value
    global exp_value
    global pres_e
    int_value=0
    sign_value=0
    exp_value=0
    pres_e=0
    init_char()
    return exponentfloat_state_0()
def exponentfloat_state_0():
    global int_value
    ok1,_=pointfloat()
    print(ok1)
    if pres_e==2:
        return exponentfloat_state_2()
    if str(int_value)!='@':
        if pres_e==1:
            return exponentfloat_state_2()
        return exponentfloat_state_1()
    return False,None
def exponentfloat_state_1():
    global int_value
    ch=next_char()
    print(ch)
    if ch== 'e' or ch== 'E':
        return exponentfloat_state_2()
    if digit(ch):
        int_value=int(str(int_value)+ch)
        return exponentfloat_state_1()
    return False,None
def exponentfloat_state_2():
    global exposant
    global sign_value
    ch=next_char()
    if ch=='+' :
        if sign_value!=0:
            return False,None
        sign_value=1
        return exponentfloat_state_2()
    if ch=='-':
        if sign_value!=0:
            return False,None
        sign_value=-1
        return exponentfloat_state_2()
    if digit(ch):
        if sign_value==0:
            sign_value=1
        exposant=int(ch)
        return exponentfloat_state_3()
    return False,None
def exponentfloat_state_3():
    global exposant
    ch=next_char()
    if ch==END:
        print(sign_value)
        return True,int_value*10**(sign_value*exposant-exp_value)
    if digit(ch):
        exposant=int(str(exposant)+ch)
        return exponentfloat_state_3()
    return False,None