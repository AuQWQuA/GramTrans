from tree_sitter import Language, Parser
import tree_sitter_pymbhell1
import tree_sitter_pymbhe

parserll1 = Parser(Language(tree_sitter_pymbhell1.language()))
parser = Parser(Language(tree_sitter_pymbhe.language()))

def ll1_deparse(node, indent=0):
    if node.type == "identifier":
        return node.text.decode("utf8")
    elif node.type == "float":
        return node.text.decode("utf8")
    elif node.type == "integer":
        return node.text.decode("utf8") 
    elif node.type == "string": 
        return node.text.decode("utf8")
    elif node.type == ",":
        return ", "
    elif node.type == "true":
        return "True"
    elif node.type == "false":
        return "False"
    elif node.type == "none":
        return "None"
    if node.child_count == 0:
        return node.type

    compound_statement = ["class_definition", "function_definition", "for_statement", "while_statement", "if_statement", "try_statement"]
    simple_statement = ["expression_statement", "return_statement", "break_statement", "import_statement", "import_from_statement", "continue_statement", "pass_statement", "delete_statement"]
    compounded_statement = ["elif_clause", "else_clause", "except_clause"]
    statement = compound_statement + simple_statement

    if node.type in ["block"]:
        returnlist =  ["\n"]
        i = 0
        while i < node.child_count:
            if node.child(i).type == "comment" or node.child(i).type == "line_continuation":
                i += 1
                continue
            returnlist += [ll1_deparse(node.child(i), indent + 1)]
            if node.child(i).type in simple_statement:
                if i + 1 < node.child_count and node.child(i + 1).type != ";":
                    returnlist += ["\n"]
                elif i + 1 == node.child_count:
                    returnlist += ["\n"]
                elif i + 2 == node.child_count and node.child(i + 1).type == ";":
                    i += 1
                    returnlist += [ll1_deparse(node.child(i), indent + 1)]
                    returnlist += ["\n"]

                elif i + 2 < node.child_count and node.child(i + 1).type == ";" and (node.child(i + 2).type not in simple_statement):
                    i += 1
                    returnlist += [ll1_deparse(node.child(i), indent + 1)]
                    returnlist += ["\n"]
            i += 1
                 
                    
    elif node.type in ["module"]:
        returnlist = []
        i = 0
        while i < node.child_count:
            if node.child(i).type == "comment" or node.child(i).type == "line_continuation":
                i += 1
                continue
            returnlist += [ll1_deparse(node.child(i), indent)]
            if node.child(i).type in simple_statement:
                if i + 1 < node.child_count and node.child(i + 1).type != ";":
                    returnlist += ["\n"]
                elif i + 1 == node.child_count:
                    returnlist += ["\n"]
                elif i + 2 == node.child_count and node.child(i + 1).type == ";":
                    i += 1
                    returnlist += [ll1_deparse(node.child(i), indent)]
                    returnlist += ["\n"]

                elif i + 2 < node.child_count and node.child(i + 1).type == ";" and (node.child(i + 2).type not in simple_statement):
                    i += 1
                    returnlist += [ll1_deparse(node.child(i), indent)]
                    returnlist += ["\n"]
            i += 1
    else:
        returnlist = [ll1_deparse(node.child(i), indent) for i in range(node.child_count) if node.child(i).type != 'comment' and node.child(i).type != 'line_continuation']
    
    childlen = len(returnlist)
    if node.type in ["class_definition"]:
        if childlen == 4:
            returnlist = [returnlist[0], " ", returnlist[1], returnlist[2], returnlist[3]]
        elif childlen == 5:
            returnlist = [returnlist[0], " ", returnlist[1], " ", returnlist[2], returnlist[3], returnlist[4]]
        else:
            print("wrong_class_definition", childlen)
    elif node.type in ["function_definition"]:
        if childlen == 5:
            returnlist = [returnlist[0], " ", returnlist[1], returnlist[2], returnlist[3], returnlist[4]]
        elif childlen == 7:
            returnlist = [returnlist[0], " ", returnlist[1], returnlist[2], " ", returnlist[3], " ", returnlist[4], returnlist[5], returnlist[6]]
    elif node.type in ["for_statement"]:
        returnlist.insert(3, " ")
        returnlist.insert(2, " ")
        returnlist.insert(1, " ")
    elif node.type in ["while_statement"]:
        returnlist.insert(1, " ")
    elif node.type in ["if_statement"]:
        returnlist.insert(1, " ")
    elif node.type in ["return_statement"]:
        if childlen == 1:
            returnlist = [returnlist[0]]
        else:
            returnlist = [returnlist[0], " ", returnlist[1]]
    elif node.type in ["import_statement"]:
        returnlist.insert(1, " ")
    elif node.type in ["import_from_statement"]:
        returnlist.insert(3, " ")
        returnlist.insert(2, " ")
        returnlist.insert(1, " ")
    elif node.type in ["delete_statement"]:
        returnlist = [returnlist[0], " ", returnlist[1]]
    
    elif node.type in ["assignment", "augmented_assignment"]:
        returnlist = [returnlist[1], " ", returnlist[0], " ", returnlist[2]]
    elif node.type in ["except_clause"]:
        returnlist.insert(1, " ")
    elif node.type in ["elif_clause"]:
        returnlist.insert(1, " ")
    elif node.type in ["comparison_operator"]:
        if childlen == 3:
            returnlist = [returnlist[0], " ", returnlist[1], " ", returnlist[2]]
        elif childlen == 4:
            returnlist = [returnlist[0], " ", returnlist[1], " ", returnlist[2], " ", returnlist[3]]
        elif childlen == 5:
            returnlist = [returnlist[0], " ", returnlist[1], " ", returnlist[2], " ", returnlist[3], " ", returnlist[4]]
    elif node.type in ["binary_operator", "boolean_operator"]:
        returnlist = [returnlist[1], " ", returnlist[0], " ", returnlist[2]]
    elif node.type in ["yield"]:
        if childlen == 2:
            returnlist = [returnlist[0], " ", returnlist[1]]
        elif childlen == 3:
            returnlist = [returnlist[0], " ", returnlist[1], " ", returnlist[2]]
    elif node.type in ["for_in_clause"]:
        returnlist = [" ", returnlist[0], " ", returnlist[1], " ", returnlist[2], " ", returnlist[3]]
    elif node.type in ["if_clause"]:
        returnlist = [" ", returnlist[0], " ", returnlist[1]]
    elif node.type in ["aliased_import"]:
        returnlist = [returnlist[0], " ", returnlist[1], " ", returnlist[2]]
    elif node.type in ["lambda"]:
        if childlen == 4:
            returnlist = [returnlist[0], " ", returnlist[1], returnlist[2], returnlist[3]]
        returnlist.insert(-1, " ")
    elif node.type in ["conditional_expression"]:
        returnlist = [returnlist[0], " ", returnlist[1], " ", returnlist[2], " ", returnlist[3], " ", returnlist[4]]
    elif node.type in ["not_operator"]:
        returnlist = ["not", " ", returnlist[1]]
    elif node.type in ["not in"]:
        returnlist = [returnlist[0], " ", returnlist[1]]
    elif node.type in ["is not"]:
        returnlist = [returnlist[0], " ", returnlist[1]]
    elif node.type in ["call"]:
        returnlist = [returnlist[1], returnlist[2]]
    elif node.type in ["unary_operator"]:
        if node.child(0).type == "NEG":
            returnlist = ["-", returnlist[1]]
    elif node.type in ["list"]:
        returnlist = returnlist[1:]
    elif node.type in ["list_comprehension"]:
        returnlist = returnlist[1:]

    if node.type in statement:
        returnlist = [" " * indent * 4] + returnlist    
    if node.type in compounded_statement:
        returnlist = [" " * indent * 4] + returnlist
    if node.type in simple_statement and node.parent.type not in ["block", "module"]:
        returnlist = returnlist + ["\n"]
    return returnlist
def deparse_ll1(node, indent=0):
    if node.type == "identifier":
        return node.text.decode("utf8")
    elif node.type == "float":
        return node.text.decode("utf8")
    elif node.type == "integer":
        return node.text.decode("utf8") 
    elif node.type == "string": 
        return node.text.decode("utf8")
    elif node.type == ",":
        return ", "
    elif node.type == "true":
        return "True"
    elif node.type == "false":
        return "False"
    elif node.type == "none":
        return "None"
    if node.child_count == 0:
        return node.type

    compound_statement = ["class_definition", "function_definition", "for_statement", "while_statement", "if_statement", "try_statement"]
    simple_statement = ["expression_statement", "return_statement", "break_statement", "import_statement", "import_from_statement", "continue_statement", "pass_statement", "delete_statement"]
    compounded_statement = ["elif_clause", "else_clause", "except_clause"]
    statement = compound_statement + simple_statement

    if node.type in ["block"]:
        returnlist =  ["\n"]
        i = 0
        while i < node.child_count:
            if node.child(i).type == "comment" or node.child(i).type == "line_continuation":
                i += 1
                continue
            returnlist += [deparse_ll1(node.child(i), indent + 1)]
            if node.child(i).type in simple_statement:
                if i + 1 < node.child_count and node.child(i + 1).type != ";":
                    returnlist += ["\n"]
                elif i + 1 == node.child_count:
                    returnlist += ["\n"]
                elif i + 2 == node.child_count and node.child(i + 1).type == ";":
                    i += 1
                    returnlist += [deparse_ll1(node.child(i), indent + 1)]
                    returnlist += ["\n"]

                elif i + 2 < node.child_count and node.child(i + 1).type == ";" and (node.child(i + 2).type not in simple_statement):
                    i += 1
                    returnlist += [deparse_ll1(node.child(i), indent + 1)]
                    returnlist += ["\n"]
            i += 1
                 
                    
    elif node.type in ["module"]:
        returnlist = []
        i = 0
        while i < node.child_count:
            if node.child(i).type == "comment" or node.child(i).type == "line_continuation":
                i += 1
                continue
            returnlist += [deparse_ll1(node.child(i), indent)]
            if node.child(i).type in simple_statement:
                if i + 1 < node.child_count and node.child(i + 1).type != ";":
                    returnlist += ["\n"]
                elif i + 1 == node.child_count:
                    returnlist += ["\n"]
                elif i + 2 == node.child_count and node.child(i + 1).type == ";":
                    i += 1
                    returnlist += [deparse_ll1(node.child(i), indent)]
                    returnlist += ["\n"]

                elif i + 2 < node.child_count and node.child(i + 1).type == ";" and (node.child(i + 2).type not in simple_statement):
                    i += 1
                    returnlist += [deparse_ll1(node.child(i), indent)]
                    returnlist += ["\n"]
            i += 1
    else:
        returnlist = [deparse_ll1(node.child(i), indent) for i in range(node.child_count) if node.child(i).type != 'comment' and node.child(i).type != 'line_continuation']
    
    childlen = len(returnlist)
    if node.type in ["class_definition"]:
        if childlen == 4:
            returnlist = [returnlist[0], " ", returnlist[1], returnlist[2], returnlist[3]]
        elif childlen == 5:
            returnlist = [returnlist[0], " ", returnlist[1], " ", returnlist[2], returnlist[3], returnlist[4]]
        else:
            print("wrong_class_definition", childlen)
    elif node.type in ["function_definition"]:
        if childlen == 5:
            returnlist = [returnlist[0], " ", returnlist[1], returnlist[2], returnlist[3], returnlist[4]]
        elif childlen == 7:
            returnlist = [returnlist[0], " ", returnlist[1], returnlist[2], " ", returnlist[3], " ", returnlist[4], returnlist[5], returnlist[6]]
    elif node.type in ["for_statement"]:
        returnlist.insert(3, " ")
        returnlist.insert(2, " ")
        returnlist.insert(1, " ")
    elif node.type in ["while_statement"]:
        returnlist.insert(1, " ")
    elif node.type in ["if_statement"]:
        returnlist.insert(1, " ")
    elif node.type in ["return_statement"]:
        if childlen == 1:
            returnlist = [returnlist[0]]
        else:
            returnlist = [returnlist[0], " ", returnlist[1]]
    elif node.type in ["import_statement"]:
        returnlist.insert(1, " ")
    elif node.type in ["import_from_statement"]:
        returnlist.insert(3, " ")
        returnlist.insert(2, " ")
        returnlist.insert(1, " ")
    elif node.type in ["delete_statement"]:
        returnlist = [returnlist[0], " ", returnlist[1]]
    
    elif node.type in ["assignment", "augmented_assignment"]:
        returnlist = [returnlist[1], " ", returnlist[0], " ", returnlist[2]]
    elif node.type in ["except_clause"]:
        returnlist.insert(1, " ")
    elif node.type in ["elif_clause"]:
        returnlist.insert(1, " ")
    elif node.type in ["comparison_operator"]:
        if childlen == 3:
            returnlist = [returnlist[0], " ", returnlist[1], " ", returnlist[2]]
        elif childlen == 4:
            returnlist = [returnlist[0], " ", returnlist[1], " ", returnlist[2], " ", returnlist[3]]
        elif childlen == 5:
            returnlist = [returnlist[0], " ", returnlist[1], " ", returnlist[2], " ", returnlist[3], " ", returnlist[4]]
    elif node.type in ["binary_operator", "boolean_operator"]:
        returnlist = [returnlist[1], " ", returnlist[0], " ", returnlist[2]]
    elif node.type in ["yield"]:
        if childlen == 2:
            returnlist = [returnlist[0], " ", returnlist[1]]
        elif childlen == 3:
            returnlist = [returnlist[0], " ", returnlist[1], " ", returnlist[2]]
    elif node.type in ["for_in_clause"]:
        returnlist = [" ", returnlist[0], " ", returnlist[1], " ", returnlist[2], " ", returnlist[3]]
    elif node.type in ["if_clause"]:
        returnlist = [" ", returnlist[0], " ", returnlist[1]]
    elif node.type in ["aliased_import"]:
        returnlist = [returnlist[0], " ", returnlist[1], " ", returnlist[2]]
    elif node.type in ["lambda"]:
        if childlen == 4:
            returnlist = [returnlist[0], " ", returnlist[1], returnlist[2], returnlist[3]]
        returnlist.insert(-1, " ")
    elif node.type in ["conditional_expression"]:
        returnlist = [returnlist[0], " ", returnlist[1], " ", returnlist[2], " ", returnlist[3], " ", returnlist[4]]
    elif node.type in ["not_operator"]:
        returnlist = ["NOT", " ", returnlist[1]]
    elif node.type in ["not in"]:
        returnlist = [returnlist[0], " ", returnlist[1]]
    elif node.type in ["is not"]:
        returnlist = [returnlist[0], " ", returnlist[1]]
    elif node.type in ["call"]:
        returnlist = ["call", " ", returnlist[0], returnlist[1]]
    elif node.type in ["unary_operator"]:
        if node.child(0).type == "-":
            returnlist = ["NEG", " ", returnlist[1]]
    elif node.type in ["list"]:
        returnlist = ["LIST"] + returnlist
    elif node.type in ["list_comprehension"]:
        returnlist = ["LIST"] + returnlist

    if node.type in statement:
        returnlist = [" " * indent * 4] + returnlist    
    if node.type in compounded_statement:
        returnlist = [" " * indent * 4] + returnlist
    if node.type in simple_statement and node.parent.type not in ["block", "module"]:
        returnlist = returnlist + ["\n"]
    return returnlist
def deparse_ll(node, indent=0):
    if node.type == "identifier":
        return node.text.decode("utf8")
    elif node.type == "float":
        return node.text.decode("utf8")
    elif node.type == "integer":
        return node.text.decode("utf8") 
    elif node.type == "string": 
        return node.text.decode("utf8")
    elif node.type == ",":
        return ", "
    elif node.type == "true":
        return "True"
    elif node.type == "false":
        return "False"
    elif node.type == "none":
        return "None"
    if node.child_count == 0:
        return node.type

    compound_statement = ["class_definition", "function_definition", "for_statement", "while_statement", "if_statement", "try_statement"]
    simple_statement = ["expression_statement", "return_statement", "break_statement", "import_statement", "import_from_statement", "continue_statement", "pass_statement", "delete_statement"]
    compounded_statement = ["elif_clause", "else_clause", "except_clause"]
    statement = compound_statement + simple_statement

    if node.type in ["block"]:
        returnlist =  [" INDENT\n"]
        i = 0
        while i < node.child_count:
            if node.child(i).type == "comment" or node.child(i).type == "line_continuation":
                i += 1
                continue
            returnlist += [deparse_ll(node.child(i), indent + 1)]
            if node.child(i).type in simple_statement:
                if i + 1 < node.child_count and node.child(i + 1).type != ";":
                    returnlist += ["\n"]
                elif i + 1 == node.child_count:
                    returnlist += ["\n"]
                elif i + 2 == node.child_count and node.child(i + 1).type == ";":
                    i += 1
                    returnlist += [deparse_ll(node.child(i), indent + 1)]
                    returnlist += ["\n"]

                elif i + 2 < node.child_count and node.child(i + 1).type == ";" and (node.child(i + 2).type not in simple_statement):
                    i += 1
                    returnlist += [deparse_ll(node.child(i), indent + 1)]
                    returnlist += ["\n"]
            i += 1
        returnlist += ["DEDENT\n"]
            
                    
    elif node.type in ["module"]:
        returnlist = []
        i = 0
        while i < node.child_count:
            if node.child(i).type == "comment" or node.child(i).type == "line_continuation":
                i += 1
                continue
            returnlist += [deparse_ll(node.child(i), indent)]
            if node.child(i).type in simple_statement:
                if i + 1 < node.child_count and node.child(i + 1).type != ";":
                    returnlist += ["\n"]
                elif i + 1 == node.child_count:
                    returnlist += ["\n"]
                elif i + 2 == node.child_count and node.child(i + 1).type == ";":
                    i += 1
                    returnlist += [deparse_ll(node.child(i), indent)]
                    returnlist += ["\n"]

                elif i + 2 < node.child_count and node.child(i + 1).type == ";" and (node.child(i + 2).type not in simple_statement):
                    i += 1
                    returnlist += [deparse_ll(node.child(i), indent)]
                    returnlist += ["\n"]
            i += 1
    else:
        returnlist = [deparse_ll(node.child(i), indent) for i in range(node.child_count) if node.child(i).type != 'comment' and node.child(i).type != 'line_continuation']
    
    childlen = len(returnlist)
    if node.type in ["class_definition"]:
        if childlen == 4:
            returnlist = [returnlist[0], " ", returnlist[1], returnlist[2], returnlist[3]]
        elif childlen == 5:
            returnlist = [returnlist[0], " ", returnlist[1], " ", returnlist[2], returnlist[3], returnlist[4]]
        else:
            print("wrong_class_definition", childlen)
    elif node.type in ["function_definition"]:
        if childlen == 5:
            returnlist = [returnlist[0], " ", returnlist[1], returnlist[2], returnlist[3], returnlist[4]]
        elif childlen == 7:
            returnlist = [returnlist[0], " ", returnlist[1], returnlist[2], " ", returnlist[3], " ", returnlist[4], returnlist[5], returnlist[6]]
    elif node.type in ["for_statement"]:
        returnlist.insert(3, " ")
        returnlist.insert(2, " ")
        returnlist.insert(1, " ")
    elif node.type in ["while_statement"]:
        returnlist.insert(1, " ")
    elif node.type in ["if_statement"]:
        returnlist.insert(1, " ")
    elif node.type in ["return_statement"]:
        if childlen == 1:
            returnlist = [returnlist[0]]
        else:
            returnlist = [returnlist[0], " ", returnlist[1]]
    elif node.type in ["import_statement"]:
        returnlist.insert(1, " ")
    elif node.type in ["import_from_statement"]:
        returnlist.insert(3, " ")
        returnlist.insert(2, " ")
        returnlist.insert(1, " ")
    elif node.type in ["delete_statement"]:
        returnlist = [returnlist[0], " ", returnlist[1]]
    
    elif node.type in ["assignment", "augmented_assignment"]:
        returnlist = [returnlist[1], " ", returnlist[0], " ", returnlist[2]]
    elif node.type in ["except_clause"]:
        returnlist.insert(1, " ")
    elif node.type in ["elif_clause"]:
        returnlist.insert(1, " ")
    elif node.type in ["comparison_operator"]:
        if childlen == 3:
            returnlist = [returnlist[0], " ", returnlist[1], " ", returnlist[2]]
        elif childlen == 4:
            returnlist = [returnlist[0], " ", returnlist[1], " ", returnlist[2], " ", returnlist[3]]
        elif childlen == 5:
            returnlist = [returnlist[0], " ", returnlist[1], " ", returnlist[2], " ", returnlist[3], " ", returnlist[4]]
    elif node.type in ["binary_operator", "boolean_operator"]:
        returnlist = [returnlist[1], " ", returnlist[0], " ", returnlist[2]]
    elif node.type in ["yield"]:
        if childlen == 2:
            returnlist = [returnlist[0], " ", returnlist[1]]
        elif childlen == 3:
            returnlist = [returnlist[0], " ", returnlist[1], " ", returnlist[2]]
    elif node.type in ["for_in_clause"]:
        returnlist = [" ", returnlist[0], " ", returnlist[1], " ", returnlist[2], " ", returnlist[3]]
    elif node.type in ["if_clause"]:
        returnlist = [" ", returnlist[0], " ", returnlist[1]]
    elif node.type in ["aliased_import"]:
        returnlist = [returnlist[0], " ", returnlist[1], " ", returnlist[2]]
    elif node.type in ["lambda"]:
        if childlen == 4:
            returnlist = [returnlist[0], " ", returnlist[1], returnlist[2], returnlist[3]]
        returnlist.insert(-1, " ")
    elif node.type in ["conditional_expression"]:
        returnlist = [returnlist[0], " ", returnlist[1], " ", returnlist[2], " ", returnlist[3], " ", returnlist[4]]
    elif node.type in ["not_operator"]:
        returnlist = ["NOT", " ", returnlist[1]]
    elif node.type in ["not in"]:
        returnlist = [returnlist[0], " ", returnlist[1]]
    elif node.type in ["is not"]:
        returnlist = [returnlist[0], " ", returnlist[1]]
    elif node.type in ["call"]:
        returnlist = ["call", " ", returnlist[0], returnlist[1]]
    elif node.type in ["unary_operator"]:
        if node.child(0).type == "-":
            returnlist = ["NEG", " ", returnlist[1]]
    elif node.type in ["list"]:
        returnlist = ["LIST"] + returnlist
    elif node.type in ["list_comprehension"]:
        returnlist = ["LIST"] + returnlist
    elif node.type in ["set_comprehension"]:
        returnlist = ["SETC "] + returnlist    
    elif node.type in ["dictionary_comprehension"]:
        returnlist = ["DICTC "] + returnlist
    elif node.type in ["dictionary"]:
        returnlist = ["DICT "] + returnlist
    elif node.type in ["set"]:
        returnlist = ["SET "] + returnlist
    elif node.type in ["tuple"]:   
        returnlist = ["TUPLE "] + returnlist
    elif node.type in ["default_parameter"]:
        returnlist = ["DEFP "] + returnlist 
    elif node.type in ["typed_parameter"]:
        returnlist = ["TYPEP "] + returnlist
    elif node.type in ["subscript"]:
        returnlist = ["SUB "] + returnlist
    elif node.type in ["attribute"]:
        returnlist = ["ATTR "] + returnlist
    

    # if node.type in statement:
        # returnlist = [" " * indent * 4] + returnlist    
    # if node.type in compounded_statement:
        # returnlist = [" " * indent * 4] + returnlist
    if node.type in simple_statement and node.parent.type not in ["block", "module"]:
        returnlist = returnlist + ["\n"]
    return returnlist
def trans_ll1(code):
    
    import re
    def remove_strings(code):
        triple_quoted_string_pattern = r"(?s)([\"']{3})(.*?)(\1)"
        string_list = []

        def replacer(match):
            quote = match.group(1)
            content = match.group(2)
            string_list.append(f"{quote}{content}{quote}")
            return "<triple-quoted-string>"

        new_code = re.sub(triple_quoted_string_pattern, replacer, code)
        return new_code, string_list

    def add_strings(code, string_list):
        def replacer(_):
            return string_list.pop(0)  # 按顺序还原

        restored_code = re.sub(r"<triple-quoted-string>", replacer, code)
        return restored_code  
    
    def remove_keywords(text):
        keywords = ['SETC', 'DICTC', 'DICT', 'SET', 'TUPLE', 'SUB', 'ATTR', 'DEFP', 'TYPEP']
        # 正则：前面是开头或非字母/下划线，关键词后面是空格
        pattern = r'(?<![a-zA-Z_])(?:' + '|'.join(keywords) + r') |^(' + '|'.join(keywords) + r') '
        return re.sub(pattern, '', text)
    
    code = remove_keywords(code)
    code, string_list = remove_strings(code)
    
    codelist = code.split("\n")
    new_codelist = []
    indent = 0
    for i in range(len(codelist)):
        codelist[i] = " " * indent * 4 + codelist[i]
        if codelist[i].endswith("INDENT"):
            codelist[i] = codelist[i][:-7]
            indent += 1
        elif codelist[i].endswith("DEDENT"):
            codelist[i] = ""
            indent -= 1
        if codelist[i] == "":
            continue
        else:
            new_codelist.append(codelist[i])
    new_code = "\n".join(new_codelist) + '\n'
    new_code = add_strings(new_code, string_list)

    return new_code
        
def stringfy(lst):
    if isinstance(lst, str):
        return lst
    return "".join([stringfy(l) for l in lst])

def parsell(code):
    codell1 = trans_ll1(code)
    root = parserll1.parse(bytes(codell1, "utf-8")).root_node
    return stringfy(ll1_deparse(root))
def parsell1(code):
    root = parserll1.parse(bytes(code, "utf-8")).root_node
    return stringfy(ll1_deparse(root))
def parse2ll(code):
    root = parser.parse(bytes(code, "utf-8")).root_node
    return stringfy(deparse_ll(root))
def parse2ll1(code):
    root = parser.parse(bytes(code, "utf-8")).root_node
    return stringfy(deparse_ll1(root))
