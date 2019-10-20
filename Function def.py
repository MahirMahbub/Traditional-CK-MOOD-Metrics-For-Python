# -*- coding: utf-8 -*-
"""
Created on Wed Oct 16 14:16:31 2019

@author: mahir
"""

import ast

mdef = 'def foo(x):\n sod\n return 2*x'
mdef = '''
import V.ast
class A(object):
    def meth(self):
        a= ast()
        return sum(i for i in range(10) if i - 2 < 5)
    def fib(self, n):
        pass
class B(A):
    def thi(self, mo):
        return sum(i for i in range(10) if i - 2 < 5)
    def fib(self, n):
        h=0
        __d = 0
        if n < 2: return 1
        return fib(n - 1) + fib(n - 2)
class C(A, B):
    def fr(self):
        return 34
    '''
a = ast.parse(mdef)
definitions = [n for n in ast.walk(a) if type(n) == ast.ClassDef]
inheritance_tree = {}
for i in definitions:
    inheritance_tree[i.name] = []
    print(i.name)
    for j in i.bases:
        if not j.id== "object": 
            inheritance_tree[i.name].append(j.id)
            print("Inherited",j.id)
import pprint
from radon.complexity import cc_rank, cc_visit
val = cc_visit('''
class A(object):
    def meth(self):
        return sum(i for i in range(10) if i - 2 < 5)
class B(A):
    def thi(self):
        return sum(i for i in range(10) if i - 2 < 5)
def fib(n):
    if n < 2: return 1
    return fib(n - 1) + fib(n - 2)
''')
pp = pprint.PrettyPrinter(indent=4)
#pp.pprint(val)
#print(val)