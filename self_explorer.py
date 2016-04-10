import ast

def _get_last_line_number(node):
    if hasattr(node,'lineno'):
        max_line_number = node.lineno
    else:
        return -1
        
    for child_node in ast.iter_child_nodes(node):
        max_line_number = max(_get_last_line_number(child_node),max_line_number)
    return max_line_number

class AnalysisNodeVisitor(ast.NodeVisitor):
    def __init__(self):
        self.node = None
        self.modules = []
        
    def visit_Module(self, node):
      node.parent = self.node
      self.node = node
      self.node.names = self.names = {x:{'type':'builtin'} for x in dir(__builtins__) + ['__file__','__builtins__']}
      ast.NodeVisitor.generic_visit(self, node)
    
    def visit_Name(self, target, scope=None):
        scope = scope or self.node
        if isinstance(target.ctx, ast.Load):
            if target.id not in scope.names:
              if scope.parent: return self.visit_Name(target, scope.parent)
              print target.lineno, target.id
        else:
          self.names[target.id] = {'line_number':target.lineno,'type':'variable'}
    
    def visit_ListComp(self, node):
      for x in node.generators: ast.NodeVisitor.generic_visit(self, x)
      ast.NodeVisitor.generic_visit(self, node)
    
    visit_GeneratorExp = visit_SetComp = visit_DictComp = visit_ListComp
    
    def analize_module(self, name):
      if name not in self.modules:
          self.modules.append(name)
          return
          module = __import__(name)
          if '__file__' in dir(module):
            if module.__file__.endswith('.py'):
              self.visit(ast.parse(open(module.__file__).read()))
            elif module.__file__[-4:] in ['.pyo','.pyc']:
              self.visit(ast.parse(open(module.__file__[:-1]).read()))
          else:
            print 'using bultins from module', name
    
    def visit_Import(self,node):
        for x in node.names:
          self.names[x.name] = {'line_number':node.lineno,'type':'import'}
          self.analize_module(x.name)
        ast.NodeVisitor.generic_visit(self, node)
  
    def visit_ImportFrom(self,node):
        for x in node.names:
          self.names[x.name] = {'line_number':node.lineno,'type':'import'}
        
        self.analize_module(node.module)
        ast.NodeVisitor.generic_visit(self, node)
    
    def visit_arguments(self, node):
      for target in node.args:
        self.names[target.id] = {'type':'param'}
      
      if node.vararg:
        self.names[node.vararg] = {'type':'param','value_type':'list'}
      
      if node.kwarg:
        self.names[node.kwarg] = {'type':'param','value_type':'dict'}
    
    def visit_FunctionDef(self,node):
        functionNode = {'type':'function','start_line':node.lineno,'end_line':_get_last_line_number(node),'docstring':(ast.get_docstring(node,clean = False))}
        self.names[node.name] = (functionNode)
        node.names = {}
        node.parent = self.node
        self.node = node
        ast.NodeVisitor.generic_visit(self, node)
        self.node = node.parent
  
    def visit_ClassDef(self,node):
        classNode = {'type':'class','start_line':node.lineno,'end_line':_get_last_line_number(node),'docstring':(ast.get_docstring(node,clean = False))}
        self.names[node.name] = (classNode)
        node.names = {}
        node.parent = self.node
        self.node = node
        ast.NodeVisitor.generic_visit(self, node)
        self.node = node.parent
  
AnalysisNodeVisitor().visit(ast.parse(open(__file__).read()))