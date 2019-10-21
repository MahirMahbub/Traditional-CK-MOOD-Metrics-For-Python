# -*- coding: utf-8 -*-
"""
Created on Wed Oct 16 15:23:49 2019

@author: mahir
"""
import sys
import Raw
from CK import *
from McCabe import get_code_complexity
try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO
import os

mdef = '''class A(object):
    def meth(self):
        return sum(i for i in range(10) if i - 2 < 5)
    def fib(self, n):
        pass
class B(A):
    def _thi(self, mo):
        return sum(i for i in range(10) if i - 2 < 5)
    def fib(self, n):
        self.p = 0
        g = A()
        g.meth()
        h=0
        __d = h
        f, k = 0
        if n < 2: return 1
        return fib(n - 1) + fib(n - 2)
class C(A, B):
    def fr(self):
        return 34
    '''

if_elif_else_dead_path = """\
def f(n):

    if n > 3:
        return "bigger than three"
    elif n > 4:
        return "is never executed"
        #fdgdgdg
    else:
        return "smaller than or equal to three"
"""
'''
stdout = sys.stdout
strio = StringIO()
sys.stdout = strio


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

val = get_complexity_number(mdef, strio)
sys.stdout = stdout
print(val)

loc = Raw.analyze(if_elif_else_dead_path)
comment_percentage = loc.comments/(loc.loc-loc.blank-loc.comments)
print("McCabe Cyclomatric Complexity: ", val)
print("LOC: ",loc.loc)
print("Multi Line of Comment: ", loc.multi)
print("Single Line of Comment: ", loc.comments)
print("Comment Percentage: ",comment_percentage)
'''

def collectingPath(direc, pathList = []):
    count = 0
    for filename in os.listdir(direc):
        pathway = os.path.join(direc, filename) 
        if os.path.isfile(pathway) and pathway.endswith(".py"):
            pathList.append(pathway)  
        elif os.path.isdir(pathway):  
            pathList = collectingPath(pathway,  pathList)
    #print(len(pathList))
    return pathList

def read_files(path_list):
    mdef = ""
    for path in path_list:
        with open(path,encoding="utf8", mode = 'r') as reader:
            val = reader.read()
            mdef += "\n"
            mdef += val
        
    return mdef

path_List =collectingPath(r"C:\Users\mahir\Desktop\Python-OOP-Toy-master\\")
mdef = read_files(path_List)
loca = Raw.analyze(mdef)
comment_percentage = loca.comments/(loca.loc-loca.blank-loca.comments)
#print("McCabe Cyclomatric Complexity: ", val)
print("Overall Report")
print("LOC: ",loca.loc)
print("Multi Line of Comment: ", loca.multi)
print("Single Line of Comment: ", loca.comments)
print("Comment Percentage: ",comment_percentage)
large_Class_Method(mdef)
#mdef = remove_comments_and_docstrings(mdef)
#print(mdef)
#inherit_tree, all_node, astree = inheritance_tree(mdef)  
#print(all_node)  
#CK_MOOD_Metrics(mdef, inherit_tree, all_node, astree)


