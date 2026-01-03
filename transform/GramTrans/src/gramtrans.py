"""
Main GramTrans algorithm implementation
"""

from typing import List, Set, Dict, Tuple, Optional
from dataclasses import dataclass
from collections import defaultdict
import copy

from grammar import Symbol, Production, Grammar, ConflictType, terminal, nonterminal, epsilon


@dataclass
class ExpansionNode:
    """Node in the expansion tree"""
    symbol: Symbol
    children: List['ExpansionNode']
    depth: int
    production_used: Optional[Production] = None
    
    def __post_init__(self):
        if self.children is None:
            self.children = []
    
    def is_leaf(self) -> bool:
        """Check if this is a leaf node"""
        return len(self.children) == 0
    
    def get_leaf_symbols(self) -> List[Symbol]:
        """Get all leaf symbols in this subtree"""
        if self.is_leaf():
            return [self.symbol]
        
        leaves = []
        for child in self.children:
            leaves.extend(child.get_leaf_symbols())
        return leaves
    
    def has_cycle(self) -> bool:
        """Check if there's a cycle (left recursion) in this path"""
        def _check_cycle(node: 'ExpansionNode', path: Set[Symbol]) -> bool:
            if node.symbol in path and not node.symbol.is_terminal:
                return True
            
            if node.symbol.is_terminal:
                return False
                
            new_path = path.copy()
            new_path.add(node.symbol)
            
            for child in node.children:
                if _check_cycle(child, new_path):
                    return True
            return False
        
        return _check_cycle(self, set())
    
    def __str__(self) -> str:
        if self.is_leaf():
            return str(self.symbol)
        
        children_str = " ".join(str(child) for child in self.children)
        return f"({self.symbol} {children_str})"


class GramTrans:
    """Main GramTrans algorithm for converting CFG to LL(1)"""
    
    def __init__(self, grammar: Grammar):
        self.original_grammar = grammar
        self.working_grammar = grammar.copy()
        self.new_terminal_counter = 0
        self.transformation_log = []
    
    def transform(self, max_layers: Optional[int] = None) -> Grammar:
        """
        Transform the grammar to LL(1)
        
        Args:
            max_layers: Maximum number of layers to check. 
                       k-layer means check depths 0 to k-1.
                       If None, check all depths until convergence.
        
        Returns:
            LL(1) or partially transformed grammar
        """
        self.transformation_log.clear()
        self.new_terminal_counter = 0
        
        # Determine if this is k-layer transformation
        is_k_layer = max_layers is not None
        max_depth_to_check = max_layers - 1 if max_layers is not None else 10
        
        layer = 0
        
        while layer <= max_depth_to_check:
            # Step 1: Extract leading symbols
            leading_symbols = self._extract_leading_symbols()
            
            # Step 2: Expand symbols to current depth
            expansion_trees = self._expand_symbols(leading_symbols, layer)
            
            # Step 3: Detect conflicts at this depth
            conflicts = self._detect_conflicts(expansion_trees, layer)
            
            # Step 4: Resolve conflicts if found
            if conflicts:
                self._resolve_conflicts(conflicts)
                self.transformation_log.append(f"Layer {layer}: Resolved {len(conflicts)} conflicts")
                # After resolving conflicts, restart from layer 0
                layer = 0
                continue
            
            # Check termination conditions
            if is_k_layer and layer >= max_depth_to_check:
                # For k-layer, stop after checking k-1 depths
                break
            
            # Check if all leaves are terminals at this depth
            if self._all_leaves_are_terminals(expansion_trees):
                break
                
            layer += 1
        
        # Step 5: Symbol reordering optimization (only for full LL(1), not k-layer)
        if not is_k_layer:
            self._reorder_symbols()
            self.transformation_log.append("Applied symbol reordering optimization")
        
        return self.working_grammar
    
    def _extract_leading_symbols(self) -> Dict[Symbol, Set[Symbol]]:
        """Extract leading symbols for each non-terminal"""
        leading_symbols = defaultdict(set)
        
        for production in self.working_grammar.productions:
            left = production.left
            first_symbol = production.get_first_symbol()
            leading_symbols[left].add(first_symbol)
        
        return leading_symbols
    
    def _expand_symbols(self, leading_symbols: Dict[Symbol, Set[Symbol]], depth: int) -> Dict[Symbol, List[ExpansionNode]]:
        """Expand leading symbols to the specified depth"""
        expansion_trees = {}
        
        for nonterminal in self.working_grammar.nonterminals:
            trees = []
            productions = self.working_grammar.get_productions_for(nonterminal)
            
            for production in productions:
                tree = self._build_expansion_tree(production, depth)
                trees.append(tree)
            
            expansion_trees[nonterminal] = trees
        
        return expansion_trees
    
    def _build_expansion_tree(self, production: Production, max_depth: int) -> ExpansionNode:
        """Build expansion tree for a single production with strict depth control"""
        first_symbol = production.get_first_symbol()
        root = ExpansionNode(first_symbol, [], 0, production)
        
        # Only expand if we haven't reached max depth and symbol is non-terminal
        if max_depth > 0 and not first_symbol.is_terminal:
            self._expand_node(root, max_depth, set())
        
        return root
    
    def _expand_node(self, node: ExpansionNode, remaining_depth: int, visited: Set[Symbol]):
        """Recursively expand a node with cycle detection"""
        if remaining_depth <= 0 or node.symbol.is_terminal:
            return
        
        # Detect left recursion (immediate recursion to same symbol)
        if node.symbol in visited:
            return
        
        # Add current symbol to visited set
        new_visited = visited.copy()
        new_visited.add(node.symbol)
        
        # Get all productions for this non-terminal
        child_productions = self.working_grammar.get_productions_for(node.symbol)
        
        for child_prod in child_productions:
            first_child_symbol = child_prod.get_first_symbol()
            child_node = ExpansionNode(first_child_symbol, [], node.depth + 1, child_prod)
            node.children.append(child_node)
            
            # Recursively expand if not terminal and depth remaining
            if not first_child_symbol.is_terminal and remaining_depth > 1:
                self._expand_node(child_node, remaining_depth - 1, new_visited)
    
    def _detect_conflicts(self, expansion_trees: Dict[Symbol, List[ExpansionNode]], depth: int) -> Set[Tuple[Production, Production]]:
        """Detect LL(1) conflicts in expansion trees at specific depth"""
        conflicts = set()
        
        for nonterminal, trees in expansion_trees.items():
            # Check for left recursion in expansion trees (check for cycles in root-to-leaf paths)
            for tree in trees:
                if self._has_left_recursion_in_tree(tree):
                    # Left recursion detected - add self-conflict
                    conflicts.add((tree.production_used, tree.production_used))
            
            # Check for shared leading symbols at current depth
            symbol_to_productions = defaultdict(list)
            
            for tree in trees:
                # Get leading symbols at the specified depth
                leading_symbols = self._get_leading_symbols_at_depth(tree, depth)
                for symbol in leading_symbols:
                    symbol_to_productions[symbol].append(tree.production_used)
            
            # Find conflicts
            for symbol, productions in symbol_to_productions.items():
                if len(productions) > 1:
                    # Multiple productions can generate the same leading symbol
                    for i in range(len(productions)):
                        for j in range(i + 1, len(productions)):
                            if productions[i] != productions[j]:
                                conflicts.add((productions[i], productions[j]))
        
        return conflicts
    
    def _has_left_recursion_in_tree(self, tree: ExpansionNode) -> bool:
        """Check if there's a cycle (left recursion) in any root-to-leaf path"""
        def _check_path_for_cycle(node: ExpansionNode, path: List[Symbol]) -> bool:
            # If we've seen this symbol before in the current path, it's a cycle
            if node.symbol in path and not node.symbol.is_terminal:
                return True
            
            # If this is a terminal, no recursion possible
            if node.symbol.is_terminal:
                return False
            
            # Add current symbol to path and check children
            new_path = path + [node.symbol]
            for child in node.children:
                if _check_path_for_cycle(child, new_path):
                    return True
            
            return False
        
        return _check_path_for_cycle(tree, [])
    
    def _get_leading_symbols_at_depth(self, tree: ExpansionNode, target_depth: int) -> Set[Symbol]:
        """Get leading symbols at a specific depth in the expansion tree"""
        if tree.depth == target_depth:
            return {tree.symbol}
        elif tree.depth < target_depth and tree.children:
            leading_symbols = set()
            for child in tree.children:
                leading_symbols.update(self._get_leading_symbols_at_depth(child, target_depth))
            return leading_symbols
        else:
            return set()
    
    def _all_leaves_are_terminals(self, expansion_trees: Dict[Symbol, List[ExpansionNode]]) -> bool:
        """Check if all leaves in expansion trees are terminals"""
        for trees in expansion_trees.values():
            for tree in trees:
                leaf_symbols = tree.get_leaf_symbols()
                for symbol in leaf_symbols:
                    if not symbol.is_terminal:
                        return False
        return True
    
    def _resolve_conflicts(self, conflicts: Set[Tuple[Production, Production]]):
        """Resolve conflicts using minimum hitting set approach"""
        if not conflicts:
            return
        
        # Convert conflicts to list for easier handling
        conflict_list = list(conflicts)
        
        # Extract all unique productions involved in conflicts
        all_conflict_productions = set()
        for prod1, prod2 in conflict_list:
            all_conflict_productions.add(prod1)
            if prod1 != prod2:  # Not a self-conflict (left recursion)
                all_conflict_productions.add(prod2)
        
        # Find minimum hitting set using greedy approximation
        hitting_set = self._find_minimum_hitting_set(conflict_list)
        
        # Add distinguishing terminals to selected productions
        for production in hitting_set:
            self._add_distinguishing_terminal(production)
    
    def _find_minimum_hitting_set(self, conflicts: List[Tuple[Production, Production]]) -> Set[Production]:
        """Find minimum hitting set using greedy approximation algorithm"""
        hitting_set = set()
        uncovered_conflicts = set(range(len(conflicts)))
        
        while uncovered_conflicts:
            # Count how many uncovered conflicts each production can cover
            production_coverage = defaultdict(set)
            
            for conflict_idx in uncovered_conflicts:
                prod1, prod2 = conflicts[conflict_idx]
                production_coverage[prod1].add(conflict_idx)
                if prod1 != prod2:  # Not left recursion
                    production_coverage[prod2].add(conflict_idx)
            
            # Greedily select the production that covers the most uncovered conflicts
            best_production = None
            max_coverage = 0
            
            for production, covered_conflicts in production_coverage.items():
                coverage_count = len(covered_conflicts & uncovered_conflicts)
                if coverage_count > max_coverage:
                    max_coverage = coverage_count
                    best_production = production
            
            if best_production is None:
                break
            
            # Add to hitting set and remove covered conflicts
            hitting_set.add(best_production)
            covered_by_best = production_coverage[best_production] & uncovered_conflicts
            uncovered_conflicts -= covered_by_best
        
        return hitting_set
    
    def _add_distinguishing_terminal(self, production: Production):
        """Add a new terminal at the beginning of a production rule"""
        # Generate a unique new terminal
        new_terminal = terminal(f"new_term_{self.new_terminal_counter}")
        self.new_terminal_counter += 1
        
        # Create new production with the distinguishing terminal
        new_right = (new_terminal,) + production.right
        new_production = Production(production.left, new_right, production.rule_id)
        
        # Replace the old production
        self.working_grammar.replace_production(production, new_production)
    
    def _reorder_symbols(self):
        """Optimize by reordering symbols to reduce new terminals"""
        # Only process productions that start with new terminals
        productions_to_update = []
        used_leading_terminals = set()
        
        # Collect all current leading terminals (to avoid conflicts)
        current_leading_terminals = set()
        for production in self.working_grammar.productions:
            if production.right and production.right[0].is_terminal:
                if not production.right[0].name.startswith("new_term_"):
                    current_leading_terminals.add(production.right[0])
        
        for production in self.working_grammar.productions:
            # Skip if doesn't start with new terminal
            if not (production.right and production.right[0].is_terminal and 
                    production.right[0].name.startswith("new_term_")):
                continue
            
            new_terminal = production.right[0]
            rest_of_rule = production.right[1:]
            
            # Look for terminals in the rest of the rule that can become unique leading symbols
            replacement_found = False
            for i, symbol in enumerate(rest_of_rule):
                if (symbol.is_terminal and not symbol.name.startswith("new_term_")):
                    # Check if using this terminal as leading symbol would be unique
                    if (symbol not in current_leading_terminals and 
                        symbol not in used_leading_terminals):
                        # This terminal can be used as a unique leading symbol
                        new_right = list(rest_of_rule)
                        replacement_terminal = new_right.pop(i)
                        new_right = [replacement_terminal] + new_right
                        
                        new_production = Production(production.left, tuple(new_right), production.rule_id)
                        productions_to_update.append((production, new_production))
                        used_leading_terminals.add(replacement_terminal)
                        replacement_found = True
                        break
        
        # Apply all updates
        for old_prod, new_prod in productions_to_update:
            self.working_grammar.replace_production(old_prod, new_prod)
        
        # Log the optimization results
        if productions_to_update:
            self.transformation_log.append(f"Symbol reordering: replaced new terminals in {len(productions_to_update)} productions")
    
    def get_transformation_log(self) -> List[str]:
        """Get the transformation log"""
        return self.transformation_log.copy()
    
    def print_transformation_steps(self):
        """Print the transformation steps"""
        print("GramTrans Transformation Log:")
        print("=" * 40)
        for step in self.transformation_log:
            print(f"  {step}")
        print(f"  Total new terminals added: {self.new_terminal_counter}")
        print("=" * 40)