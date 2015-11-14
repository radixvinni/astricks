#!/usr/bin/env python
#coding: utf-8

from ast import *
from copy import copy

class RewriteNames(NodeTransformer):
    """Rewrite variable names in a function.
    Eg. if {'a':'b', 'x':'y', 'i':'j'}: ``for i in x: x[i] += a`` to ``for j in y: y[j] += b``
    """
    def __init__(self, names = {}):
      self.names = names
    
    def visit_Name(self, node):
        node.id = self.names[node.id]
        return node



class UnpackAugAssign(NodeTransformer):
    """Replaces augmented assignments with non-augmented ones.
    Eg., ``x[i] += y`` to ``x[i] = x[i] + y``.
    """
    def visit_AugAssign(self, node):
  
        load_target = copy(node.target)
        load_target.ctx = Load()
  
        op_node = BinOp(left=load_target, right=node.value, op=node.op)
        assign = Assign(targets=[node.target], value=copy_location(op_node, node))
  
        return copy_location(assign, node)

class UnpackAssignTargets(NodeTransformer):
    """Replaces tuple assignment with multiple ones.
    Eg., ``a,b,x = x,y,z`` to ``a = x; b = y; c = z``.
    """
    def visit_Assign(self, node):
      
      if not isinstance(node.target[0],Tuple): 
        return node
      
      return [ copy_location(Assign(targets=[target], value=node.value[0].elts[i]), node) 
              for i, target in enumerate(node.target[0].elts) ]

#TODO: rewrite (2).__add__(2) to 2+2 #parse('2 + 2', mode='eval')
