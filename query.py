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

def extract_match_expr(df, expression):
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

def process_input(input, operation_stack, csv_data):
    first_char = input[0]
    if first_char == 'A' and input[0:3] == 'AND(':
        print("TOOD")
    elif first_char == 'O' and input[0:2] == 'OR(':
        print("TODO")
    elif first_char == 'N' and input[0:3] == 'NOT(':
        print("TODO")
    elif first_char == 'M' and input[0:5] == 'MATCH(':
        operation_stack.append([1, 2, 3]) # TODO: add result of 
    elif first_char == ',' and input[0:1] == ', ':
        # TODO: call extract_match_expr here
        process_input(input[2:], operation_stack, csv_data) 
    elif first_char == ')': # This does NOT include the ) for MATCH(...)
        element1 = operation_stack.pop()
        element2 = operation_stack.pop()
        if type(element2) != str:
            operation = operation_stack.pop()
            if operation == 'AND': # Take the common rows in element1 and element2 only
                print("todo")
            elif operation == 'OR': # Combine rows in element1 and element2
                print("todo")
            else:
                raise Exception(f'Unrecognized operation {operation}')
        elif element2 == 'NOT': # This is a NOT operation, negate the rows in element1
                print("todo")
        else:
            raise Exception(f'Unrecognized operation {operation}')
        # TODO: negate the list of rows in element1
        # TODO: push the combined result back to the stack
    else:
        raise Exception(f'Cannot parse input {input}')

# df = pd.read_csv("data.csv")
# print(extract_match_expr(df, 'MATCH("Rank", "2")'))