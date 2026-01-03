"""
Grammar loader for JSON format
"""

import json
from typing import Dict, List, Any
from grammar import Grammar, Production, Symbol, terminal, nonterminal, epsilon


def load_grammar_from_json(filepath: str) -> Grammar:
    """Load grammar from JSON file"""
    with open(filepath, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Create symbol mapping
    symbols = {}
    
    # Create terminals
    for term_name in data.get('terminals', []):
        symbols[term_name] = terminal(term_name)
    
    # Create non-terminals
    for nonterm_name in data.get('nonterminals', []):
        symbols[nonterm_name] = nonterminal(nonterm_name)
    
    # Handle epsilon if present
    if 'ε' in data.get('terminals', []) or 'epsilon' in data.get('terminals', []):
        symbols['ε'] = epsilon()
        symbols['epsilon'] = epsilon()
    
    # Create productions
    productions = []
    for prod_data in data['productions']:
        left_name = prod_data['left']
        right_names = prod_data['right']
        rule_id = prod_data.get('id', None)
        
        if left_name not in symbols:
            symbols[left_name] = nonterminal(left_name)
        
        left_symbol = symbols[left_name]
        right_symbols = []
        
        for right_name in right_names:
            if right_name not in symbols:
                # Auto-detect if it's terminal or non-terminal
                # If it appears as left side of any production, it's non-terminal
                is_nonterminal = any(p['left'] == right_name for p in data['productions'])
                if is_nonterminal:
                    symbols[right_name] = nonterminal(right_name)
                else:
                    symbols[right_name] = terminal(right_name)
            
            right_symbols.append(symbols[right_name])
        
        production = Production(left_symbol, tuple(right_symbols), rule_id)
        productions.append(production)
    
    # Get start symbol
    start_symbol_name = data.get('start_symbol')
    start_symbol = symbols.get(start_symbol_name) if start_symbol_name else None
    
    return Grammar(productions, start_symbol)


def save_grammar_to_json(grammar: Grammar, filepath: str):
    """Save grammar to JSON file"""
    data = {
        'terminals': [str(t) for t in sorted(grammar.terminals, key=lambda x: x.name)],
        'nonterminals': [str(nt) for nt in sorted(grammar.nonterminals, key=lambda x: x.name)],
        'start_symbol': str(grammar.start_symbol) if grammar.start_symbol else None,
        'productions': []
    }
    
    for i, production in enumerate(grammar.productions):
        prod_data = {
            'id': production.rule_id or str(i + 1),
            'left': str(production.left),
            'right': [str(s) for s in production.right]
        }
        data['productions'].append(prod_data)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def validate_grammar_json(data: Dict[str, Any]) -> bool:
    """Validate JSON grammar format"""
    required_fields = ['productions']
    optional_fields = ['terminals', 'nonterminals', 'start_symbol']
    
    # Check required fields
    for field in required_fields:
        if field not in data:
            return False
    
    # Validate productions format
    if not isinstance(data['productions'], list):
        return False
    
    for prod in data['productions']:
        if not isinstance(prod, dict):
            return False
        if 'left' not in prod or 'right' not in prod:
            return False
        if not isinstance(prod['right'], list):
            return False
    
    return True


# Example JSON format:
EXAMPLE_JSON_FORMAT = {
    "terminals": ["a", "b", "d", "e", "f", "g", "ε"],
    "nonterminals": ["A", "B", "C", "D"],
    "start_symbol": "A",
    "productions": [
        {"id": "1", "left": "A", "right": ["a", "b"]},
        {"id": "2", "left": "A", "right": ["a", "d"]},
        {"id": "3", "left": "A", "right": ["C", "e"]},
        {"id": "6", "left": "C", "right": ["a", "f"]},
        {"id": "4", "left": "B", "right": ["A", "d"]},
        {"id": "5", "left": "B", "right": ["A", "g"]},
        {"id": "7", "left": "D", "right": ["D", "b"]},
        {"id": "8", "left": "D", "right": ["ε"]}
    ]
}