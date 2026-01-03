"""
Demonstration of JSON grammar loading and GramTrans transformation
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from grammar_loader import load_grammar_from_json, save_grammar_to_json
from gramtrans import GramTrans


def demo_json_loading():
    """Demonstrate loading grammars from JSON files"""
    print("GramTrans: JSON Grammar Loading Demo")
    print("=" * 40)
    print()
    
    # Test files
    test_files = [
        "grammars/simple_conflict.json",
        "grammars/paper_example.json",
        "grammars/arithmetic.json"
    ]
    
    for json_file in test_files:
        filepath = os.path.join(os.path.dirname(__file__), json_file)
        
        if not os.path.exists(filepath):
            print(f"⚠️  File not found: {json_file}")
            continue
            
        print(f"📁 Loading: {json_file}")
        print("-" * 30)
        
        try:
            # Load grammar from JSON
            grammar = load_grammar_from_json(filepath)
            
            print("Original Grammar:")
            print(grammar)
            print()
            
            # Apply transformations
            print("1-Layer Transformation:")
            gramtrans_1layer = GramTrans(grammar)
            grammar_1layer = gramtrans_1layer.transform(max_layers=1)
            print(grammar_1layer)
            gramtrans_1layer.print_transformation_steps()
            print()
            
            print("Full LL(1) Transformation:")
            gramtrans_ll1 = GramTrans(grammar)
            grammar_ll1 = gramtrans_ll1.transform()
            print(grammar_ll1)
            gramtrans_ll1.print_transformation_steps()
            
            # Save transformed grammars
            output_dir = os.path.join(os.path.dirname(__file__), "output")
            os.makedirs(output_dir, exist_ok=True)
            
            base_name = os.path.splitext(os.path.basename(json_file))[0]
            
            save_grammar_to_json(grammar_1layer, 
                               os.path.join(output_dir, f"{base_name}_1layer.json"))
            save_grammar_to_json(grammar_ll1, 
                               os.path.join(output_dir, f"{base_name}_ll1.json"))
            
            print(f"💾 Saved transformed grammars to output/{base_name}_*.json")
            print()
            
            # Verify LL(1) property
            verify_ll1_property(grammar_1layer, "1-Layer")
            verify_ll1_property(grammar_ll1, "Full LL(1)")
            
        except Exception as e:
            print(f"❌ Error processing {json_file}: {e}")
        
        print("=" * 50)
        print()


def verify_ll1_property(grammar, transformation_type):
    """Verify LL(1) property of transformed grammar"""
    print(f"🔍 Verifying {transformation_type} Grammar:")
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
            print(f"  ⚠️  {nt}: Conflicts found - {[str(s) for s in leading_symbols]}")
            conflicts_found = True
        else:
            print(f"  ✓ {nt}: No conflicts ({len(productions)} productions)")
    
    if not conflicts_found:
        print(f"  ✅ {transformation_type} grammar satisfies LL(1) property!")
    else:
        print(f"  ❌ {transformation_type} grammar has remaining conflicts")
    print()


def demo_custom_grammar():
    """Demonstrate creating and transforming a custom grammar"""
    print("📝 Custom Grammar Example")
    print("-" * 30)
    
    # Create a custom grammar with left recursion
    custom_grammar = {
        "terminals": ["x", "y", "+"],
        "nonterminals": ["S", "E"],
        "start_symbol": "S",
        "productions": [
            {"id": "1", "left": "S", "right": ["E"]},
            {"id": "2", "left": "E", "right": ["E", "+", "x"]},  # Left recursive
            {"id": "3", "left": "E", "right": ["x"]},
            {"id": "4", "left": "E", "right": ["y"]}
        ]
    }
    
    # Save to file
    custom_file = os.path.join(os.path.dirname(__file__), "output", "custom.json")
    os.makedirs(os.path.dirname(custom_file), exist_ok=True)
    
    import json
    with open(custom_file, 'w') as f:
        json.dump(custom_grammar, f, indent=2)
    
    print(f"Created custom grammar: {custom_file}")
    
    # Load and transform
    grammar = load_grammar_from_json(custom_file)
    print("Original Grammar:")
    print(grammar)
    print()
    
    # Transform
    gramtrans = GramTrans(grammar)
    ll1_grammar = gramtrans.transform()
    
    print("Transformed LL(1) Grammar:")
    print(ll1_grammar)
    gramtrans.print_transformation_steps()


if __name__ == "__main__":
    demo_json_loading()
    demo_custom_grammar()