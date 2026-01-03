"""
Complete example demonstrating GramTrans usage
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from grammar import Grammar, Production, terminal, nonterminal, epsilon
from gramtrans import GramTrans


def main():
    print("GramTrans: Automatic LL(1) Grammar Transformation")
    print("=" * 55)
    print()
    
    # Example 1: Simple conflict resolution
    print("Example 1: Resolving Leading Symbol Conflicts")
    print("-" * 45)
    
    # Create grammar with shared leading symbols
    A = nonterminal("A")
    a, b, d = terminal("a"), terminal("b"), terminal("d")
    
    productions = [
        Production(A, (a, b), "1"),  # A -> a b
        Production(A, (a, d), "2"),  # A -> a d (conflict: both start with 'a')
    ]
    
    grammar = Grammar(productions, A)
    print("Original Grammar:")
    print(grammar)
    print()
    
    # Apply GramTrans
    gramtrans = GramTrans(grammar)
    ll1_grammar = gramtrans.transform()
    
    print("Transformed LL(1) Grammar:")
    print(ll1_grammar)
    print()
    
    gramtrans.print_transformation_steps()
    print()
    
    # Example 2: Left recursion elimination
    print("Example 2: Left Recursion Elimination")
    print("-" * 40)
    
    # Create left-recursive grammar
    S = nonterminal("S")
    x, y = terminal("x"), terminal("y")
    
    productions = [
        Production(S, (S, x), "1"),  # S -> S x (left recursive)
        Production(S, (y,), "2"),    # S -> y
    ]
    
    grammar = Grammar(productions, S)
    print("Original Grammar (with left recursion):")
    print(grammar)
    print()
    
    gramtrans = GramTrans(grammar)
    ll1_grammar = gramtrans.transform()
    
    print("Transformed LL(1) Grammar:")
    print(ll1_grammar)
    print()
    
    gramtrans.print_transformation_steps()
    print()
    
    # Example 3: Complex grammar from paper
    print("Example 3: Paper Example (Figure 6)")
    print("-" * 35)
    
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
    print("Original Grammar:")
    print(grammar)
    print()
    
    gramtrans = GramTrans(grammar)
    ll1_grammar = gramtrans.transform()
    
    print("Transformed LL(1) Grammar:")
    print(ll1_grammar)
    print()
    
    gramtrans.print_transformation_steps()
    print()
    
    # Verify LL(1) property
    print("Verification:")
    print("-" * 15)
    verify_ll1_property(ll1_grammar)
    print()
    
    # Example 4: Partial transformation
    print("Example 4: Partial Transformation (1-layer)")
    print("-" * 45)
    
    gramtrans_partial = GramTrans(grammar)
    partial_ll1 = gramtrans_partial.transform(max_layers=1)
    
    print("1-Layer Transformed Grammar:")
    print(partial_ll1)
    print()
    
    gramtrans_partial.print_transformation_steps()
    print()
    
    print("Algorithm Performance:")
    print(f"  Full transformation: {gramtrans.new_terminal_counter} new terminals")
    print(f"  1-layer transformation: {gramtrans_partial.new_terminal_counter} new terminals")
    print()
    
    print("✓ GramTrans demonstration complete!")


def verify_ll1_property(grammar):
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
            print(f"⚠️  Conflict found in {nt}: {leading_symbols}")
            conflicts_found = True
        else:
            print(f"✓ {nt}: No conflicts ({len(productions)} productions)")
    
    if not conflicts_found:
        print("✓ Grammar satisfies LL(1) property!")
    else:
        print("✗ Grammar has remaining conflicts")


if __name__ == "__main__":
    main()