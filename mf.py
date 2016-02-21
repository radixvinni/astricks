#!/usr/bin/env python
#coding: utf-8
"trying to use uncompyle2 + astor instead of Meta"

from uncompyle2 import magics, scanner25, scanner26, scanner27, walker
from metastring import compile_func, make_function_def

from imp import get_magic
from StringIO import StringIO
from astor import to_source

import ast

class Mf:
  def __init__(self, func):
    version = float(magics.versions[get_magic()]) #2.7
    if hasattr(func, 'func_code'):
        co = func.func_code
    else:
        co = func.__code__ 
    
    out = StringIO()
    
    if version == 2.7:
        scanner = scanner27.Scanner27()
    elif version == 2.6:
        scanner = scanner26.Scanner26()
    elif version == 2.5:
        scanner = scanner25.Scanner25()
    
    scanner.setShowAsm(0, out)
    tokens, customize = scanner.disassemble(co)
    walk = walker.Walker(out, scanner, showast=0)
    
    self.ast = walk.build_ast(tokens, customize)
    if self.ast[-1] == walker.RETURN_NONE:
            ast.pop() # remove last node
            #todo: if empty, add ast.Pass()
    
    walk.mod_globs = self.globs = walker.find_globals(self.ast, set())
    
    self.customize = customize
    self.walk = walk
    
    dump = StringIO()
    self.walk.f = dump
    self.walk.gen_source(self.ast, self.customize)
    
    stmt = ast.parse(dump.getvalue()).body
    self.ast = make_function_def(co, stmt, func.__defaults__)
    #self.defaults = func.func_defaults if sys.version_info.major < 3 else func.__defaults__
  
  def dump(self):
    return ast.dump(self.ast)
  
  def __call__(self, *args, **kwargs):
    self.ast = ast.fix_missing_locations(self.ast)
    return compile_func(self.ast, __name__, globals())(*args, **kwargs)
  
  def __hash__(self):
    return hash(ast.dump(self.ast))
  
  def __eq__(self,other):
    return ast.dump(self.ast) == ast.dump(other.ast)
  
  def __repr__(self):
    return to_source(self.ast)

if __name__ == "__main__":
    print Mf(lambda x:x+1)
