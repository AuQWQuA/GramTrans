
from tree_sitter import Language, Parser
import tree_sitter_mathqapythonll1
import tree_sitter_mathqapythonll2
import tree_sitter_mathqapythoncsg
import json
import re
import tempfile
import argparse
import os
parser1 = Parser(Language(tree_sitter_mathqapythonll1.language()))
parser2 = Parser(Language(tree_sitter_mathqapythonll2.language()))
parser3 = Parser(Language(tree_sitter_mathqapythoncsg.language()))

argparser = argparse.ArgumentParser()
argparser.add_argument("--file_name", type=str, default="DSL_LL1")
argparser.add_argument("--language", type=str, default="LL1")
args = argparser.parse_args()
file_name = args.file_name
language = args.language

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
def converse_ll1(text):
    return stringfy(ll1deparse_normal(parser1.parse(bytes(text, "utf-8")).root_node))
def converse_ll2(text):
    return stringfy(ll2deparse_normal(parser2.parse(bytes(text, "utf-8")).root_node))
def converse_csg(text):
    return stringfy(csgdeparse_normal(parser3.parse(bytes(text, "utf-8")).root_node))
def truncate_at_answer(text):
    match = re.search(r'(?m)^.*\banswer\b.*$', text)
    if match:
        return text[:match.end()].strip() 
    return text 

def run_script_and_check_answer(script, expected_answer, converse = ""):
    if converse == "ll1":
        try: 
            script = converse_ll1(script)
        except Exception as e:
            # print(f"Error converting to LL1: {e}")
            return False
    elif converse == "ll2":
        try: 
            script = converse_ll2(script)
        except Exception as e:
            # print(f"Error converting to LL2: {e}")
            return False
    elif converse == "csg":
        try: 
            script = converse_csg(script)
            if script == False:
                # print(f"Error converting to CSG, csg ERROR")
                return False
        except Exception as e:
            # print(f"Error converting to CSG: {e}")
            return False
    with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as temp_file:
        temp_file.write(script)
        temp_file_path = temp_file.name
    
    try:
        exec_globals = {}
        with open(temp_file_path, 'r') as f:
            exec(f.read(), exec_globals)
        
        script_answer = exec_globals.get('answer', None)
        assert script_answer == expected_answer, f"Assertion failed: expected {expected_answer}, got {script_answer}"
        return True
    except Exception as e:
        # print(f"Error executing script: {e}")
        return False
    finally:
        os.remove(temp_file_path)  

def evaluate_scripts(datas, language):
    correct_count = 0
    total = len(datas)
    
    for i in range(total):
        script_text = datas[i]['output'] 
        expected_answer = datas[i]['answer'] 
        truncated_script = truncate_at_answer(script_text)  
        
        if language == "LL1":
            if run_script_and_check_answer(truncated_script, expected_answer, "ll1"):
                correct_count += 1
        elif language == "LL2":
            if run_script_and_check_answer(truncated_script, expected_answer, "ll2"):
                correct_count += 1
        elif language == "NCFG":
            if run_script_and_check_answer(truncated_script, expected_answer, "csg"):
                correct_count += 1
        else:
            if run_script_and_check_answer(truncated_script, expected_answer, ""):
                correct_count += 1
    
    print(f"Correct scripts: {correct_count}/{total}")
    return correct_count

with open(f"./output/{file_name}.jsonl", "r") as f:
    datas = [json.loads(l) for l in f]
correct_count = evaluate_scripts(datas, language)
