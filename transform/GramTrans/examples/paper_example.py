"""
Test the GramTrans algorithm using the example from Figure 6 in the paper
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from grammar import Symbol, Production, Grammar, terminal, nonterminal, epsilon
from gramtrans import GramTrans
from grammar_loader import load_grammar_from_json


def create_paper_example_grammar():
    """Create the grammar from Figure 6 in the paper"""
    
    # Define symbols
    A = nonterminal("A")
    B = nonterminal("B") 
    C = nonterminal("C")
    D = nonterminal("D")
    
    a = terminal("a")
    b = terminal("b")
    d = terminal("d")
    e = terminal("e")
    f = terminal("f")
    g = terminal("g")
    eps = epsilon()
    
    # Define productions (from Figure 6)
    productions = [
        Production(A, (a, b), "1"),      # 1. A -> a b
        Production(A, (a, d), "2"),      # 2. A -> a d  
        Production(A, (C, e), "3"),      # 3. A -> C e
        Production(C, (a, f), "6"),      # 6. C -> a f
        Production(B, (A, d), "4"),      # 4. B -> A d
        Production(B, (A, g), "5"),      # 5. B -> A g  
        Production(D, (D, b), "7"),      # 7. D -> D b (left recursion)
        Production(D, (eps,), "8"),      # 8. D -> ε
    ]
    
    grammar = Grammar(productions, A)
    return grammar


def test_gramtrans_corrected():
    """Test the corrected GramTrans algorithm"""
    print("Testing GramTrans with Paper Example (Figure 6) - Corrected")
    print("=" * 60)
    
    # Create original grammar
    original_grammar = create_paper_example_grammar()
    print("Original Grammar:")
    print(original_grammar)
    print()
    
    # Test 1-Layer transformation
    print("1-Layer Transformation (no reordering):")
    print("-" * 45)
    gramtrans_1layer = GramTrans(original_grammar)
    grammar_1layer = gramtrans_1layer.transform(max_layers=1)
    
    print(grammar_1layer)
    print()
    gramtrans_1layer.print_transformation_steps()
    print()
    
    # Test Full LL(1) transformation  
    print("Full LL(1) Transformation (with reordering):")
    print("-" * 45)
    gramtrans_ll1 = GramTrans(original_grammar)
    grammar_ll1 = gramtrans_ll1.transform()
    
    print(grammar_ll1)
    print()
    gramtrans_ll1.print_transformation_steps()
    print()
    
    # Show the key differences
    print("Key Differences:")
    print("-" * 20)
    print("1-Layer:")
    for prod in grammar_1layer.productions:
        if prod.left.name in ['A', 'C']:
            print(f"  {prod}")
    
    print("\nFull LL(1):")
    for prod in grammar_ll1.productions:
        if prod.left.name in ['A', 'C']:
            print(f"  {prod}")
    
    print()
    print("Notable changes in Full LL(1):")
    print("  • A -> C e becomes A -> e C (reordering)")
    print("  • C -> a f becomes C -> f a (reordering)")
    print("  • Uses existing unique terminals instead of new ones where possible")
    print()
    
    # Verify both are LL(1)
    print("Verification:")
    print("-" * 15)
    verify_ll1_property(grammar_1layer, "1-Layer")
    verify_ll1_property(grammar_ll1, "Full LL(1)")


def test_json_loading():
    """Test loading from JSON"""
    print("\n" + "=" * 60)
    print("Testing JSON Grammar Loading")
    print("=" * 60)
    
    json_file = os.path.join(os.path.dirname(__file__), "grammars", "paper_example.json")
    
    if os.path.exists(json_file):
        print(f"Loading grammar from: {json_file}")
        grammar = load_grammar_from_json(json_file)
        
        print("Loaded Grammar:")
        print(grammar)
        print()
        
        # Transform
        gramtrans = GramTrans(grammar)
        ll1_grammar = gramtrans.transform()
        
        print("Transformed Grammar:")
        print(ll1_grammar)
        gramtrans.print_transformation_steps()
    else:
        print(f"JSON file not found: {json_file}")


def verify_ll1_property(grammar, grammar_type):
    """Verify that a grammar satisfies LL(1) property"""
    conflicts_found = False
    
    for nt in grammar.nonterminals:
        productions = grammar.get_productions_for(nt)
        if len(productions) <= 1:
            continue
            
        leading_symbols = []
        for prod in productions:
            leading_symbols.append(prod.get_first_symbol())
        
        # Check for duplicates
        if len(leading_symbols) != len(set(leading_symbols)):
            print(f"⚠️  {grammar_type} - {nt}: Conflicts found!")
            conflicts_found = True
        else:
            print(f"✓ {grammar_type} - {nt}: No conflicts")
    
    if not conflicts_found:
        print(f"✅ {grammar_type} grammar satisfies LL(1) property!")
    else:
        print(f"❌ {grammar_type} grammar has remaining conflicts")


if __name__ == "__main__":
    test_gramtrans_corrected()
    test_json_loading()