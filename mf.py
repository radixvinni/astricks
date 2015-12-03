#!/usr/bin/env python
#coding: utf-8
"trying to use uncompyle2 + astor instead of Meta"

from uncompyle2 import magics, scanner25, scanner26, scanner27, walker

from imp import get_magic
from StringIO import StringIO
from astor import to_source

import ast

def compile_func(ast_node, filename, globals, **defaults):
    '''
    Compile a function from an ast.FunctionDef instance.
    :return: A python function object
    '''

    funcion_name = ast_node.name
    module = ast.Module(body=[ast_node])

    ctx = {'%s_default' % key : arg for key, arg in defaults.items()}
    code = compile(module, filename, 'exec')
    eval(code, globals, ctx)
    function = ctx[funcion_name]

    return function

def make_function_def(code, stmnts, defaults=None, lineno=0):
        "Make ast.FunctionDef of a function with given code and decompiled body"
        if code.co_flags & 2:
            vararg = None
            kwarg = None

        varnames = list(code.co_varnames[:code.co_argcount])
        co_locals = list(code.co_varnames[code.co_argcount:])

        #have var args
        if code.co_flags & 4:
            vararg = co_locals.pop(0)

        #have kw args
        if code.co_flags & 8:
            kwarg = co_locals.pop(0)

        args = [ast.Name(id=argname, ctx=ast.Param(), lineno=lineno, col_offset=0) for argname in varnames]
            
        args = ast.arguments(args=args,
                              defaults=defaults if defaults else [],
                              kwarg=kwarg,
                              vararg=vararg,
                              lineno=lineno, col_offset=0
                              )
        """if instructions.seen_yield: #TODO: generator functions
                return_ = stmnts[-1]

                assert isinstance(return_, ast.Return)
                assert isinstance(return_.value, ast.Name)
                assert return_.value.id == 'None'
                return_.value = None"""
        ast_obj = ast.FunctionDef(name='f' if code.co_name == '<lambda>' else code.co_name, args=args, body=stmnts, decorator_list=[], lineno=lineno, col_offset=0)

        return ast_obj

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
    #TODO self.defaults = func.func_defaults if sys.version_info.major < 3 else func.__defaults__
  
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
