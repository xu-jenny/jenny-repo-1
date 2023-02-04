import pandas as pd

def is_number_tryexcept(s):
    """ Returns True if string is a number. """
    try:
        float(s)
        return True
    except ValueError:
        return False

def match(df, col, val):
    print(col, val, type(col), type(val))
    return df.loc[df[col] == val]

def extract_expr(df, expression):
    if expression[0:5] == 'MATCH':
        expr = expression[5:].replace('"','')
        left_paren_index = int(expr.index('('))
        comma_index = int(expr.index(','))
        right_paren_index = int(expr.index(')'))
        
        col_name = expr[left_paren_index+1:comma_index]
        value = expr[comma_index+1:right_paren_index]

        if(is_number_tryexcept(value)):
            return match(df, col_name, float(value))
        return match(df, col_name, value)
    else:
         raise Exception(f'Unrecognized operation for input {input}') # todo: make exception class

df = pd.read_csv("data.csv")
print(extract_expr(df, 'MATCH("Rank", "2")'))