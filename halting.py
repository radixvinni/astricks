#!/usr/bin/env python
#coding: utf-8

from mf import Mf as _Mf
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


class Mf(_Mf):
  def usage(self):
    ex = AstUsageExplorer()
    ast.NodeVisitor.generic_visit(ex,self.ast)
    return ex.usage | ex.calls

  def halting(self):
    allowed = set(["Return","Assign","BinOp","Compare","AugAssign","Num","Name","For","Load","Store","Add","Mult","Sub","Div","And","Lt","LtE","Gt","GtE","arguments","Call","range"])
    return self.usage() - allowed
  