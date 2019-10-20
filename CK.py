# -*- coding: utf-8 -*-
"""
Created on Thu Oct 17 11:38:38 2019

@author: mahir
"""

import ast
import copy
import re, sys
from McCabe import get_code_complexity
try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO
import textwrap

mdef = '''
import V
class A(object):
    def meth(self):
        return sum(i for i in range(10) if i - 2 < 5)
    def fib(self, n):
        pass
class B(A):
    def _thi(self, mo):
        for i in range(5):
            for j in i:
                print(j)
        return sum(i for i in range(10) if i - 2 < 5)
    def fib(self, n):
        self.p = 0
        g = A()
        g.meth()
        g.fib(n)
        h=0
        __d = h
        f, k = 0
        if n < 2: return 1
        return fib(n - 1) + fib(n - 2)
class C(A, B):
    def fr(self):
        return 34
        
class E(object):
    def fr(self):
        return 34
class F(E):
    def meth(self):
        return sum(i for i in range(10) if i - 2 < 5)
    def fib(self, n):
        pass
    '''
def findAllMethods(script):
    reg = re.compile('((?:^[ \t]*)def \w+\(.*\): *(?=.*?[^ \t\n]).*\r?\n)'
                 '|'
                 '((^[ \t]*)def \w+\(.*\): *\r?\n'
                 '(?:[ \t]*\r?\n)*'
                 '\\3([ \t]+)[^ \t].*\r?\n'
                 '(?:[ \t]*\r?\n)*'
                 '(\\3\\4.*\r?\n(?: *\r?\n)*)*)',
                 re.MULTILINE)
    arr =[]
    
    for ma in  reg.finditer(script):
        #print ("aaaa ",ma.group())
        arr.append(ma.group())
        
    return arr 

def get_complexity_number(snippet, strio, max=0):
    """Get the complexity number from the printed string."""
    # Report from the lowest complexity number.
    get_code_complexity(snippet, max)
    strio_val = strio.getvalue()
    strio.close()
    if strio_val:
        return int(strio_val.split()[-1].strip("()"))
    else:
        return None
   
def weighted_method_per_class(source):
    print()
    print("Metrics Name: Weighted Method Per Class")
    classes = re.findall('(class[\s\S]*?)(?=class|$)',source)
    
    for clas in classes:
        astt = ast.parse(clas)
        def_class = [n for n in ast.walk(astt) if type(n) == ast.ClassDef]
        print()
        print("    Class Name: ", def_class[0].name)
        methods = findAllMethods(clas)
        wmpc=0
        for method in methods:
            method = textwrap.dedent(method)
            a = ast.parse(method)
            definitions = [n for n in ast.walk(a) if type(n) == ast.FunctionDef]
            #print(method)
            stdout = sys.stdout
            strio = StringIO()
            sys.stdout = strio
            
            #print(findAllMethods(method))
            val = get_complexity_number(method, strio)
            sys.stdout = stdout
            print("            Method Name: ", definitions[0].name)
            print("            Complexity", val)
            #print()
            wmpc+=val
        print("        Weighted Method Per Class for ",def_class[0].name, "is ", wmpc)
        

def inheritance_tree(source):
    a = ast.parse(mdef)
    all_node = set()
    definitions = [n for n in ast.walk(a) if type(n) == ast.ClassDef]
    #print(definitions)
    inheritance_tree = {}
    for i in definitions:
        all_node.update(i.name)
        inheritance_tree[i.name] = []
        print("Parent Class: ", i.name)
        for j in i.bases:
            if not j.id== "object": 
                inheritance_tree[i.name].append(j.id)
                print("    Inherited Class",j.id)
    return inheritance_tree, all_node, definitions

def depth_of_inheritance_tree_util(tree,counter, max_counter):
    print()
    print("Metrics Name: Depth of Inheritance Tree: ")
    for child in tree:
        counter+=1
        max_counter = depth_of_inheritance_tree(tree, child, counter, max_counter)
        max_counter = max(max_counter, counter)
        counter-=1
        #print(child, max_counter)
    print("    DIT: ", max_counter)
    return max_counter
def depth_of_inheritance_tree(tree, node, counter, max_counter):
    for child in tree[node]:
        if not child == None and not child == "":
            counter+=1

            max_counter = depth_of_inheritance_tree(tree, child, counter, max_counter)
            max_counter = max(max_counter, counter)
            #print(max_counter, node)
            counter-=1
    return max_counter
def Number_of_child(tree, all_node):
    print()
    print("Metrics Name: Number of Child")
    print()
    child = {}
    for i in all_node:
        child[i] = []
    for node in all_node:
        for parent in tree:
            if node in tree[parent]:
                child[node].append(parent)
    for parent in child:
        print("    Class: ", parent)
        print("        Number of Child: ", str(len(child[parent])))
    return child
def attr_hiding_factor(astree):
    print()
    print("Metrics Name: Attribute Hiding Factor")
    print()
    for class_obj in astree:
        #print("Class Name: ", class_obj.name)
        variable_count = 0
        private_var_count = 0
        class_attr= set()
        class_pr_attr = set()
        for func_obj in class_obj.body:

            for statements in func_obj.body:
                if isinstance(statements,ast.Assign):
                    for variables in statements.targets:
                        if isinstance(variables,ast.Tuple):
                            if isinstance(variables, ast.Attribute):
                                if variables.attr[0] == "_":
                                    class_attr.update(variables.attr)
                                    class_pr_attr.update(variables.attr)
                                else:
                                    class_attr.update(variables.attr)
                            else:
                                for var in variables.elts:
                                    #print(var.id)
                                    variable_count+=1
                                    if var.id[0] == "_":
                                        private_var_count+=1
                        elif isinstance(variables,ast.Name):
                            #print(variables.id)
                            variable_count+=1
                            if variables.id[0] == "_":
                                private_var_count+=1
                        elif isinstance(variables, ast.Attribute):
                            if variables.attr[0] == "_":
                                class_attr.update(variables.attr)
                                class_pr_attr.update(variables.attr)
                            else:
                                class_attr.update(variables.attr)
        variable_count +=len(class_attr)
        private_var_count +=len(class_pr_attr)
        if variable_count>0:
            hiding_factor = private_var_count/variable_count
        else:
            hiding_factor = 0
        print("    Class: "+class_obj.name, ": ")
        print("        FHF: ", hiding_factor)
            
def method_hiding_factor(astree):
     print()
     print("Metrics Name: Method Hiding Factor")
     print()
     for class_obj in astree:
        #print("Class Name: ", class_obj.name)
        function_count = 0
        private_func_count = 0
        for func_obj in class_obj.body:
            function_count += 1
            if func_obj.name[0] == "_":
                private_func_count += 1
        hiding_factor = private_func_count/function_count
        print("    Class "+class_obj.name, ": ")
        print("        MHF: ", hiding_factor)
def BFS(child_tree, start, visited, all_inherit):
    for child in child_tree[start]:
        if not child in visited:
            visited.append(child)
            for parent in inheritance_tree[child]:
                all_inherit[child]+=all_inherit[parent]
            #all_inherit[child]+=all_inherit[start]
            BFS(child_tree, child, visited, all_inherit)
        else:
            return
        
    
def method_inheritance_factor(inheritance_tree, child_tree, astree):
    print()
    print("Metrics Name: Method Inheritance Factor")
    print()
    class_to_method = {}
    for classes in astree:
        all_method = []
        for methods in classes.body:
            all_method.append(methods.name)
        class_to_method[classes.name] = all_method.copy()
    class_inherit_method = copy.deepcopy(class_to_method) 
    visited = []
    for node in inheritance_tree:
        if len(inheritance_tree[node]) == 0:
            BFS(child_tree, node, visited, class_inherit_method)
            
    #print(class_inherit_method)
    #print( class_to_method)
    inherit_count = {}
    for node in class_to_method:
        inherit_count[node] = len(set(class_inherit_method[node])-set(class_to_method[node]))
    #print(inherit_count)
    MIF = {}
    for node in class_to_method:
        if not inherit_count[node] == 0:
            MIF[node] =  inherit_count[node]/len(set(class_inherit_method[node]))
        else:
            MIF[node] = 0
    #print(inherit_count)
    for factor in MIF:
        print("    Class: ", factor)
        print("        MIF: ", MIF[factor])
            

def coupling_factor(astree):
    print()
    print("Metrics Name: Coupling Factor")
    print()
    classes = []
    for clas in astree:
        classes.append(clas.name)
    #print(classes)
    coupling = 0
    for clas in astree:
        for func in clas.body:
            for line in func.body:
                if isinstance(line, ast.Assign) and isinstance(line.value, ast.Call):
                    if line.value.func.id in classes:
                        coupling+=1
    print("    COF: ", coupling/len(classes))
                    
def CK_MOOD_Metrics(inheritance_tree, all_node, astree):  
    maxi = depth_of_inheritance_tree_util(inheritance_tree, 0, 0)
    child_tree = Number_of_child(inheritance_tree, all_node)
    #print(child_tree)
    attr_hiding_factor(astree)
    method_hiding_factor(astree)
    method_inheritance_factor(inheritance_tree, child_tree, astree)
    weighted_method_per_class(mdef)
    coupling_factor(astree)
    
inheritance_tree, all_node, astree = inheritance_tree(mdef)    
CK_MOOD_Metrics(inheritance_tree, all_node, astree)