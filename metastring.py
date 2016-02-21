#!/usr/bin/env python
#coding: utf-8

import ast
from astor import to_source

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


class Ms:
  def __init__(self, func):
    if not isinstance(func, (unicode,str)): 
      self.ast = make_function_def(func, ast.parse(func.__doc__).body, func.__defaults__)
      return
    
    self.ast = ast.parse(func).body
    if len(self.ast) == 0: 
      raise RuntimeError('string empty')
    
    self.ast = self.ast[0]
    if isinstance(self.ast, ast.Expr): 
      self.ast = self.ast.value
    
    if isinstance(self.ast, ast.Lambda):
      self.ast = ast.FunctionDef(
        name="f",
        args=self.ast.args, 
        body=[ast.Return(value=self.ast.body, lineno=self.ast.lineno, col_offset=1)], 
        lineno=self.ast.lineno, 
        col_offset=self.ast.col_offset,
        decorator_list=[])
  
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