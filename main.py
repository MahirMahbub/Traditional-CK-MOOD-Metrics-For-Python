# -*- coding: utf-8 -*-
"""
Created on Wed Oct 16 15:23:49 2019

@author: mahir
"""
import sys
import Raw
from McCabe import get_code_complexity
try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO


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

val = get_complexity_number(if_elif_else_dead_path, strio)
sys.stdout = stdout
print(val)

loc = Raw.analyze(if_elif_else_dead_path)
comment_percentage = loc.comments/(loc.loc-loc.blank-loc.comments)
print("McCabe Cyclomatric Complexity: ", val)
print("LOC: ",loc.loc)
print("Multi Line of Comment: ", loc.multi)
print("Single Line of Comment: ", loc.comments)
print("Comment Percentage: ",comment_percentage)


