import tree_sitter_mathqapython
import tree_sitter_mathqapythonll1
import tree_sitter_mathqapythonll2
import tree_sitter_mathqapythoncsg
from tree_sitter import Language, Parser
from typing import cast
parser = Parser(Language(cast(object, (tree_sitter_mathqapython.language()))))
def deparse(node):
    if node.child_count == 0:
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
        return node.type
    returnlist = [deparse(node.child(i)) for i in range(node.child_count) if node.child(i).type != 'comment']
    if node.type in ["expression_statement"]:
        returnlist += ["\n"]
    elif node.type in ["binary_operator", "assignment"]:
        returnlist = [returnlist[0], " ", returnlist[1], " ", returnlist[2]]
    elif node.type in ["import_statement"]:
        returnlist = [returnlist[0]," ", returnlist[1], "\n"]
    elif node.type in ["lambda"]:
        returnlist = [returnlist[0], " ", returnlist[1], returnlist[2], " ", returnlist[3]]
    return returnlist

def deparse_ll1(node):
    if node.child_count == 0:
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
        return node.type
    returnlist = [deparse_ll1(node.child(i)) for i in range(node.child_count) if node.child(i).type != 'comment']
    if node.type in ['unary_operator']:
        returnlist = ['neg', ' ', returnlist[1]]
    if node.type in ["expression_statement"]:
        returnlist += ["\n"]
    elif node.type in ["assignment"]:
        returnlist = [returnlist[0], " ", returnlist[1], " ", returnlist[2]]
    elif node.type in ["binary_operator"]:
        returnlist = [returnlist[1], " ", returnlist[0], " ", returnlist[2]]
    elif node.type in ["import_statement"]:
        returnlist = [returnlist[0]," ", returnlist[1], "\n"]
    elif node.type in ["lambda"]:
        returnlist = [returnlist[0], " ", returnlist[1], returnlist[2], " ", returnlist[3]]
    elif node.type in ["call"]:
        returnlist = ["call", " ", returnlist[0], returnlist[1]]
    elif node.type in ["attribute"]:
        returnlist = ["attr", " ", returnlist[0], returnlist[1], returnlist[2]]
    return returnlist
def ll1deparse_normal(node):
    if node.child_count == 0:
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
        return node.type
    returnlist = [ll1deparse_normal(node.child(i)) for i in range(node.child_count) if node.child(i).type != 'comment']
    if node.type in ['unary_operator']:
        returnlist = ['-', returnlist[1]]
    if node.type in ["expression_statement"]:
        returnlist += ["\n"]
    elif node.type in ["assignment"]:
        returnlist = [returnlist[0], " ", returnlist[1], " ", returnlist[2]]
    elif node.type in ["binary_operator"]:
        returnlist = [returnlist[1], " ", returnlist[0], " ", returnlist[2]]
    elif node.type in ["import_statement"]:
        returnlist = [returnlist[0]," ", returnlist[1], "\n"]
    elif node.type in ["lambda"]:
        returnlist = [returnlist[0], " ", returnlist[1], returnlist[2], " ", returnlist[3]]
    elif node.type in ["call"]:
        returnlist = [returnlist[1], returnlist[2]]
    elif node.type in ["attribute"]:
        returnlist = [returnlist[1], returnlist[2], returnlist[3]]
    return returnlist
def deparse_ll2(node):
    if node.child_count == 0:
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
        return node.type
    returnlist = [deparse_ll2(node.child(i)) for i in range(node.child_count) if node.child(i).type != 'comment']
    if node.type in ['unary_operator']:
        returnlist = ["ll", " ", 'neg', ' ', returnlist[1]]
    if node.type in ["expression_statement"]:
        returnlist += ["\n"]
    elif node.type in ["assignment"]:
        returnlist = ["ll", " ", returnlist[0], " ", returnlist[1], " ", returnlist[2]]
    elif node.type in ["binary_operator"]:
        returnlist = ["ll", " ", returnlist[1], " ", returnlist[0], " ", returnlist[2]]
    elif node.type in ["import_statement"]:
        returnlist = ["ll", " ", returnlist[0]," ", returnlist[1], "\n"]
    elif node.type in ["lambda"]:
        returnlist = ["ll", " ", returnlist[0], " ", returnlist[1], returnlist[2], " ", returnlist[3]]
    elif node.type in ["call"]:
        returnlist = ["ll", " ", "call", " ", returnlist[0], returnlist[1]]
    elif node.type in ["attribute"]:
        returnlist = ["ll", " ", "attr", " ", returnlist[0], returnlist[1], returnlist[2]]
    elif node.type in ["parenthesized_expression"]:
        returnlist = ["ll", " ", returnlist[0], returnlist[1], returnlist[2]]
    return returnlist
def ll2deparse_normal(node):
    if node.child_count == 0:
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
        return node.type
    returnlist = [ll2deparse_normal(node.child(i)) for i in range(node.child_count) if node.child(i).type != 'comment']
    if node.type in ['unary_operator']:
        returnlist = ['-', returnlist[2]]
    if node.type in ["expression_statement"]:
        returnlist += ["\n"]
    elif node.type in ["assignment"]:
        returnlist = [returnlist[1], " ", returnlist[2], " ", returnlist[3]]
    elif node.type in ["binary_operator"]:
        returnlist = [returnlist[2], " ", returnlist[1], " ", returnlist[3]]
    elif node.type in ["import_statement"]:
        returnlist = [returnlist[1]," ", returnlist[2], "\n"]
    elif node.type in ["lambda"]:
        returnlist = [returnlist[1], " ", returnlist[2], returnlist[3], " ", returnlist[4]]
    elif node.type in ["call"]:
        returnlist = [returnlist[2], returnlist[3]]
    elif node.type in ["attribute"]:
        returnlist = [returnlist[2], returnlist[3], returnlist[4]]
    elif node.type in ["parenthesized_expression"]:
        returnlist = [returnlist[1], returnlist[2], returnlist[3]]
    return returnlist
def deparse_csg(node):
    if node.child_count == 0:
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
        elif node.type == "comment":
            return node.text.decode("utf8")
        return node.type
    returnlist = [deparse_csg(node.child(i)) for i in range(node.child_count) if node.child(i).type != 'comment']
    if node.type in ["expression_statement"]:
        returnlist += ["\n"]
    elif node.type in ["binary_operator"]:
        returnlist = [returnlist[0], " ", returnlist[1], " ", returnlist[2]]
    elif node.type in ["import_statement"]:
        returnlist = [returnlist[0]," ", returnlist[1], "\n"]
    elif node.type in ["lambda"]:
        returnlist = [returnlist[0], " ", returnlist[1], returnlist[2], " ", returnlist[3]]
    elif node.type in ["assignment"]:
        returnlist = [returnlist[0], " ", returnlist[1], " ", returnlist[2], " ", ";", " ", returnlist[0]]
    return returnlist
def csgdeparse_normal(node):
    def stringfy(lst):
        if isinstance(lst, str):
            return lst
        return "".join([stringfy(l) for l in lst])
    if node.child_count == 0:
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
        elif node.type == "comment":
            return node.text.decode("utf8")
        return node.type
    returnlist = [csgdeparse_normal(node.child(i)) for i in range(node.child_count) if node.child(i).type != 'comment']
    if False in returnlist:
        return False
    if node.type in ["expression_statement"]:
        returnlist += ["\n"]
    elif node.type in ["binary_operator"]:
        returnlist = [returnlist[0], " ", returnlist[1], " ", returnlist[2]]
    elif node.type in ["import_statement"]:
        returnlist = [returnlist[0]," ", returnlist[1], "\n"]
    elif node.type in ["lambda"]:
        returnlist = [returnlist[0], " ", returnlist[1], returnlist[2], " ", returnlist[3]]
    elif node.type in ["assignment"]:
        if stringfy(returnlist[0]) != stringfy(returnlist[4]):
            return False
        returnlist = [returnlist[0], " ", returnlist[1], " ", returnlist[2]]
    return returnlist
def stringfy(lst):
    if isinstance(lst, str):
        return lst
    return "".join([stringfy(l) for l in lst])