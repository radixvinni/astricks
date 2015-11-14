metafunc.py
===========

Function wrapper for decompiling and ast manipulation of wrapped function. Can be used as decorator with any python function or lambda.

```python
>>> Mf(lambda x:x+1)
#-5599708371849146885
def f(x):
    return (x + 1)
```

rewrite_rules.py
================

Defines NodeTransformers to modify ast

```python
>>> b=Mf(lambda y:y+1)
>>> RewriteNames({'y':'x'}).visit(b.ast)
<_ast.FunctionDef object at 0x7f5e03f5f350>
>>> b
#-5599708371849146885
def f(x):
    return (x + 1)
>>> b==a
True