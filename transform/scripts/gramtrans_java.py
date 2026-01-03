def get_first_terminal(rule):
    if rule['type'] == 'SEQ':
        first_terminal = []
        for r in rule['members']:
            terminal = get_first_terminal(r)
            first_terminal += terminal
            if ('blank', None) not in terminal:
                return first_terminal
        return first_terminal
    elif rule['type'] == 'CHOICE':
        first_terminal = []
        for r in rule['members']:
            first_terminal += get_first_terminal(r)
        return first_terminal
    elif rule['type'] == "REPEAT":
        return get_first_terminal(rule['content']) + [('blank', None)]
    elif rule['type'] == "REPEAT1":
        return get_first_terminal(rule['content'])
    elif rule['type'] == "PREC":
        return get_first_terminal(rule['content'])
    elif rule['type'] == "PREC_LEFT":
        return get_first_terminal(rule['content'])
    elif rule['type'] == "PREC_RIGHT":
        return get_first_terminal(rule['content'])
    elif rule['type'] == "PREC_DYNAMIC":
        return get_first_terminal(rule['content'])
    elif rule['type'] == "BLANK":
        return [('blank', None)]
    elif rule['type'] == "SYMBOL":
        return [('nonter', rule['name'])]
    elif rule['type'] == "FIELD":
        return get_first_terminal(rule['content'])
    elif rule['type'] == "STRING":
        return [('ter', rule['value'])]
    elif rule['type'] == "ALIAS":
        return get_first_terminal(rule['content'])
    elif rule['type'] == "TOKEN":
        return [('var', None)]
    elif rule['type'] == "IMMEDIATE_TOKEN":
        return [('var', None)]
    elif rule['type'] == "PATTERN":
        return [('var', None)]
    else:
        print("Error, new type:", rule['type'])

def find_duplicates(input_list):
    seen = set()
    duplicates = set()
    
    for item in input_list:
        if item in seen:
            duplicates.add(item)
        else:
            seen.add(item)
    
    return list(duplicates)

def find_duplicates_2(input_list):
    seen = set()
    duplicates = set()
    
    for items in input_list:
        for item in items:
            if item in seen:
                duplicates.add(item)
            else:
                seen.add(item)
    
    return list(duplicates)

def unzip_one_symbol(terminal_list):
    unzip_terminal_list = [] 
    for terminal in terminal_list:
        if terminal[0] == 'nonter':
            if terminal[1] in first_terminals:
                unzip_terminal_list.append(first_terminals[terminal[1]])
            else:
                unzip_terminal_list.append([terminal])
        else:
            unzip_terminal_list.append([terminal])
    return unzip_terminal_list
