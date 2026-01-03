"""
Core data structures for grammar representation
"""

from typing import List, Set, Dict, Optional, Tuple
from dataclasses import dataclass
from enum import Enum


class ConflictType(Enum):
    """Types of LL(1) conflicts"""
    SHARED_LEADING = "shared_leading"
    LEFT_RECURSION = "left_recursion"


@dataclass(frozen=True)
class Symbol:
    """Represents a grammar symbol (terminal or non-terminal)"""
    name: str
    is_terminal: bool
    
    def __post_init__(self):
        if not self.name:
            raise ValueError("Symbol name cannot be empty")
    
    def __str__(self) -> str:
        return self.name
    
    def __repr__(self) -> str:
        type_str = "T" if self.is_terminal else "NT"
        return f"Symbol({self.name}, {type_str})"


@dataclass(frozen=True)
class Production:
    """Represents a production rule: left -> right"""
    left: Symbol
    right: Tuple[Symbol, ...]
    rule_id: Optional[str] = None
    
    def __post_init__(self):
        if self.left.is_terminal:
            raise ValueError("Left side of production must be non-terminal")
        if not self.right:
            raise ValueError("Right side of production cannot be empty (use epsilon symbol instead)")
    
    def __str__(self) -> str:
        right_str = " ".join(str(symbol) for symbol in self.right)
        return f"{self.left} -> {right_str}"
    
    def __repr__(self) -> str:
        return f"Production({self.left}, {self.right})"
    
    def get_first_symbol(self) -> Symbol:
        """Get the first symbol on the right side"""
        return self.right[0]
    
    def is_epsilon_production(self) -> bool:
        """Check if this is an epsilon production"""
        return len(self.right) == 1 and self.right[0].name == "ε"


class Grammar:
    """Represents a context-free grammar"""
    
    def __init__(self, productions: List[Production], start_symbol: Optional[Symbol] = None):
        self.productions = productions
        self.start_symbol = start_symbol
        self._terminals: Optional[Set[Symbol]] = None
        self._nonterminals: Optional[Set[Symbol]] = None
        self._validate()
    
    def _validate(self):
        """Validate the grammar"""
        if not self.productions:
            raise ValueError("Grammar must have at least one production")
        
        # Set start symbol if not provided
        if self.start_symbol is None:
            self.start_symbol = self.productions[0].left
    
    @property
    def terminals(self) -> Set[Symbol]:
        """Get all terminal symbols in the grammar"""
        if self._terminals is None:
            self._compute_symbols()
        return self._terminals
    
    @property
    def nonterminals(self) -> Set[Symbol]:
        """Get all non-terminal symbols in the grammar"""
        if self._nonterminals is None:
            self._compute_symbols()
        return self._nonterminals
    
    def _compute_symbols(self):
        """Compute terminal and non-terminal sets"""
        self._terminals = set()
        self._nonterminals = set()
        
        for production in self.productions:
            self._nonterminals.add(production.left)
            for symbol in production.right:
                if symbol.is_terminal:
                    self._terminals.add(symbol)
                else:
                    self._nonterminals.add(symbol)
    
    def get_productions_for(self, nonterminal: Symbol) -> List[Production]:
        """Get all productions for a given non-terminal"""
        return [p for p in self.productions if p.left == nonterminal]
    
    def add_production(self, production: Production):
        """Add a new production to the grammar"""
        self.productions.append(production)
        # Reset cached symbols
        self._terminals = None
        self._nonterminals = None
    
    def remove_production(self, production: Production):
        """Remove a production from the grammar"""
        if production in self.productions:
            self.productions.remove(production)
            # Reset cached symbols
            self._terminals = None
            self._nonterminals = None
    
    def replace_production(self, old_production: Production, new_production: Production):
        """Replace an existing production with a new one"""
        for i, prod in enumerate(self.productions):
            if prod == old_production:
                self.productions[i] = new_production
                # Reset cached symbols
                self._terminals = None
                self._nonterminals = None
                break
    
    def copy(self) -> 'Grammar':
        """Create a deep copy of the grammar"""
        return Grammar(self.productions.copy(), self.start_symbol)
    
    def __str__(self) -> str:
        lines = []
        if self.start_symbol:
            lines.append(f"Start symbol: {self.start_symbol}")
        lines.append("Productions:")
        for i, production in enumerate(self.productions, 1):
            lines.append(f"  {i}. {production}")
        return "\n".join(lines)
    
    def __repr__(self) -> str:
        return f"Grammar({len(self.productions)} productions, start={self.start_symbol})"


# Utility functions for creating symbols
def terminal(name: str) -> Symbol:
    """Create a terminal symbol"""
    return Symbol(name, True)

def nonterminal(name: str) -> Symbol:
    """Create a non-terminal symbol"""
    return Symbol(name, False)

def epsilon() -> Symbol:
    """Create the epsilon symbol"""
    return Symbol("ε", True)