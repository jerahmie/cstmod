"""padbracket
    Pad square bracket characters for pattern matching with square brackets.
    
"""

def padbrackets(string_with_brackets):

    f_right_bracket = string_with_brackets.split('[')  
    f_padded_right_bracket = [] # storage of padded string fragments 
    for fsub in f_right_bracket:
        temp = fsub.split(']')
        f_padded_right_bracket.append("[]]".join(temp))

    return "[[]".join(f_padded_right_bracket)
