"""
GramTrans: Automatic LL(1) Grammar Transformation
"""

from .grammar import Symbol, Production, Grammar
from .gramtrans import GramTrans

__version__ = "1.0.0"
__all__ = ["Symbol", "Production", "Grammar", "GramTrans"]