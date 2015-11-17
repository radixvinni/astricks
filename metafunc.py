#!/usr/bin/env python
#coding: utf-8

from meta.decompiler import decompile_func, compile_func
from meta import dump_python_source
import ast

class AstUsageExplorer (ast.NodeVisitor):
  def __init__(self):
    self.usage = set()
    self.calls = set()
    self.names = set()
  
  def visit_Call(self, node):
    self.usage.add(type(node).__name__)
    self.calls.add(ast.NodeVisitor.visit(self, node.func))
  
  def visit_Attribute(self, node):
    self.usage.add(type(node).__name__)
    return ast.NodeVisitor.visit(self, node.value) + '.' + node.attr
  
  def visit_Name(self, node):
    self.usage.add(type(node).__name__)
    self.names.add(node.id)
    return node.id
  
  def generic_visit(self, node):
    self.usage.add(type(node).__name__)
    ast.NodeVisitor.generic_visit(self, node)

class Mf:
  def __init__(self, func):
    self.ast = decompile_func(func)
    if isinstance(self.ast, ast.Lambda):
      self.ast = ast.FunctionDef(
        name="f", 
        args=self.ast.args, 
        body=[ast.Return(value=self.ast.body, lineno=1, col_offset=0)], 
        lineno=self.ast.lineno, 
        col_offset=self.ast.col_offset,
        decorator_list=[])
  
  def usage(self):
    ex = AstUsageExplorer()
    ast.NodeVisitor.generic_visit(ex,self.ast)
    return ex.usage, ex.calls, ex.names
  
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
    return "#%s%s"%(hash(self),dump_python_source(self.ast))