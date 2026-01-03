"""
Test program translation functionality
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from grammar import Symbol, Production, Grammar, terminal, nonterminal, epsilon
from gramtrans import GramTrans
from translator import create_translator_from_gramtrans


def create_simple_arithmetic_grammar():
    """Create a simple arithmetic expression grammar"""
    
    # Define symbols
    E = nonterminal("E")  # Expression
    T = nonterminal("T")  # Term
    F = nonterminal("F")  # Factor
    
    plus = terminal("+")
    mult = terminal("*")
    lparen = terminal("(")
    rparen = terminal(")")
    num = terminal("num")
    
    # Define productions
    productions = [
        Production(E, (E, plus, T), "1"),    # E -> E + T (left recursive)
        Production(E, (T,), "2"),            # E -> T
        Production(T, (T, mult, F), "3"),    # T -> T * F (left recursive)
        Production(T, (F,), "4"),            # T -> F
        Production(F, (lparen, E, rparen), "5"),  # F -> ( E )
        Production(F, (num,), "6"),          # F -> num
    ]
    
    grammar = Grammar(productions, E)
    return grammar


def test_arithmetic_translation():
    """Test translation of arithmetic expressions"""
    print("Testing Arithmetic Expression Translation")
    print("=" * 50)
    
    # Create original grammar
    original_grammar = create_simple_arithmetic_grammar()
    print("Original Grammar:")
    print(original_grammar)
    print()
    
    # Transform to LL(1)
    gramtrans = GramTrans(original_grammar)
    ll1_grammar = gramtrans.transform()
    
    print("LL(1) Grammar:")
    print(ll1_grammar)
    print()
    
    gramtrans.print_transformation_steps()
    print()
    
    # Create translator
    translator = create_translator_from_gramtrans(original_grammar, gramtrans)
    
    # Test programs
    test_programs = [
        "num + num",
        "num * num",
        "( num + num ) * num",
        "num + num * num"
    ]
    
    print("Translation Tests:")
    print("-" * 30)
    
    for program in test_programs:
        try:
            print(f"Original: {program}")
            ll1_program = translator.original_to_ll1(program)
            print(f"LL(1):    {ll1_program}")
            
            # Translate back
            back_program = translator.ll1_to_original(ll1_program)
            print(f"Back:     {back_program}")
            
            if program == back_program:
                print("✓ Round-trip successful")
            else:
                print("✗ Round-trip failed")
            print()
            
        except Exception as e:
            print(f"✗ Error: {e}")
            print()


def test_simple_grammar():
    """Test with a very simple grammar"""
    print("\n" + "=" * 50)
    print("Testing Simple Grammar")
    print("=" * 50)
    
    # Create simple grammar: S -> a S | b
    S = nonterminal("S")
    a = terminal("a")
    b = terminal("b")
    
    productions = [
        Production(S, (a, S), "1"),  # S -> a S (left recursive)
        Production(S, (b,), "2"),    # S -> b
    ]
    
    grammar = Grammar(productions, S)
    print("Original Grammar:")
    print(grammar)
    print()
    
    # Transform
    gramtrans = GramTrans(grammar)
    ll1_grammar = gramtrans.transform()
    
    print("LL(1) Grammar:")
    print(ll1_grammar)
    print()
    
    # Test translation
    translator = create_translator_from_gramtrans(grammar, gramtrans)
    
    test_programs = ["b", "a b", "a a b"]
    
    for program in test_programs:
        try:
            print(f"Original: {program}")
            ll1_program = translator.original_to_ll1(program)
            print(f"LL(1):    {ll1_program}")
            back_program = translator.ll1_to_original(ll1_program)
            print(f"Back:     {back_program}")
            print("✓ Success" if program == back_program else "✗ Failed")
            print()
        except Exception as e:
            print(f"✗ Error: {e}")
            print()


if __name__ == "__main__":
    test_simple_grammar()
    test_arithmetic_translation()