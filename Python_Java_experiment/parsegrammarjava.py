from tree_sitter import Language, Parser
import tree_sitter_javahemp
import tree_sitter_javahempll
parser = Parser(Language(tree_sitter_javahemp.language()))
parser2 = Parser(Language(tree_sitter_javahempll.language()))

keywords_with_space = ["case", "catch", "class", "else", "for", "if", "import", "public", "return", "static", "switch", "throw", "throws", "try", "while", "new"]
newlinestatements = [
    "return_statement", "expression_statement", "continue_statement", 
    "break_statement", "throw_statement", "import_declaration", "local_variable_declaration",
    ]
indentstatements = [
    "for_statement","return_statement", "if_statement", "expression_statement", "local_variable_declaration",
    "enhanced_for_statement", "while_statement", "continue_statement", "switch_block_statement_group",
    "break_statement", "throw_statement", "switch_expression", "try_statement", "switch_rule",
    "import_declaration", "class_declaration", "method_declaration", "catch_clause"
    ]
notypespace = ["generic_type", "scoped_type_identifier", "array_type", "type_arguments", "object_creation_expression", "array_creation_expression"]
def deparse_ll(node, indent=0, hasindent=True, newline=True):
    if node.type in ["identifier", "decimal_integer_literal", "hex_integer_literal", "octal_integer_literal", "binary_integer_literal", "decimal_floating_point_literal", "hex_floating_point_literal", "character_literal", "string_literal", "true", "false", "null_literal"]:
        return [node.text.decode("utf8")]
    elif node.type in ["integral_type", "type_identifier", "boolean_type", "floating_point_type"]:
        if node.parent.type not in notypespace:
            return [node.text.decode("utf8") + " "]
        else:
            return [node.text.decode("utf8")]
    elif node.type == ",":
        return [", "]
    elif node.type == ":":
        return [": "]
    elif node.type == "?":
        return ["? "]
    elif node.type == "->":
        return [" -> "]
    elif node.type in keywords_with_space:
        if node.child_count == 0:
            return [node.text.decode("utf8") + " "]
    elif node.type == "instanceof":
        return [" instanceof "]
    elif node.type == "block_comment":
        return [node.text.decode("utf8") + "\n"]
        # return " " * indent * 4 + node.text.decode("utf8") + "\n"
    elif node.type == "line_comment":
        return ""
        # return " " * indent * 4 + node.text.decode("utf8") + "\n"
    if node.child_count == 0:
        return [node.type]
    returnlist = []

    def add_statement(node, indent):
        if node.type == "block":
            return deparse_ll(node, indent)
        else:
            return ["\n"] + deparse_ll(node, indent + 1) 
    # if node.type in indentstatements and hasindent:
        # returnlist.append(" " * indent * 4)
    if node.type in ["method_invocation"]:
        returnlist.append("CALL ")
    
    if node.type in ["block", "class_body", "switch_block"]:
        returnlist.append(" " + "{\n")
        for child in node.children[1:-1]:
            returnlist.append(deparse_ll(child, indent + 1))
        returnlist.append("}")
        # returnlist.append(" " * indent * 4 + "}")
        returnlist.append("\n")
    elif node.type == "for_statement":
        for i in range(node.child_count - 1):
            if i == 2:
                returnlist.append(deparse_ll(node.children[i], indent, False, False))
            else:
                returnlist.append(deparse_ll(node.children[i], indent))
        returnlist.append(add_statement(node.children[-1], indent))
    elif node.type == "enhanced_for_statement":
        returnlist.append("enhanced_for ")
        for child in node.children[1:-1]:
            returnlist.append(deparse_ll(child, indent))
        returnlist.append(add_statement(node.children[-1], indent))
    elif node.type == "if_statement":
        for i in range(2):
            returnlist.append(deparse_ll(node.children[i], indent))
        returnlist.append(add_statement(node.children[2], indent))
        if node.child_count > 3:
            returnlist.append("else")
            # returnlist.append(" " * indent * 4 + "else")
            if node.children[4].type == "if_statement":
                returnlist.append(" ")
                returnlist.append(deparse_ll(node.children[4], indent, False))
            else:
                returnlist.append(add_statement(node.children[4], indent))
    elif node.type == "while_statement":
        for i in range(2):
            returnlist.append(deparse_ll(node.children[i], indent))
        returnlist.append(add_statement(node.children[2], indent))
    elif node.type in ["binary_expression", "assignment_expression"]:
        returnlist.append(node.children[1].text.decode("utf8") + " ")
        returnlist.append(deparse_ll(node.children[0], indent))
        returnlist.append(" ")
        returnlist.append(deparse_ll(node.children[2], indent))
    elif node.type in ['unary_expression']:
        if node.children[0].type == "-":
            returnlist.append("NEG ")
        else:
            returnlist.append(deparse_ll(node.children[0], indent))
        returnlist.append(deparse_ll(node.children[1], indent))
    elif node.type in ['update_expression']:
        if node.children[0].type == "++":
            returnlist.append("INC ")
            returnlist.append(deparse_ll(node.children[1], indent))
        else:
            if node.children[1].type == "--":
                returnlist.append("PDEC ")
            elif node.children[1].type == "++":
                returnlist.append("PINC ")
            returnlist.append(deparse_ll(node.children[0], indent))
    elif node.type == "instanceof_expression":
        returnlist.append("instanceof ")
        returnlist.append(deparse_ll(node.children[0], indent))
        returnlist.append(" ")
        for child in node.children[2:]:
            returnlist.append(deparse_ll(child, indent))
    elif node.type == "variable_declarator":
        for child in node.children:
            if child.type == "=":
                returnlist.append(" = ")
            else:
                returnlist.append(deparse_ll(child, indent))
    elif node.type == "switch_rule":
        for i in range(2):
            returnlist.append(deparse_ll(node.children[i], indent))
        returnlist.append(deparse_ll(node.children[2], indent, False))
    elif node.type == "switch_block_statement_group":
        for i in range(2):
            returnlist.append(deparse_ll(node.children[i], indent))
        if node.child_count > 2:
            returnlist.append(add_statement(node.children[2], indent))
        else:
            returnlist.append("\n")
    elif node.type == "marker_annotation":
        for child in node.children:
            returnlist.append(deparse_ll(child, indent))
        returnlist.append("\n")
        # returnlist.append("\n" + " " * indent * 4)
    else:
        for child in node.children:
            returnlist.append(deparse_ll(child, indent))
    if node.type in newlinestatements and newline:
        returnlist.append("\n")
    if node.type in ["scoped_type_identifier", "generic_type", "array_type"] and node.parent.type not in notypespace:
        returnlist.append(" ")
    return returnlist    
def stringfy(lst):
    if isinstance(lst, str):
        return lst
    return "".join([stringfy(l) for l in lst])

keywords_with_space = ["case", "catch", "class", "else", "for", "if", "import", "public", "return", "static", "switch", "throw", "throws", "try", "while", "new"]
newlinestatements = [
    "return_statement", "expression_statement", "continue_statement", 
    "break_statement", "throw_statement", "import_declaration", "local_variable_declaration",
    ]
indentstatements = [
    "for_statement","return_statement", "if_statement", "expression_statement", "local_variable_declaration",
    "enhanced_for_statement", "while_statement", "continue_statement", "switch_block_statement_group",
    "break_statement", "throw_statement", "switch_expression", "try_statement", "switch_rule",
    "import_declaration", "class_declaration", "method_declaration", "catch_clause"
    ]
notypespace = ["generic_type", "scoped_type_identifier", "array_type", "type_arguments", "object_creation_expression", "array_creation_expression"]
def ll_deparse(node, indent=0, hasindent=True, newline=True):
    if node.type in ["identifier", "decimal_integer_literal", "hex_integer_literal", "octal_integer_literal", "binary_integer_literal", "decimal_floating_point_literal", "hex_floating_point_literal", "character_literal", "string_literal", "true", "false", "null_literal"]:
        return [node.text.decode("utf8")]
    elif node.type in ["integral_type", "type_identifier", "boolean_type", "floating_point_type"]:
        if node.parent.type not in notypespace:
            return [node.text.decode("utf8") + " "]
        else:
            return [node.text.decode("utf8")]
    elif node.type == ",":
        return [", "]
    elif node.type == ":":
        return [": "]
    elif node.type == "?":
        return ["? "]
    elif node.type == "->":
        return [" -> "]
    elif node.type in keywords_with_space:
        if node.child_count == 0:
            return [node.text.decode("utf8") + " "]
    elif node.type == "instanceof":
        return [" instanceof "]
    elif node.type == "block_comment":
        return [" " * indent * 4 + node.text.decode("utf8") + "\n"]
    elif node.type == "line_comment":
        return [" " * indent * 4 + node.text.decode("utf8") + "\n"]
    if node.child_count == 0:
        return [node.type]
    returnlist = []

    def add_statement(node, indent):
        if node.type == "block":
            return ll_deparse(node, indent)
        else:
            return ["\n"] + ll_deparse(node, indent + 1) 
    if node.type in indentstatements and hasindent:
        returnlist.append(" " * indent * 4)

    
    if node.type in ["block", "class_body", "switch_block"]:
        returnlist.append(" " + "{\n")
        for child in node.children[1:-1]:
            returnlist.append(ll_deparse(child, indent + 1))
        returnlist.append(" " * indent * 4 + "}")
        returnlist.append("\n")
    elif node.type in ["method_invocation"]:
        for child in node.children[1:]:
            returnlist.append(ll_deparse(child, indent))
    elif node.type == "for_statement":
        for i in range(node.child_count - 1):
            if i == 2:
                returnlist.append(ll_deparse(node.children[i], indent, False, False))
            else:
                returnlist.append(ll_deparse(node.children[i], indent))
        returnlist.append(add_statement(node.children[-1], indent))
    elif node.type == "enhanced_for_statement":
        returnlist.append("for ")
        for child in node.children[1:-1]:
            returnlist.append(ll_deparse(child, indent))
        returnlist.append(add_statement(node.children[-1], indent))
    elif node.type == "if_statement":
        for i in range(2):
            returnlist.append(ll_deparse(node.children[i], indent))
        returnlist.append(add_statement(node.children[2], indent))
        if node.child_count > 3:
            returnlist.append(" " * indent * 4 + "else")
            if node.children[4].type == "if_statement":
                returnlist.append(" ")
                returnlist.append(ll_deparse(node.children[4], indent, False))
            else:
                returnlist.append(add_statement(node.children[4], indent))
    elif node.type == "while_statement":
        for i in range(2):
            returnlist.append(ll_deparse(node.children[i], indent))
        returnlist.append(add_statement(node.children[2], indent))
    elif node.type in ["binary_expression", "assignment_expression"]:
        returnlist.append(ll_deparse(node.children[1], indent))
        returnlist.append(" " + node.children[0].text.decode("utf8") + " ")
        returnlist.append(ll_deparse(node.children[2], indent))
    elif node.type in ['unary_expression']:
        if node.children[0].type == "NEG":
            returnlist.append("-")
        else:
            returnlist.append(ll_deparse(node.children[0], indent))
        returnlist.append(ll_deparse(node.children[1], indent))
    elif node.type == "update_expression":
        if node.children[0].type == "INC":
            returnlist.append("++")
            returnlist.append(ll_deparse(node.children[1], indent))
        else:
            returnlist.append(ll_deparse(node.children[1], indent))
            if node.children[0].type == "PDEC":
                returnlist.append("--")
            elif node.children[0].type == "PINC":
                returnlist.append("++")
    elif node.type == "instanceof_expression":
        returnlist.append(ll_deparse(node.children[1], indent))
        returnlist.append(" instanceof ")
        for child in node.children[2:]:
            returnlist.append(deparse_ll(child, indent))    
    elif node.type == "variable_declarator":
        for child in node.children:
            if child.type == "=":
                returnlist.append(" = ")
            else:
                returnlist.append(ll_deparse(child, indent))
    elif node.type == "switch_rule":
        for i in range(2):
            returnlist.append(ll_deparse(node.children[i], indent))
        returnlist.append(ll_deparse(node.children[2], indent, False))
    elif node.type == "switch_block_statement_group":
        for i in range(2):
            returnlist.append(ll_deparse(node.children[i], indent))
        if node.child_count > 2:
            returnlist.append(add_statement(node.children[2], indent))
        else:
            returnlist.append("\n")
    elif node.type == "marker_annotation":
        for child in node.children:
            returnlist.append(ll_deparse(child, indent))
        returnlist.append("\n" + " " * indent * 4)
    else:
        for child in node.children:
            returnlist.append(ll_deparse(child, indent))
    if node.type in newlinestatements and newline:
        returnlist.append("\n")
    if node.type in ["scoped_type_identifier", "generic_type", "array_type"] and node.parent.type not in notypespace:
        returnlist.append(" ")
    return returnlist    
keywords_with_space = ["case", "catch", "class", "else", "for", "if", "import", "public", "return", "static", "switch", "throw", "throws", "try", "while", "new"]
newlinestatements = [
    "return_statement", "expression_statement", "continue_statement", 
    "break_statement", "throw_statement", "import_declaration", "local_variable_declaration",
    ]
indentstatements = [
    "for_statement","return_statement", "if_statement", "expression_statement", "local_variable_declaration",
    "enhanced_for_statement", "while_statement", "continue_statement", "switch_block_statement_group",
    "break_statement", "throw_statement", "switch_expression", "try_statement", "switch_rule",
    "import_declaration", "class_declaration", "method_declaration", "catch_clause"
    ]
notypespace = ["generic_type", "scoped_type_identifier", "array_type", "type_arguments", "object_creation_expression", "array_creation_expression"]

def deparse(node, indent=0, hasindent=True, newline=True):
    if node.type in ["identifier", "decimal_integer_literal", "hex_integer_literal", "octal_integer_literal", "binary_integer_literal", "decimal_floating_point_literal", "hex_floating_point_literal", "character_literal", "string_literal", "true", "false", "null_literal"]:
        return node.text.decode("utf8")
    elif node.type in ["integral_type", "type_identifier", "boolean_type", "floating_point_type"]:
        if node.parent.type not in notypespace:
            return node.text.decode("utf8") + " "
        else:
            return node.text.decode("utf8")
    elif node.type == ",":
        return ", "
    elif node.type == ":":
        return ": "
    elif node.type == "?":
        return "? "
    elif node.type == "->":
        return " -> "
    elif node.type in keywords_with_space:
        if node.child_count == 0:
            return node.text.decode("utf8") + " "
    elif node.type == "instanceof":
        return " instanceof "
    elif node.type == "block_comment":
        return " " * indent * 4 + node.text.decode("utf8") + "\n"
    elif node.type == "line_comment":
        # return " " * indent * 4 + node.text.decode("utf8") + "\n"
        return ""
    if node.child_count == 0:
        return node.type
    returnlist = []

    def add_statement(node, indent):
        if node.type == "block":
            return deparse(node, indent)
        else:
            return ["\n"] + deparse(node, indent + 1) 
    if node.type in indentstatements and hasindent:
        returnlist.append(" " * indent * 4)
    if node.type in ["block", "class_body", "switch_block"]:
        returnlist.append(" " + "{\n")
        for child in node.children[1:-1]:
            returnlist += deparse(child, indent + 1)
        returnlist.append(" " * indent * 4 + "}")
        returnlist.append("\n")
    elif node.type == "for_statement":
        for i in range(node.child_count - 1):
            if i == 2:
                returnlist += deparse(node.children[i], indent, False, False)
            else:
                returnlist += deparse(node.children[i], indent)
        returnlist += add_statement(node.children[-1], indent)
    elif node.type == "enhanced_for_statement":
        for child in node.children[:-1]:
            returnlist += deparse(child, indent)
        returnlist += add_statement(node.children[-1], indent)
    elif node.type == "if_statement":
        for i in range(2):
            returnlist += deparse(node.children[i], indent)
        returnlist += add_statement(node.children[2], indent)
        if node.child_count > 3:
            returnlist.append(" " * indent * 4 + "else")
            if node.children[4].type == "if_statement":
                returnlist.append(" ")
                returnlist += deparse(node.children[4], indent, False)
            else:
                returnlist += add_statement(node.children[4], indent)
    elif node.type == "while_statement":
        for i in range(2):
            returnlist += deparse(node.children[i], indent)
        returnlist += add_statement(node.children[2], indent)
    elif node.type in ["binary_expression", "assignment_expression"]:
        returnlist += deparse(node.children[0], indent)
        returnlist.append(" " + node.children[1].text.decode("utf8") + " ")
        returnlist += deparse(node.children[2], indent)
    elif node.type == "variable_declarator":
        for child in node.children:
            if child.type == "=":
                returnlist.append(" = ")
            else:
                returnlist += deparse(child, indent)
    elif node.type == "switch_rule":
        for i in range(2):
            returnlist += deparse(node.children[i], indent)
        returnlist += deparse(node.children[2], indent, False)
    elif node.type == "switch_block_statement_group":
        for i in range(2):
            returnlist += deparse(node.children[i], indent)
        if node.child_count > 2:
            returnlist += add_statement(node.children[2], indent)
        else:
            returnlist.append("\n")
    elif node.type == "marker_annotation":
        for child in node.children:
            returnlist += deparse(child, indent)
        returnlist.append("\n" + " " * indent * 4)
    else:
        for child in node.children:
            returnlist += deparse(child, indent)
    if node.type in newlinestatements and newline:
        returnlist.append("\n")
    if node.type in ["scoped_type_identifier", "generic_type", "array_type"] and node.parent.type not in notypespace:
        returnlist.append(" ")
    return returnlist    
def stringfy(lst):
    if isinstance(lst, str):
        return lst
    return "".join([stringfy(l) for l in lst])
    
def parse2normal(code):
    try:            
        tree = parser.parse(bytes(code, "utf8"))
        root_node = tree.root_node
        return stringfy(deparse(root_node))
    except:
        return ""
def parse2ll(code):
    try:
        tree = parser.parse(bytes(code, "utf8"))
        root_node = tree.root_node
        return stringfy(deparse_ll(root_node))
    except:
        return ""
def parsell(code):
    try:
        tree = parser2.parse(bytes(code, "utf8"))
        root_node = tree.root_node
        # l = ll_deparse(root_node)
        # return stringfy(l[0]) + stringfy(l[1]) + stringfy(l[2][:3]) + stringfy(l[2][3][:3]) + '}'
        return stringfy(ll_deparse(root_node))
    except:
        return ""