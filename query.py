import pandas as pd

def is_number_tryexcept(s):
    """ Returns True if string is a number. """
    try:
        float(s)
        return True
    except ValueError:
        return False

def match(df, col, val):
    return set(df[df[col] == val].index)

def process_match_operation(input, df):
    try:
        # print(f'match expression input [{input}]')
        input_expression = input
        input_expression = input_expression.replace('"','')
        comma_index = int(input_expression.index(','))
        col_name = input_expression[0:comma_index]
        value = input_expression[comma_index+2:]
        if(is_number_tryexcept(value)):
            return match(df, col_name, float(value))
        return match(df, col_name, value)
    except Exception as ex:
         raise Exception(f'Unable to process match operation for input {input}, details: {ex}')


def negate_result(result, total_num_of_rows):
    negated_result = set()
    for i in range(total_num_of_rows):
        if i not in result:
            negated_result.add(i)
    return negated_result

def combine_results(result1, result2, operation):
    # print(f'Combine results, result1 is {result1}, result2 is {result2}, operation {operation}')
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
    # print(combined_result)
    return combined_result

# input is a valid sequence that starts with AND(...), OR(...), NOT(...), MATCH(...), comma(,) or ) 
# operation_stack is either a set of matched rows, or strings 'AND', 'OR', 'NOT'
def process_input(input, operation_stack, df):
    # print(operation_stack)
    if not input: # processed to end of string, return final result on the stack
        selected_rows = list(operation_stack.pop())
        print(df.loc[df.index[selected_rows]])
        return df.loc[df.index[selected_rows]]

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
        process_input(input[right_paren_index+1:], operation_stack, df)
    elif first_char == ',' and input[0:2] == ', ':
        process_input(input[2:], operation_stack, df)
    elif first_char == ')': # This does NOT include the ) for MATCH(...)
        result1 = operation_stack.pop()
        result2 = operation_stack.pop()
        if type(result2) != str:
            operation = operation_stack.pop()
            combined_result = combine_results(result1, result2, operation)
            operation_stack.append(combined_result)
        else:
            if result2 == 'NOT':
                negated_result = negate_result(result1, len(df))
                operation_stack.append(negated_result)
            else:
                raise Exception(f'Unrecognized operation {operation}')
        process_input(input[1:], operation_stack, df)
    else:
        raise Exception(f'Cannot parse input [{input}]')

df = pd.read_csv('data.csv')
# query = 'AND(MATCH("Type", "TV Show"), MATCH("Rank", "1"))'
query = 'AND(AND(OR(MATCH("Rank", "1"), MATCH("Rank", "3")), NOT(MATCH("Type", "Movie"))), MATCH("Days In Top 10", "11"))'
# query = 'MATCH("Type", "TV Show")'
process_input(query, [], df)