# Transform Scripts

This directory contains the core transformation and translation scripts for the GramTrans project.
Since we need use the Python and Java parser (we choose tree-sitter), we can't use the GramTrans script directly. Here are the script for tree-sitter format.

```
scripts/
├── grammar_explore_java.py     # java grammar explore 
├── grammar_explore_python.py   # python grammar explore
├── gramtrans_java.py           # transform java grammar 
├── gramtrans_python.py         # transform python grammar
├── java_trans.py               # translator for java
├── mathqa_trans.py             # translator for mathqa
└── python_trans.py             # translator for python
```

