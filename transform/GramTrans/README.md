# GramTrans: LL(1) Grammar Transformation

Implementation of the hierarchical conflict elimination algorithm. Automatically transforms any context-free grammar into an LL(1) grammar.

## Usage

### From Python Code
```python
from src.grammar import Grammar, Production, terminal, nonterminal
from src.gramtrans import GramTrans

# Define grammar with conflicts
A = nonterminal("A")
a, b, d = terminal("a"), terminal("b"), terminal("d")

productions = [
    Production(A, (a, b), "1"),  # A -> a b
    Production(A, (a, d), "2"),  # A -> a d (conflict: both start with 'a')
]

grammar = Grammar(productions, A)

# Transform to LL(1)
gramtrans = GramTrans(grammar)
ll1_grammar = gramtrans.transform()

print(ll1_grammar)
gramtrans.print_transformation_steps()
```

### From JSON Files
```python
from src.grammar_loader import load_grammar_from_json
from src.gramtrans import GramTrans

# Load grammar from JSON
grammar = load_grammar_from_json("examples/grammars/paper_example.json")

# Apply transformations
gramtrans = GramTrans(grammar)

# 1-layer transformation (no reordering)
grammar_1layer = gramtrans.transform(max_layers=1)

# Full LL(1) transformation (with reordering)
grammar_ll1 = gramtrans.transform()
```

### JSON Grammar Format
```json
{
  "terminals": ["a", "b", "d"],
  "nonterminals": ["A"],
  "start_symbol": "A",
  "productions": [
    {"id": "1", "left": "A", "right": ["a", "b"]},
    {"id": "2", "left": "A", "right": ["a", "d"]}
  ]
}
```

## Core Components

- **`Grammar`**: Represents context-free grammars with productions
- **`GramTrans`**: Main transformation algorithm
- **`ProgramTranslator`**: Bidirectional program conversion

## Key Features

- **Conflict Detection**: Identifies shared leading symbols and left recursion
- **Hierarchical Resolution**: Layer-by-layer conflict elimination
- **Symbol Optimization**: Minimizes new terminals through reordering
- **Partial Transformation**: Support for k-layer transformations

## Examples

Run the paper example:
```bash
python examples/paper_example.py
```

Complete demonstration:
```bash
python examples/complete_demo.py
```

## Algorithm Steps

1. Extract leading symbols from productions
2. Expand symbols iteratively to detect conflicts
3. Resolve conflicts using minimum hitting set
4. Optimize through symbol reordering
5. Verify LL(1) property

## Files

- `src/grammar.py`: Grammar data structures
- `src/gramtrans.py`: Main transformation algorithm
- `src/translator.py`: Program translation utilities
- `examples/`: Usage demonstrations and tests