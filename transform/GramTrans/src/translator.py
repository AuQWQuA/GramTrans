"""
Program translator between original and LL(1) grammars
"""

from typing import List, Dict, Optional, Tuple, Any
from dataclasses import dataclass
import copy

from grammar import Symbol, Production, Grammar, terminal, nonterminal


@dataclass
class ParseNode:
    """Node in a parse tree"""
    symbol: Symbol
    children: List['ParseNode']
    production: Optional[Production] = None
    token_value: Optional[str] = None  # For terminal nodes
    
    def __post_init__(self):
        if self.children is None:
            self.children = []
    
    def is_leaf(self) -> bool:
        return len(self.children) == 0
    
    def to_program(self) -> str:
        """Convert parse tree back to program string"""
        if self.is_leaf():
            return self.token_value or str(self.symbol)
        
        result = []
        for child in self.children:
            child_str = child.to_program()
            if child_str.strip():  # Skip empty strings
                result.append(child_str)
        
        return " ".join(result)


class SimpleParser:
    """Simple recursive descent parser"""
    
    def __init__(self, grammar: Grammar):
        self.grammar = grammar
        self.tokens = []
        self.position = 0
    
    def parse(self, tokens: List[str]) -> ParseNode:
        """Parse tokens into a parse tree"""
        self.tokens = tokens
        self.position = 0
        
        if not self.grammar.start_symbol:
            raise ValueError("Grammar has no start symbol")
        
        return self._parse_nonterminal(self.grammar.start_symbol)
    
    def _parse_nonterminal(self, nonterminal: Symbol) -> ParseNode:
        """Parse a non-terminal"""
        if self.position >= len(self.tokens):
            raise ValueError(f"Unexpected end of input when parsing {nonterminal}")
        
        # Get all productions for this non-terminal
        productions = self.grammar.get_productions_for(nonterminal)
        
        # Try each production
        for production in productions:
            saved_position = self.position
            try:
                children = []
                
                # Try to match each symbol in the production
                for symbol in production.right:
                    if symbol.is_terminal:
                        child = self._parse_terminal(symbol)
                    else:
                        child = self._parse_nonterminal(symbol)
                    children.append(child)
                
                # Success - create parse node
                return ParseNode(nonterminal, children, production)
                
            except ValueError:
                # Backtrack and try next production
                self.position = saved_position
                continue
        
        # No production matched
        current_token = self.tokens[self.position] if self.position < len(self.tokens) else "EOF"
        raise ValueError(f"No valid production for {nonterminal} at token '{current_token}'")
    
    def _parse_terminal(self, terminal: Symbol) -> ParseNode:
        """Parse a terminal symbol"""
        if self.position >= len(self.tokens):
            raise ValueError(f"Expected {terminal} but reached end of input")
        
        current_token = self.tokens[self.position]
        
        # Handle special terminals
        if terminal.name == "ε":
            # Epsilon - don't consume token
            return ParseNode(terminal, [], token_value="")
        
        # Match terminal
        if (terminal.name == current_token or 
            terminal.name.startswith("new_term_")):  # New terminals match any token
            self.position += 1
            return ParseNode(terminal, [], token_value=current_token)
        
        raise ValueError(f"Expected {terminal} but got '{current_token}'")


class ProgramTranslator:
    """Translates programs between original and LL(1) grammars"""
    
    def __init__(self, original_grammar: Grammar, ll1_grammar: Grammar, 
                 production_mapping: Dict[Production, Production]):
        self.original_grammar = original_grammar
        self.ll1_grammar = ll1_grammar
        self.production_mapping = production_mapping  # original -> ll1
        self.reverse_mapping = {v: k for k, v in production_mapping.items()}  # ll1 -> original
        
        self.original_parser = SimpleParser(original_grammar)
        self.ll1_parser = SimpleParser(ll1_grammar)
    
    def original_to_ll1(self, program: str) -> str:
        """Translate program from original grammar to LL(1) grammar"""
        # Tokenize
        tokens = program.split()
        
        # Parse with original grammar
        parse_tree = self.original_parser.parse(tokens)
        
        # Transform parse tree
        ll1_tree = self._transform_tree_to_ll1(parse_tree)
        
        # Generate LL(1) program
        return ll1_tree.to_program()
    
    def ll1_to_original(self, program: str) -> str:
        """Translate program from LL(1) grammar to original grammar"""
        # Tokenize (filter out new terminals)
        tokens = [t for t in program.split() if not t.startswith("new_term_")]
        
        # Parse with LL(1) grammar
        parse_tree = self.ll1_parser.parse(program.split())
        
        # Transform parse tree
        original_tree = self._transform_tree_to_original(parse_tree)
        
        # Generate original program
        return original_tree.to_program()
    
    def _transform_tree_to_ll1(self, node: ParseNode) -> ParseNode:
        """Transform parse tree from original to LL(1)"""
        if node.is_leaf():
            return ParseNode(node.symbol, [], token_value=node.token_value)
        
        # Find corresponding LL(1) production
        if node.production and node.production in self.production_mapping:
            ll1_production = self.production_mapping[node.production]
            
            # Transform children
            ll1_children = []
            original_child_idx = 0
            
            for ll1_symbol in ll1_production.right:
                if ll1_symbol.name.startswith("new_term_"):
                    # This is a new distinguishing terminal
                    ll1_children.append(ParseNode(ll1_symbol, [], token_value=ll1_symbol.name))
                else:
                    # Map from original children
                    if original_child_idx < len(node.children):
                        original_child = node.children[original_child_idx]
                        ll1_child = self._transform_tree_to_ll1(original_child)
                        ll1_children.append(ll1_child)
                        original_child_idx += 1
            
            return ParseNode(node.symbol, ll1_children, ll1_production)
        
        # Fallback - direct transformation
        ll1_children = []
        for child in node.children:
            ll1_children.append(self._transform_tree_to_ll1(child))
        
        return ParseNode(node.symbol, ll1_children, node.production)
    
    def _transform_tree_to_original(self, node: ParseNode) -> ParseNode:
        """Transform parse tree from LL(1) to original"""
        if node.is_leaf():
            # Skip new terminals
            if node.symbol.name.startswith("new_term_"):
                return None
            return ParseNode(node.symbol, [], token_value=node.token_value)
        
        # Find corresponding original production
        if node.production and node.production in self.reverse_mapping:
            original_production = self.reverse_mapping[node.production]
            
            # Transform children (skip new terminals)
            original_children = []
            for child in node.children:
                if child.symbol.name.startswith("new_term_"):
                    continue  # Skip new terminals
                
                transformed_child = self._transform_tree_to_original(child)
                if transformed_child is not None:
                    original_children.append(transformed_child)
            
            return ParseNode(node.symbol, original_children, original_production)
        
        # Fallback - direct transformation
        original_children = []
        for child in node.children:
            transformed_child = self._transform_tree_to_original(child)
            if transformed_child is not None:
                original_children.append(transformed_child)
        
        return ParseNode(node.symbol, original_children, node.production)


def create_translator_from_gramtrans(original_grammar: Grammar, gramtrans) -> ProgramTranslator:
    """Create a translator from a GramTrans instance"""
    ll1_grammar = gramtrans.working_grammar
    
    # Create production mapping based on rule IDs or position
    production_mapping = {}
    
    for i, original_prod in enumerate(original_grammar.productions):
        # Find corresponding LL(1) production
        for ll1_prod in ll1_grammar.productions:
            if (ll1_prod.rule_id == original_prod.rule_id or 
                (ll1_prod.left == original_prod.left and 
                 _productions_equivalent(original_prod, ll1_prod))):
                production_mapping[original_prod] = ll1_prod
                break
    
    return ProgramTranslator(original_grammar, ll1_grammar, production_mapping)


def _productions_equivalent(prod1: Production, prod2: Production) -> bool:
    """Check if two productions are equivalent (ignoring new terminals)"""
    if prod1.left != prod2.left:
        return False
    
    # Filter out new terminals from prod2
    filtered_right = tuple(s for s in prod2.right if not s.name.startswith("new_term_"))
    
    return prod1.right == filtered_right