import pandas as pd

def is_number_tryexcept(s):
    """ Returns True if string is a number. """
    try:
        float(s)
        return True
    except ValueError:
        return False

def match(df, col, val):
    return df.loc[df[col] == val]

def process_match_operation(expression, df):
    try:
        expr = expression.replace('"','')
        comma_index = int(expr.index(','))
        
        col_name = expr[0:comma_index]
        value = expr[comma_index+1:]
        if(is_number_tryexcept(value)):
            return match(df, col_name, float(value))
        return match(df, col_name, value)
    except Exception as ex:
         raise Exception(f'Unable to process match operation for input {input}, details: {ex}')

def negate_result(result, total_num_of_rows):
    negated_result = set()
    for i in range(total_num_of_rows):
        if i not in result:
            negated_result.append(i)
    return negated_result

def combine_results(result1, result2, operation):
    combined_result = set()
    if operation == 'AND':
        for val in result1:
            if val in result2:
                combined_result.add(val)
    elif operation == 'OR':
        for val in result1:
            combined_result.add(val)
        for val in result2:
            combined_result.add(val)
    else:
        raise Exception(f'Unrecognized operation {operation}')
    return combined_result

def process_input(input, operation_stack, df):
    if len(input) < 1:
        return
    first_char = input[0]
    if first_char == 'A' and input[0:4] == 'AND(':
        operation_stack.append('AND')
        process_input(input[4:], operation_stack, df)
    elif first_char == 'O' and input[0:3] == 'OR(':
        operation_stack.append('OR')
        process_input(input[3:], operation_stack, df)
    elif first_char == 'N' and input[0:4] == 'NOT(':
        operation_stack.append('NOT')
        process_input(input[4:], operation_stack, df)
    elif first_char == 'M' and input[0:6] == 'MATCH(':
        right_paren_index = int(input.index(')'))
        result = process_match_operation(input[6:right_paren_index], df)
        operation_stack.append(result)
        process_input(input[right_paren_index+2:].strip(), operation_stack, df)
    elif first_char == ',' and input[0:1] == ', ':
        process_input(input[2:], operation_stack, df) 
    elif first_char == ')': # This does NOT include the ) for MATCH(...)
        print(operation_stack)
        result1 = operation_stack.pop()
        result2 = operation_stack.pop()
        if type(result2) != str:
            operation = operation_stack.pop()
            combined_result = combine_results(result1, result2, operation)
            operation_stack.append(combined_result)
        else:
            if result2 == 'NOT':
                negated_result = negate_result(result, len(df))
                operation_stack.append(negated_result)
            else:
                raise Exception(f'Unrecognized operation {operation}')
    else:
        raise Exception(f'Cannot parse input {input}')

# print(extract_match_expr(df, 'MATCH("Rank", "2")'))
df = pd.read_csv("data.csv")
process_input('AND(MATCH("RANK", "1"), MATCH("Days in Top 10", "0"))', [], df)