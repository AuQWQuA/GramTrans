import json
from tree_sitter import Language, Parser
from tree_sitter_java import language as javalang
parser = Parser(Language(javalang()))

used_rules = {}
inlinenodes = grammar['inline'] + [key for key in grammar['rules'].keys() if key.startswith("_")] + grammar['supertypes']
root = parser.parse(bytes(data[0]['code'], "utf-8")).root_node
external_inline = [item['name'] for item in grammar['externals'] if item['type'] == "SYMBOL" and item['name'].startswith("_")]
external_symbols = [item['name'] for item in grammar['externals'] if item['type'] == "SYMBOL" and not item['name'].startswith("_") and item['name'] != "comment"]

class PsuedoNode:
    def __init__(self, node, type):
        self.type = type
        self.children = []
        self.named_children = []
        for child in node.children:
            self.children.append(child)
        for child in node.named_children:
            self.named_children.append(child)

def get_used_rules(node):
    rule = grammar['rules'][node.type]
    
    children = [child for child in node.children if child.type not in ["block_comment","line_comment", "line_continuation"]]

    def merge_matchparts(part1, part2):
        if part1['type'] != part2['type']:
            return False, None
        mergepart = {}
        mergepart['type'] = part1['type']
        if mergepart['type'] == 'SEQ':
            mergepart['members'] = []
            if len(part1['members']) != len(part2['members']):
                return False, None
            for i in range(len(part1['members'])):
                issuccess, submergepart = merge_matchparts(part1['members'][i], part2['members'][i])
                if not issuccess:
                    return False, None
                else:
                    mergepart['members'].append(submergepart)
            return True, mergepart
        elif mergepart['type'] == 'CHOICE':
            mergepart['members'] = []
            matched_indices = [False] * len(part2['members'])
            for member in part1['members']:
                matched = False
                for i in range(len(part2['members'])):
                    if not matched_indices[i]:
                        issuccess, submergepart = merge_matchparts(member, part2['members'][i])
                        if issuccess:
                            mergepart['members'].append(submergepart)
                            matched_indices[i] = True
                            matched = True
                            break
                if not matched:
                    mergepart['members'].append(member)
            for i, member in enumerate(part2['members']):
                if not matched_indices[i]:
                    mergepart['members'].append(member)
            return True, mergepart
        elif mergepart['type'] == 'REPEAT':
            if part1['content'] == {"type": "BLANK"}:
                return True, part2
            elif part2['content'] == {"type": "BLANK"}:
                return True, part1
            else:
                issuccess, mergepart['content'] = merge_matchparts(part1['content'], part2['content'])
                if issuccess:
                    return True, mergepart
                else:
                    return False, None

        elif mergepart['type'] == 'REPEAT1':
            issuccess, mergepart['content'] = merge_matchparts(part1['content'], part2['content'])
            if issuccess:
                return True, mergepart
            else:
                return False, None
        elif mergepart['type'] == 'PREC':
            if part1['value'] != part2['value']:
                return False, None
            else:
                mergepart['value'] = part1['value']
            issuccess, mergepart['content'] = merge_matchparts(part1['content'], part2['content'])
            if issuccess:
                return True, mergepart
            else:
                return False, None        
        elif mergepart['type'] == 'PREC_LEFT':
            if part1['value'] != part2['value']:
                return False, None
            else:
                mergepart['value'] = part1['value']
            issuccess, mergepart['content'] = merge_matchparts(part1['content'], part2['content'])
            if issuccess:
                return True, mergepart
            else:
                return False, None
        elif mergepart['type'] == 'PREC_RIGHT':
            if part1['value'] != part2['value']:
                return False, None
            else:
                mergepart['value'] = part1['value']
            issuccess, mergepart['content'] = merge_matchparts(part1['content'], part2['content'])
            if issuccess:
                return True, mergepart
            else:
                return False, None
        elif mergepart['type'] == 'PREC_DYNAMIC':
            if part1['value'] != part2['value']:
                return False, None
            else:
                mergepart['value'] = part1['value']
            issuccess, mergepart['content'] = merge_matchparts(part1['content'], part2['content'])
            if issuccess:
                return True, mergepart
            else:
                return False, None   
        elif mergepart['type'] == 'STRING':
            if part1['value'] != part2['value']:
                return False, None
            else:
                mergepart['value'] = part1['value']
            return True, mergepart
        elif mergepart['type'] == 'BLANK':
            return True, mergepart
        elif mergepart['type'] == 'SYMBOL':
            if part1['name'] != part2['name']:
                return False, None
            else:
                mergepart['name'] = part1['name']
            return True, mergepart
        elif mergepart['type'] == 'FIELD':
            if part1['name'] != part2['name']:
                return False, None
            else:
                mergepart['name'] = part1['name']
            issuccess, mergepart['content'] = merge_matchparts(part1['content'], part2['content'])
            if issuccess:
                return True, mergepart
            else:
                return False, None
        elif mergepart['type'] == 'ALIAS':
            if part1['value'] != part2['value']:
                return False, None
            elif part1['named'] != part2['named']:
                return False, None
            issuccess, mergepart['content'] = merge_matchparts(part1['content'], part2['content'])
            if issuccess:
                mergepart['value'] = part1['value']
                mergepart['named'] = part1['named']
                return True, mergepart
            else:
                return False, None
        else:
            assert False, "NEW MERGE PART" + mergepart['type']


    def match_subpart(subpart, children):
        matchpart = {}
        matchchildren = []
        matchsymbol = []
        matchnewrules = []
        
        if subpart['type'] == 'SEQ':
            matchpart['type'] = 'SEQ'
            matchpart['members'] = []
            for member in subpart['members']:
                success, submatchpart, submatchchildren, submatchsymbol, submatchnewrules = match_subpart(member, children[len(matchchildren):])
                if success:
                    matchpart['members'].append(submatchpart)
                    matchchildren += submatchchildren
                    matchsymbol += submatchsymbol
                    matchnewrules += submatchnewrules
                else:
                    return False, {}, [], [], []
            return True, matchpart, matchchildren, matchsymbol, matchnewrules
        
        elif subpart['type'] == 'CHOICE':
            matchpart['type'] = 'CHOICE'
            matchpart['members'] = []
            tempsuccess = []
            blanknum = -1
            for member in subpart['members']:
                success, submatchpart, submatchchildren, submatchsymbol, submatchnewrules = match_subpart(member, children)
                if success:
                    if submatchpart == {"type": "BLANK"}:
                        blanknum = len(tempsuccess)
                    tempsuccess.append((submatchpart, submatchchildren, submatchsymbol, submatchnewrules))
            if len(tempsuccess) == 1:
                matchpart['members'] = [tempsuccess[0][0]]
                matchchildren = tempsuccess[0][1]
                matchsymbol = tempsuccess[0][2]
                matchnewrules = tempsuccess[0][3]
                return True, matchpart, matchchildren, matchsymbol, matchnewrules
            elif blanknum != -1 and len(tempsuccess) == 2:
                matchpart['members'] = [tempsuccess[1-blanknum][0]]
                matchchildren = tempsuccess[1-blanknum][1]
                matchsymbol = tempsuccess[1-blanknum][2]
                matchnewrules = tempsuccess[1-blanknum][3]
                return True, matchpart, matchchildren, matchsymbol, matchnewrules
            elif len(tempsuccess) == 3 and children[0].type == "block":
                if children[0].start_point == children[0].end_point:
                    matchpart['members'] = [tempsuccess[2][0]]
                    matchchildren = tempsuccess[2][1]
                    matchsymbol = tempsuccess[2][2]
                    matchnewrules = tempsuccess[2][3]
                    return True, matchpart, matchchildren, matchsymbol, matchnewrules
                elif children[0].start_point[0] == children[0].parent.start_point[0]:
                    matchpart['members'] = [tempsuccess[0][0]]
                    matchchildren = tempsuccess[0][1]
                    matchsymbol = tempsuccess[0][2]
                    matchnewrules = tempsuccess[0][3]
                    return True, matchpart, matchchildren, matchsymbol, matchnewrules
                elif children[0].start_point[0] > children[0].parent.start_point[0]:
                    matchpart['members'] = [tempsuccess[1][0]]
                    matchchildren = tempsuccess[1][1]
                    matchsymbol = tempsuccess[1][2]
                    matchnewrules = tempsuccess[1][3]
                    return True, matchpart, matchchildren, matchsymbol, matchnewrules
                else:
                    print(children[0].start_point, children[0].parent.start_point)
                    assert False, "Cannot match choice"
            elif len(tempsuccess) > 1:
                if len(tempsuccess) == 2 and len(tempsuccess[0][1]) > len(tempsuccess[1][1]):
                    matchpart['members'] = [tempsuccess[0][0]]
                    matchchildren = tempsuccess[0][1]
                    matchsymbol = tempsuccess[0][2]
                    matchnewrules = tempsuccess[0][3]
                    return True, matchpart, matchchildren, matchsymbol, matchnewrules
                elif len(tempsuccess) == 2 and len(tempsuccess[0][1]) < len(tempsuccess[1][1]):
                    matchpart['members'] = [tempsuccess[1][0]]
                    matchchildren = tempsuccess[1][1]
                    matchsymbol = tempsuccess[1][2]
                    matchnewrules = tempsuccess[1][3]
                    return True, matchpart, matchchildren, matchsymbol, matchnewrules
                elif len(tempsuccess) == 2 and len(tempsuccess[0][1]) == len(tempsuccess[1][1]) and len(tempsuccess[0][1]) == 1:
                    if tempsuccess[0][0]['type'] == "SYMBOL":
                        matchpart['members'] = [tempsuccess[0][0]]
                        matchchildren = tempsuccess[0][1]
                        matchsymbol = tempsuccess[0][2]
                        matchnewrules = tempsuccess[0][3]
                        return True, matchpart, matchchildren, matchsymbol, matchnewrules
                    elif tempsuccess[1][0]['type'] == "SYMBOL":
                        matchpart['members'] = [tempsuccess[1][0]]
                        matchchildren = tempsuccess[1][1]
                        matchsymbol = tempsuccess[1][2]
                        matchnewrules = tempsuccess[1][3]
                        return True, matchpart, matchchildren, matchsymbol, matchnewrules
                    else:
                        print(subpart)
                        print("Ambiguous choice")
                        for temp in tempsuccess:
                            print(temp)
                        assert False, "Ambiguous choice"
                elif len(tempsuccess) == 2 and len(tempsuccess[0][1]) == len(tempsuccess[1][1]) and len(tempsuccess[0][1]) > 1:
                    if len(json.dumps(tempsuccess[0][0])) < len(json.dumps(tempsuccess[1][0])):
                        matchpart['members'] = [tempsuccess[0][0]]
                        matchchildren = tempsuccess[0][1]
                        matchsymbol = tempsuccess[0][2]
                        matchnewrules = tempsuccess[0][3]
                        return True, matchpart, matchchildren, matchsymbol, matchnewrules
                    elif len(json.dumps(tempsuccess[0][0])) >= (json.dumps(tempsuccess[1][0])):
                        matchpart['members'] = [tempsuccess[1][0]]
                        matchchildren = tempsuccess[1][1]
                        matchsymbol = tempsuccess[1][2]
                        matchnewrules = tempsuccess[1][3]
                        return True, matchpart, matchchildren, matchsymbol, matchnewrules
                else:
                    print(subpart)
                    print("Ambiguous choice")
                    for temp in tempsuccess:
                        print(temp)
                    assert False, "Ambiguous choice"
                    
            else:
                return False, {}, [], [], []
        elif subpart['type'] == 'REPEAT':
            matchpart['type'] = 'REPEAT'
            matchpart['content'] = {"type": "BLANK"}
            matchparts = []
            while len(children) > len(matchchildren):
                success, submatchpart, submatchchildren ,submatchsymbol, submatchnewrules= match_subpart(subpart['content'], children[len(matchchildren):])
                if success:
                    matchparts.append(submatchpart)
                    matchchildren += submatchchildren
                    matchsymbol += submatchsymbol
                    matchnewrules += submatchnewrules
                else:
                    break
            if len(matchparts) > 0:
                matchpart['content'] = matchparts[0]
                for i in range(1, len(matchparts)):
                    merge_success, matchpart['content'] = merge_matchparts(matchpart['content'], matchparts[i])
                    if not merge_success:
                        assert False, "Cannot merge repeat parts"
                return True, matchpart, matchchildren, matchsymbol, matchnewrules
            else:
                return True, matchpart, matchchildren, matchsymbol, matchnewrules

        elif subpart['type'] == 'REPEAT1':
            matchpart['type'] = 'REPEAT1'
            matchpart['content'] = {}
            matchparts = []
            while len(children) > len(matchchildren):
                success, submatchpart, submatchchildren, submatchsymbol, submatchnewrules = match_subpart(subpart['content'], children[len(matchchildren):])
                if success:
                    matchparts.append(submatchpart)
                    matchchildren += submatchchildren
                    matchsymbol += submatchsymbol
                    matchnewrules += submatchnewrules
                else:
                    break
            if len(matchparts) > 0:
                matchpart['content'] = matchparts[0]
                for i in range(1, len(matchparts)):
                    merge_success, matchpart['content'] = merge_matchparts(matchpart['content'], matchparts[i])
                    if not merge_success:
                        assert False, "Cannot merge repeat parts"
                return True, matchpart, matchchildren, matchsymbol, matchnewrules
            else:
                return False, {}, [], [], []
            
        elif subpart['type'] == 'PREC':
            matchpart['type'] = 'PREC'
            matchpart['value'] = subpart['value']
            success, submatchpart, submatchchildren, submatchsymbol, submatchnewrules = match_subpart(subpart['content'], children)
            if success:
                matchpart['content'] = submatchpart
                matchchildren = submatchchildren
                matchsymbol = submatchsymbol
                matchnewrules = submatchnewrules
                return True, matchpart, matchchildren, matchsymbol, matchnewrules
            else:
                return False, {}, [], [], []
        elif subpart['type'] == 'PREC_LEFT':
            matchpart['type'] = 'PREC_LEFT'
            matchpart['value'] = subpart['value']
            success, submatchpart, submatchchildren, submatchsymbol, submatchnewrules = match_subpart(subpart['content'], children)
            if success:
                matchpart['content'] = submatchpart
                matchchildren = submatchchildren
                matchsymbol = submatchsymbol
                matchnewrules = submatchnewrules
                return True, matchpart, matchchildren, matchsymbol, matchnewrules
            else:
                return False, {}, [], [], []
        elif subpart['type'] == 'PREC_RIGHT':
            matchpart['type'] = 'PREC_RIGHT'
            matchpart['value'] = subpart['value']
            success, submatchpart, submatchchildren, submatchsymbol, submatchnewrules = match_subpart(subpart['content'], children)
            if success:
                matchpart['content'] = submatchpart
                matchchildren = submatchchildren
                matchsymbol = submatchsymbol
                matchnewrules = submatchnewrules
                return True, matchpart, matchchildren, matchsymbol, matchnewrules
            else:
                return False, {}, [], [], []
        elif subpart['type'] == 'PREC_DYNAMIC':
            matchpart['type'] = 'PREC_DYNAMIC'
            matchpart['value'] = subpart['value']
            success, submatchpart, submatchchildren, submatchsymbol, submatchnewrules = match_subpart(subpart['content'], children)
            if success:
                matchpart['content'] = submatchpart
                matchchildren = submatchchildren
                matchsymbol = submatchsymbol
                matchnewrules = submatchnewrules
                return True, matchpart, matchchildren, matchsymbol, matchnewrules
            else:
                return False, {}, [], [], []

        elif subpart['type'] == "BLANK":
            matchpart['type'] = "BLANK"
            return True, matchpart, matchchildren, matchsymbol, matchnewrules
        elif subpart['type'] == "SYMBOL":
            matchpart['type'] = "SYMBOL"
            if subpart['name'] in external_inline:
                matchpart['name'] = subpart['name']
                return True, matchpart, matchchildren, matchsymbol, matchnewrules
            if subpart['name'] in inlinenodes:
                success, submatchpart, submatchchildren, submatchsymbol, submatchnewrules = match_subpart(grammar['rules'][subpart['name']], children)
                if success:
                    matchpart['name'] = subpart['name']
                    matchnewrules.append({subpart['name']: submatchpart})
                    matchnewrules += submatchnewrules
                    matchchildren += submatchchildren    
                    matchsymbol += submatchsymbol                
                    return True, matchpart, matchchildren, matchsymbol, matchnewrules
                else:
                    return False, {}, [], [], []
            elif len(children) == 0:
                return False, {}, [], [], []
            elif subpart['name'] == children[0].type:
                matchpart['name'] = subpart['name']
                matchchildren.append(children[0])
                matchsymbol.append(children[0])
                return True, matchpart, matchchildren, matchsymbol, matchnewrules
            else:
                return False, {}, [], [], []
        elif subpart['type'] == 'FIELD':
            matchpart['type'] = 'FIELD'
            matchpart['name'] = subpart['name']
            success, submatchpart, submatchchildren, submatchsymbol, submatchnewrules = match_subpart(subpart['content'], children)
            if success:
                matchpart['content'] = submatchpart
                matchchildren = submatchchildren
                matchsymbol = submatchsymbol
                matchnewrules = submatchnewrules
                return True, matchpart, matchchildren, matchsymbol, matchnewrules
            else:
                return False, {}, [], [], []
        elif subpart['type'] == 'STRING':
            if len(children) == 0:
                return False, {}, [], [], []
            matchpart['type'] = 'STRING'
            if children[0].type == subpart['value']:
                matchpart['value'] = subpart['value']
                matchchildren.append(children[0])
                return True, matchpart, matchchildren, matchsymbol, matchnewrules
            else:
                return False, {}, [], [], []
        elif subpart['type'] == 'ALIAS':
            if len(children) == 0:
                return False, {}, [], [], []
            matchpart['type'] = 'ALIAS'
            if subpart['value'] == children[0].type:
                matchpart['named'] = subpart['named']
                if subpart['content']['type'] == 'SYMBOL':
                    if subpart['content']['name'] != "identifier":
                        matchsymbol.append(PsuedoNode(children[0], subpart['content']['name']))
                        matchpart['value'] = subpart['value']
                        matchpart['content'] = subpart['content']
                        matchchildren = [children[0]]
                        return True, matchpart, matchchildren, matchsymbol, matchnewrules
                    else:
                        if children[0].type == "type_identifier":
                            matchsymbol.append(PsuedoNode(children[0], "identifier"))
                            matchpart['value'] = subpart['value']
                            matchpart['content'] = subpart['content']
                            matchchildren = [children[0]]
                            return True, matchpart, matchchildren, matchsymbol, matchnewrules
                elif children[0].type == 'identifier':
                    text = children[0].text.decode("utf-8")

                    if subpart['content']['type'] == 'CHOICE':
                        for member in subpart['content']['members']:
                            if member['type'] == 'STRING':
                                if text == member['value']:
                                    matchpart['content'] = {'type': 'CHOICE', 'members': [member]}
                                    matchpart['value'] = subpart['value']
                                    matchchildren.append(children[0])
                                    return True, matchpart, matchchildren, matchsymbol, matchnewrules
                    elif subpart['content']['type'] == 'STRING':
                        if text == subpart['content']['value']:
                            matchpart['content'] = subpart['content']
                            matchpart['value'] = subpart['value']
                            matchchildren.append(children[0])
                            return True, matchpart, matchchildren, matchsymbol, matchnewrules                        
            return False, {}, [], [], []
            
        elif subpart['type'] == 'TOKEN' or subpart['type'] == 'IMMEDIATE_TOKEN' or subpart['type'] == "PATTERN":
            print("PATTERN")
            return True, matchpart, matchchildren, matchsymbol, matchnewrules
        else:
            assert False, "NEW SUBPART" + subpart['type']

    success, matchpart, matchchildren, matchsymbol, matchnewrules = match_subpart(rule, children)
    if matchchildren != children:
        assert False, "Not all children matched"

    if success:
        if node.type in used_rules:
            issuccess, mergepart = merge_matchparts(used_rules[node.type], matchpart)
            if not issuccess:
                print("wrong merge")
                print(used_rules[key])
                print(value)
                assert False, "Cannot merge rules"
            used_rules[node.type] = mergepart
        else:
            used_rules[node.type] = matchpart
    else:
        assert False, "Cannot match rule"

    for inlinerule in matchnewrules:
        for key, value in inlinerule.items():
            if key in used_rules:
                issuccess, mergepart = merge_matchparts(used_rules[key], value)
                if not issuccess:
                    print("wrong merge")
                    print(used_rules[key])
                    print(value)
                    assert False, "Cannot merge rules"
                used_rules[key] = mergepart
            else:
                used_rules[key] = value
    
    # for child in matchsymbol:
    #     if child.type not in ['identifier', 'integer', 'float'] and child.type not in external_symbols:
    #         print(child.type)
    
    for child in matchsymbol:
        if child.type not in ['identifier', "decimal_integer_literal", "hex_integer_literal", "octal_integer_literal", "binary_integer_literal", "decimal_floating_point_literal", "hex_floating_point_literal", "character_literal", "string_literal", "true", "false", "null_literal", "boolean_type", "void_type"] and child.type not in external_symbols:
            get_used_rules(child)

#如果CHOICE只有一个元素，就直接用这个元素，如果REPEAT只有BLANK，则去除，如果SEQ只有一个元素，则去除SEQ
def simplrule(rule):
    if "type" not in rule:
        print(rule)
    if rule['type'] == 'CHOICE':
        members = []
        for member in rule['members']:
            simplmember = simplrule(member)
            if simplmember not in members:
                members.append(simplmember)
        if len(members) == 1:
            if members[0] == {"type": "BLANK"}:
                return {"type": "BLANK"}
            else:
                return members[0]
        else:
            rule['members'] = members
            return rule
    elif rule['type'] == 'REPEAT':
        simplcontent = simplrule(rule['content'])
        if simplcontent == {"type": "BLANK"}:
            return {"type": "BLANK"}
        else:
            rule['content'] = simplcontent
            return rule
    elif rule['type'] == 'REPEAT1':
        simplcontent = simplrule(rule['content'])
        if simplcontent == {"type": "BLANK"}:
            return {"type": "BLANK"}
        else:
            rule['content'] = simplcontent
            return rule
    elif rule['type'] == 'SEQ':
        members = []
        for member in rule['members']:
            simplmember = simplrule(member)
            if simplmember != {"type": "BLANK"}:
                members.append(simplmember)
        if len(members) == 1:
            return members[0]
        else:
            rule['members'] = members
            return rule
    elif rule['type'] == 'PREC':
        simplcontent = simplrule(rule['content'])
        if simplcontent == {"type": "BLANK"}:
            return {"type": "BLANK"}
        else:
            rule['content'] = simplcontent
            return rule
    elif rule['type'] == 'PREC_LEFT':
        simplcontent = simplrule(rule['content'])
        if simplcontent == {"type": "BLANK"}:
            return {"type": "BLANK"}
        else:
            rule['content'] = simplcontent
            return rule
    elif rule['type'] == 'PREC_RIGHT':
        simplcontent = simplrule(rule['content'])
        if simplcontent == {"type": "BLANK"}:
            return {"type": "BLANK"}
        else:
            rule['content'] = simplcontent
            return rule
    elif rule['type'] == 'PREC_DYNAMIC':
        simplcontent = simplrule(rule['content'])
        if simplcontent == {"type": "BLANK"}:
            return {"type": "BLANK"}
        else:
            rule['content'] = simplcontent
            return rule
    elif rule['type'] == 'FIELD':
        simplcontent = simplrule(rule['content'])
        if simplcontent == {"type": "BLANK"}:
            return {"type": "BLANK"}
        else:
            rule['content'] = simplcontent
            return rule
    elif rule['type'] == 'ALIAS':
        simplcontent = simplrule(rule['content'])
        if simplcontent == {"type": "BLANK"}:
            return {"type": "BLANK"}
        else:
            rule['content'] = simplcontent
            return rule
    else:
        return rule
    
import json


def symbol_name_to_ref(name):
    """
    将 JSON 中的符号名转换为 tree-sitter 语法中的引用形式。
    比如 "_statement" -> $._statement, "identifier" -> $.identifier
    """
    # 你也可以根据需求决定是否保留下划线之类的规则，这里示例全部直接使用 $.<name>
    return f'$.{name}'

def convert_node(node):
    """
    将 JSON 中的一个节点（dict）转换为相应的 tree-sitter 语法字符串。
    """
    node_type = node["type"]
    
    if node_type == "SYMBOL":
        # SYMBOL => $.some_rule
        # 如果要在符号名前面保留下划线，则直接用它本身；否则可对下划线特殊处理
        return symbol_name_to_ref(node["name"])
    
    elif node_type == "STRING":
        # STRING => 'xxx'
        return f"'{node['value']}'"
    
    elif node_type == "FIELD":
        # FIELD => field('fieldName', <content>)
        return f"field('{node['name']}', {convert_node(node['content'])})"
    
    elif node_type == "SEQ":
        # SEQ => seq(..., ...)
        members_str = ", ".join(convert_node(m) for m in node["members"])
        return f"seq({members_str})"
    
    elif node_type == "CHOICE":
        # CHOICE => choice(..., ...)
        members_str = ", ".join(convert_node(m) for m in node["members"])
        return f"choice({members_str})"
    
    elif node_type == "REPEAT":
        # REPEAT => repeat(...)
        # 如果需要 repeat1，则改这里
        return f"repeat({convert_node(node['content'])})"
    
    elif node_type == "REPEAT1":
        # 如果 JSON 中可能出现 REPEAT1，可以在这里处理
        return f"repeat1({convert_node(node['content'])})"
    
    elif node_type in ("PREC_LEFT", "PREC_RIGHT", "PREC", "PREC_DYNAMIC"):
        # 例如 PREC_LEFT => prec.left(value, <content>)
        #     PREC_RIGHT => prec.right(value, <content>)
        #     PREC => prec(value, <content>)
        value = node["value"]
        content_str = convert_node(node["content"])
        # 可能是负数，也可能是正数，所以要直接把 value 放进去
        if node_type == "PREC_LEFT":
            return f"prec.left({value}, {content_str})"
        elif node_type == "PREC_RIGHT":
            return f"prec.right({value}, {content_str})"
        else:
            # 普通 prec
            return f"prec({value}, {content_str})"
    elif node_type == "ALIAS":
        # ALIAS => alias(...)
        # 如果 named 为 True，则是 alias.as，否则是 alias
        named = "true" if node["named"] else "false"
        return f"alias({convert_node(node['content'])}, {node['value']})"
    elif node_type == "BLANK":
        return "blank"
    
    else:
        # 如果出现未定义的类型，这里可以抛错或者根据需求自行处理
        raise ValueError(f"Unknown node type: {node_type}")

def convert_json_to_js(json_dict):
    """
    将最外层的 JSON dict（若干规则）转换成多行的 tree-sitter 语法字符串。
    假设每个 key 都对应一个 ruleName。
    """
    lines = []
    for rule_name, rule_def in json_dict.items():
        # 如果这个条目不是一个 dict 或者没有 'type'，可能不符合你想要的规则结构，可酌情跳过
        if not isinstance(rule_def, dict) or 'type' not in rule_def:
            continue
        
        # 将该 rule 转换成 JS 语法
        converted_str = convert_node(rule_def)
        # 形如: module: $ => repeat($._statement),
        line = f"{rule_name}: $ => {converted_str},"
        lines.append(line)
    
    return "\n".join(lines)
convert_json_to_js(used_rules)
with open("temp.js", "w") as f:
    f.write(convert_json_to_js(used_rules))


def find_symbols(data, symbols=set()):
    if isinstance(data, dict):
        # 如果字典中的 "type" 是 "SYMBOL"，则将 "name" 添加到符号集合中
        if data.get('type') == 'SYMBOL' and 'name' in data:
            symbols.add(data['name'])
        # 递归查找字典中的每一项
        for key, value in data.items():
            find_symbols(value, symbols)
    elif isinstance(data, list):
        # 遍历列表中的每一项
        for item in data:
            find_symbols(item, symbols)
    return symbols
symbols = find_symbols(used_rules)

